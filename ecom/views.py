from django.http import HttpResponseRedirect
from django.shortcuts import render


def home_view(request):

    return render(request, 'ecom/index.html', {})



