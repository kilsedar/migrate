from django.shortcuts import render
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from forms import DownloadForm

# Create your views here.
def submit(request):
    dform = DownloadForm(request.POST or None)
    if dform.is_valid():
      dform.save()
      return redirect(reverse('free_data'))
    return render(request, 'download.html', context={'dform': dform})
