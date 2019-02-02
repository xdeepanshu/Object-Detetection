import six
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

import json
from .forms import PhotoForm
from .models import Photo

def filter_nones(d):
    return dict((k, v) for k, v in six.iteritems(d) if v is not None)


@login_required
def list_view(request):
    user = request.user
    #Only users can see there own images
    return render(request, 'list.html', dict(photos=Photo.objects.filter(user=user)))

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