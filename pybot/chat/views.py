from django.shortcuts import render
from django.views import generic


class Index(generic.View):
    def get(self, request):
        return render(request, 'chat/index.html')