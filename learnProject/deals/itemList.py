from deals.models import cateoryModel
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from deals.models import itemModel
import xml.etree.ElementTree as ET

'''
def dealValue(value):
    if value == None:
        return ''
    else:
        return value

def itemList(requset):
    tree = ET.parse('/Users/virgil/Desktop/list (15).xml')
    root = tree.getroot()
    for offers in tree.findall('offers'):
        for offer in offers.findall('offer'):
            images = ''
            for imgs in offer.findall('imgs'):
                for img in imgs.findall('img'):
                    images=images+img.text+'|'
            pName=''
            pPhone=''
            pEmail=''
            pLogo=''
            Maddress=''
            Mdescription=''
            Mlongitude=''
            Mlatitude=''
            for p in  offer.findall('partner'):
                pName = p.find('name').text
                pPhone = p.find('phone').text
                pEmail = p.find('email').text
                pLogo = p.find('logo').text

            redemptions = offer.find('redemptions')
            if len(redemptions) > 0 :
                redemption = redemptions[0]
                Maddress = redemption.find('address').text
                Mdescription = redemption.find('description').text
                Mlongitude = redemption.find('longitude').text
                Mlatitude = redemption.find('latitude').text

            mcity =  offer.findall('city')[0]
            cityID = dealValue(mcity.find('id').text)
            cityName = dealValue(mcity.find('name').text)
            citySlug_name = dealValue(mcity.find('slug_name').text)
            cityTimezone = dealValue(mcity.find('timezone').text)
            cityLanguage = dealValue(mcity.find('language').text)
            Mhas_child = ''
            if  offer.find('has_child').text != None:
                               Mhas_child= offer.find('has_child').text
            mDiscount = offer.find('discount').text
            if mDiscount == None:
                mDiscount =''

            item =itemModel(item_id=offer.get('id'),
                            ccode=offer.get('ccode'),
                            title=dealValue(offer.find('title').text),
                            short_title=dealValue(offer.find('short_title').text),
                            desc=dealValue(offer.find('desc').text),
                            disclaimer=dealValue(offer.find('disclaimer').text),
                            highlights=dealValue(offer.find('highlights').text),
                            imgs=images,
                            price=dealValue(offer.find('price').text),
                            value=dealValue(offer.find('value').text),
                            discount=mDiscount,
                            discount_display_type=dealValue(offer.find('discount_display_type').text),
                            is_hide_sold_quantity=dealValue(offer.find('is_hide_sold_quantity').text),
                            is_paperless=dealValue(offer.find('is_paperless').text),
                            quantity=dealValue(offer.find('quantity').text),
                            max_purchase_quantity=dealValue(offer.find('max_purchase_quantity').text),
                            deal_on_quantity=dealValue(offer.find('deal_on_quantity').text),
                            display_weight=dealValue(offer.find('display_weight').text),
                            start_date=dealValue(offer.find('start_date').text),
                            end_date=dealValue(offer.find('end_date').text),
                            valid_since=dealValue(offer.find('valid_since').text),
                            expiry=dealValue(offer.find('expiry').text),
                             has_child= Mhas_child,
                            lock_quantity=dealValue(offer.find('lock_quantity').text),
                            is_soldout=dealValue(offer.find('is_soldout').text),
                            is_deal_on=dealValue(offer.find('is_deal_on').text),
                            deal_on_at=dealValue(offer.find('deal_on_at').text),
                            partner_name=pName,
                            partner_log=pLogo,
                            partner_email=pEmail,
                            partner_phone=pPhone,
                            address=Maddress,
                            description=Mdescription,
                            longitude=Mlongitude,
                            latitude=Mlatitude,
                            redemption_method=dealValue(offer.find('redemption_method').text),
                            city_id=cityID,
                            city_name=cityName,
                            city_slug_name=citySlug_name,
                            city_timezone=cityTimezone,
                            city_language=cityLanguage,
                            payment_method='VISA',
                            category='13',
                            )
            item.save()
    return HttpResponse(len(itemModel.objects.all()))
'''
def itemList(request):
    page = int(request.GET['page'])
    count = int(request.GET['count'])
    objects = None
    if 'category' in request.GET:
           category = request.GET['category']
           objects = itemModel.objects.filter(category=category)[count*page:(page+1)*count]
    else :
            objects = itemModel.objects.order_by('item_id')[count*page:(page+1)*count]
    t = get_template('item.xml')
    xml = t.render(Context({'item_list': objects}))
    return HttpResponse(xml)