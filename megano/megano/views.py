from pathlib import Path

from django.shortcuts import render


# func testing
def func1(request):
    return render(request, 'base/base.html')