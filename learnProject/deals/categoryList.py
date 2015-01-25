from deals.models import cateoryModel
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
import xml.etree.ElementTree as ET

def categoryList(requset):
    objects = cateoryModel.objects.all()
    t = get_template('category.xml')
    xml = t.render(Context({'item_list': objects}))
    return HttpResponse(xml)
    '''
    tree = ET.parse('/Users/virgil/Desktop/list (4).xml')
    root = tree.getroot()
    for categorys in tree.findall('categories'):
        for category in categorys.findall('category'):
            c =  cateoryModel(name=category.find('name').text,slug_name=category.find('slug_name').text,categoryId=category.find('id').text)
            c.save()
    return HttpResponse(len(cateoryModel.objects.all()))
    '''
