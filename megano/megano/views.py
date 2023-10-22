from pathlib import Path

from django.shortcuts import render


def func1(request):
    return render(request, 'base/base.html')