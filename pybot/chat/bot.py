import requests
from bs4 import BeautifulSoup

from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect


def bot(request):
    question = request.POST['message'].lower()
    if question == 'бот':
        answer = "Привет!"
    elif question == 'выйти':
        logout(request)
        return redirect('chat:index')
    elif "заголовок сайта" in question:
        site = question.split()[-1]
        req = requests.get(site)
        soup = BeautifulSoup(req.text, 'html.parser')
        title = soup.title
        if title:
            answer = title.string
        else:
            answer = "Заголовка на данном сайте не присутсвует"
    elif "h1 с сайта" in question:
        site = question.split()[-1]
        req = requests.get(site)
        soup = BeautifulSoup(req.text, 'html.parser')
        h1 = soup.h1
        if not h1:
            answer = "h1 на данном сайте не присутсвует"
        else:
            answer = h1.string
    elif "все варианты заголовков с сайтов" in question:
        # sites = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|'
        #                    '(?:%[0-9a-fA-F][0-9a-fA-F]))+', question)
        start = question.find('сайтов') + len('сайтов')
        sites = question[start:].split(",")
        answer = ""
        for site in sites:
            req = requests.get(site.strip())
            soup = BeautifulSoup(req.text, 'html.parser')
            title = soup.title
            answer += site + ": "
            if title:
                answer += title.string + "<br>"
            else:
                answer += "Заголовок не найден <br>"
    elif "сохрани для меня информацию" in question:
        start_phrase = question.find("сохрани для меня информацию")
        start_phrase += len("сохрани для меня информацию")
        phrase = question[start_phrase:].strip()
        if phrase:
            answer = "Сохранил: " + phrase
            request.user.notes_set.create(note=phrase)
        else:
            priv_query = request.user.query_set.order_by('-date')[0]
            request.user.notes_set.create(note=priv_query.answer)
            answer = "Сохранил: " + priv_query.answer
    elif "последнее сохранил" in question:
        try:
            note = request.user.notes_set.order_by('-date')[0]
            answer = note.note
        except IndexError:
            answer = "Вы еще ничего не просили меня сохранять"
    elif "напомни мне" in question:
        answer = "Напоминать еще не умею."
    else:
        answer = "Неизвестная команда"
    request.user.query_set.create(question=question, answer=answer)
    queries = request.user.query_set.order_by('date')
    context = {'queries': queries}
    response = render(request, 'chat/index.html', context)
    return response

