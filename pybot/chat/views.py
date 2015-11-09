import datetime

from django.shortcuts import render
from django.views import generic
from .models import Query
from django.contrib.auth.models import User

from .bot import bot

user = User.objects.get(username='jay')

class Login(generic.View):
    def get(self, request):
        return render(request, 'chat/login.html')


class Index(generic.View):
    def get(self, request):
        queries = user.query_set.order_by('date')
        context = {'queries': queries}
        return render(request, 'chat/index.html', context)

    def post(self, request):
        question = request.POST['message']
        answer = bot(question)
        user.query_set.create(question=question, answer=answer)
        queries = user.query_set.order_by('date')

        context = {'queries': queries}
        # date = datetime.datetime.now().strftime("дата %d.%m.%Y %H:%M:%S:")
        return render(request, 'chat/index.html', context)