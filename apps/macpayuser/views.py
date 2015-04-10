from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.views.generic import View

# Create your views here.




class HomeView(View):

    def get(self, request):
        return render_to_response('index.html')