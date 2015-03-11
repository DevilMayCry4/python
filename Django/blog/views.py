from django.shortcuts import render
 
def postlist(request):
    return render(request, 'post_list.html', {})