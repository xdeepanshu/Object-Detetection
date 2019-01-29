import six
from django.shortcuts import render

from .forms import PhotoForm
from .models import Photo


def filter_nones(d):
    return dict((k, v) for k, v in six.iteritems(d) if v is not None)


def list_view(request):
    defaults = dict(format="jpg", height=150, width=150)
    defaults["class"] = "thumbnail inline"

    # The different transformations to present
    samples = [
        dict(crop="fill", radius=10),
        dict(crop="scale"),
        dict(crop="fit", format="png"),
        dict(crop="thumb", gravity="face"),
        dict(format="png", angle=20, height=None, width=None, transformation=[
            dict(crop="fill", gravity="north", width=150, height=150, effect="sepia"),
        ]),
    ]
    samples = [filter_nones(dict(defaults, **sample)) for sample in samples]
    return render(request, 'list.html', dict(photos=Photo.objects.all(), samples=samples))


def upload(request):
    context = dict(
        backend_form=PhotoForm(),
    )
    if request.method == 'POST':
        # Only backend upload should be posting here
        form = PhotoForm(request.POST, request.FILES)
        context['posted'] = form.instance
        if form.is_valid():
            # Uploads image and creates a model instance for it
            result = form.save()
            print(result.image.url)
    return render(request, 'upload.html', context)