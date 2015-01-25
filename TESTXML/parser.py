import xml.etree.ElementTree as ET


if __name__ == '__main__':
    tree = ET.parse('/Users/virgil/Desktop/list (2).xml')
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
            for p in offer.findall('partner'):
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

            mcity = offer.findall('city')[0]
            cityID = mcity.find('id').text
            cityName = mcity.find('name').text
            citySlug_name = mcity.find('slug_name').text
            cityTimezone = mcity.find('timezone').text
            cityLanguage = mcity.find('language').text
            print(offer.get('id'))
            print(offer.get('ccode'))
            print(offer.find('title').text)
            print(offer.find('desc').text)
            print(offer.find('highlights').text)
            print(images)
            print(offer.find('price').text)
            print(offer.find('value').text)
            print(offer.find('discount').text)
            print(offer.find('discount_display_type').text)
            print(offer.find('is_hide_sold_quantity').text)
            print(offer.find('is_paperless').text)
            print(offer.find('quantity').text)
            print(offer.find('max_purchase_quantity').text)
            print(offer.find('deal_on_quantity').text)
            print(offer.find('display_weight').text)
            print(offer.find('start_date').text)
            print(offer.find('end_date').text)
            print(offer.find('expiry').text)
            if offer.find('has_child').text==None:
                print('chiren 0')
            else:
                print('1')
            print(offer.find('lock_quantity').text)
            print(offer.find('is_soldout').text)
            print(offer.find('is_deal_on').text)
            print(offer.find('deal_on_at').text)
            print(pName)
            print(pEmail)
            print(pPhone)
            print(pLogo)
            print(Maddress)
            print(Mdescription)

            print(offer.find('redemption_method').text)

