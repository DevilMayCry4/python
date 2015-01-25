
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context

def getCrumb(requset):
    t = get_template('crumb')
    xml = t.render(Context({'item': 'test'}))
    return HttpResponse(xml)