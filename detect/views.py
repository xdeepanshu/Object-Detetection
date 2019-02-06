import six
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

import json
from .forms import PhotoForm
from .models import Photo

def filter_nones(d):
    return dict((k, v) for k, v in six.iteritems(d) if v is not None)


@login_required
def list_view(request):
    user = request.user
    #Only users can see there own images
    photos = Photo.objects.filter(user=user)
    return render(request, 'list.html', dict(photos=photos))

@login_required
def upload(request):
    context = dict(
        backend_form=PhotoForm(),
    )
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        context['posted'] = form.instance
        if form.is_valid():
            # Uploads image and creates a model instance for it
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
    return render(request, 'upload.html', context)

@login_required
def photo_detail(request,public_id):
    user = request.user
    context = {}
    try:
        user_photo = Photo.objects.filter(user=user)
        for photo in user_photo:
            if photo.image.public_id == public_id:
                print("Found")
                text=json.loads(photo.watson_response)["images"][0]["classifiers"][0]['classes']
                context = dict(photo=photo, text=text)
        else:
            raise ObjectDoesNotExist()
    except ObjectDoesNotExist:
        pass
    return render(request, 'detail.html', context)

@login_required
def photo_delete(request, public_id):
    user = request.user

    try:
        user_photos = Photo.objects.filter(user=user)
        for photo in user_photos:
            if photo.image.public_id == public_id:
                #To delete it from an instance
                photo.delete()
            else:   
                raise ObjectDoesNotExist()
    except ObjectDoesNotExist:
        pass
    return redirect('/')

