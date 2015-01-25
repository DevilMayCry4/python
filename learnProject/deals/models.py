from django.db import models

# Create your models here.
class cateoryModel(models.Model):
      name = models.CharField(max_length=50)
      slug_name = models.CharField(max_length=60)
      categoryId = models.CharField(max_length=10)

class itemModel(models.Model):
      item_id = models.CharField(max_length=20,null=True, blank=True)
      ccode = models.CharField(max_length=20,null=True, blank=True)
      title = models.TextField(null=True, blank=True)
      short_title = models.TextField(null=True, blank=True)
      desc = models.TextField(null=True, blank=True)
      disclaimer = models.TextField(null=True, blank=True)
      highlights = models.TextField(null=True, blank=True)
      imgs = models.CharField(max_length=2000,null=True, blank=True)
      price = models.CharField(max_length=20,null=True, blank=True)
      value = models.CharField(max_length=20,null=True, blank=True)
      discount = models.CharField(max_length=20,null=True, blank=True)
      discount_display_type = models.CharField(max_length=20,null=True, blank=True)
      is_hide_sold_quantity = models.CharField(max_length=1,null=True, blank=True)
      is_paperless = models.CharField(max_length=1,null=True, blank=True)
      quantity = models.CharField(max_length=10,null=True, blank=True)
      max_purchase_quantity = models.CharField(max_length=10,null=True, blank=True)
      deal_on_quantity = models.CharField(max_length=10,null=True, blank=True)
      display_weight = models.CharField(max_length=10,null=True, blank=True)
      start_date = models.CharField(max_length=30,null=True, blank=True)
      end_date = models.CharField(max_length=30,null=True, blank=True)
      valid_since = models.CharField(max_length=30,null=True, blank=True)
      expiry = models.CharField(max_length=30,null=True, blank=True)
      has_child = models.CharField(max_length=1,null=True, blank=True)
      lock_quantity = models.CharField(max_length=10,null=True, blank=True)
      is_soldout = models.CharField(max_length=1,null=True, blank=True)
      is_deal_on = models.CharField(max_length=1,null=True, blank=True)
      deal_on_at = models.CharField(max_length=30,null=True, blank=True)
      partner_name = models.CharField(max_length=100,null=True, blank=True)
      partner_log = models.CharField(max_length=500,null=True, blank=True)
      partner_email = models.CharField(max_length=100,null=True, blank=True)
      partner_phone = models.CharField(max_length=50,null=True, blank=True)
      address = models.CharField(max_length=500,null=True, blank=True)
      description = models.CharField(max_length=500,null=True, blank=True)
      longitude = models.CharField(max_length=50,null=True, blank=True)
      latitude = models.CharField(max_length=50,null=True, blank=True)
      redemption_method = models.CharField(max_length=50,null=True, blank=True)
      city_id = models.CharField(max_length=50,null=True, blank=True)
      city_name = models.CharField(max_length=50,null=True, blank=True)
      city_slug_name = models.CharField(max_length=50,null=True, blank=True)
      city_timezone = models.CharField(max_length=50,null=True, blank=True)
      city_language = models.CharField(max_length=50,null=True, blank=True)
      payment_method = models.CharField(max_length=50,null=True, blank=True)
      category=models.CharField(max_length=5,null=True, blank=True)

      def getImgs(self):
          img = ''
          for s in self.imgs.split('|'):
              if len(s) > 0:
                  img = img +'<img>'+s+'</img>'+'\n'
          return img
