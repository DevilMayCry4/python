from django.http import  HttpResponse
from django import template

DATABASE_NAME = '/home/django/db.sqlite3'

def Hello(request):
    file = open('website/index.html')
    t = template.Template(file.read())
    context = template.Context({'name':'hello world'})
    return HttpResponse(t.render(context))
