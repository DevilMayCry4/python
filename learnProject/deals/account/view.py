#coding=utf-8
from django.shortcuts import render
from django import forms
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from  deals.models import User
from django.views.decorators.csrf import csrf_exempt
import json

#定义表单模型
class UserForm(forms.Form):
    default_errors = {
    'required': 'This field is required',
    'invalid': 'Enter a valid value'
    }
    username = forms.CharField(max_length=100,error_messages=default_errors)
    password = forms.CharField(max_length=100,error_messages=default_errors)
    email = forms.EmailField(max_length=100,error_messages=default_errors)

# Create your views here.
@csrf_exempt
def register(request):
    message =''
    if request.method == "POST":
        uf = UserForm(request.POST)
        if uf.is_valid():
            #获取表单信息
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            email = uf.cleaned_data['email']
            #将表单写入数据库
            user = User()
            user.username = username
            user.password = password
            user.email = email
            user.save()
            #返回注册成功页面
            return render_to_response('success')
        else:
            if uf.errors:
                messageJson = json.loads(uf.errors.as_json())
                for filed in uf.errors:
                    if messageJson[filed] != None:
                       message = message +filed+':'+ messageJson[filed][0]['message']+'.\n'

            else:
                message='资料有误'
    else:
        message='请使用post'
    return render_to_response('fail',{'message':message})