from django.shortcuts import render
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .bot import bot

PASSWORD = "12345"


class Index(generic.View):
    def get(self, request):
        if request.user.is_authenticated():
            queries = request.user.query_set.order_by('date')
            context = {'queries': queries}
            return render(request, 'chat/index.html', context)
        else:
            greeting = "Здравствуйте, меня зовут PyBot, для начала работы "
            greeting += "со мной введите ваше имя."
            context = {"answer": greeting}
            return render(request, 'chat/auth.html', context)


    def post(self, request):
        if request.user.is_authenticated():
            return bot(request)
        else:
            username = request.POST['message']
            user = authenticate(username=username, password=PASSWORD)
            if not user:
                User.objects.create_user(username, "", PASSWORD)
                user = authenticate(username=username, password=PASSWORD)
            login(request, user)
            context = {
                "answer": "Добро пожаловать, {}.".format(username)
            }
            return render(request, 'chat/auth.html', context)
