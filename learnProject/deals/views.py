from django.shortcuts import render
from django.http import HttpResponse
from deals.models import User
from deals.form import LoginForm
from django.template.loader import get_template
from django.template import Context
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
# Create your views here.

@csrf_exempt
def login(request):
    message = ''
    if request.method == "POST":
       form = LoginForm(request.POST)
       if form.is_valid():
           username = form.cleaned_data['username']
           password = form.cleaned_data['password']
           users = User.objects.filter(username=username)
           if len(users):
               user = users[0]
               if user.password == password:
                   t = get_template('login')
                   xml = t.render(Context({'user': user}))
                   return HttpResponse(xml)
               else:
                   message = 'password is wrong'
           else:
              message = username+'no exist'
       else:
            if form.errors:
                messageJson = json.loads(form.errors.as_json())
                for filed in form.errors:
                    if messageJson[filed] != None:
                       message = message +filed+':'+ messageJson[filed][0]['message']+'.\n'

            else:
                message = 'wrong data'

    else:
         message = 'use post'

    return render_to_response('fail',{'message':message})