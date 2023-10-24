from django.db import models
from django.utils.timezone import timezone
#python manage.py migrate --run-syncdb

# Create your models here.
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=300)
    pub_date = models.DateField()
    image = models.ImageField(upload_to="shop/images", default="")

    def __int__(self):
        return self.product_name


class Contact(models.Model):
    Name = models.CharField(max_length=56)
    Email = models.EmailField(max_length=56)
    Phone = models.IntegerField()
    Desc = models.CharField(max_length=300)

    def __str__(self):
        return self.Name


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    Item_json = models.CharField(max_length=5000, default="")
    Amount = models.IntegerField()
    Name = models.CharField(max_length=30)
    Email = models.EmailField()
    Address = models.CharField(max_length=80)
    Address2 = models.CharField(max_length=100)
    City = models.CharField(max_length=30)
    State = models.CharField(max_length=30)
    Zip_code = models.CharField(max_length=25)
    Phone_number = models.CharField(max_length=13)

    def __str__(self):
        return self.Name


class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)
    update_desc1 = models.CharField(max_length=5000)
    timestamp1 = models.DateField(null=True, blank=True, default="2000-12-01")
    update_desc2 = models.CharField(max_length=5000)
    timestamp2 = models.DateField(null=True, blank=True, default="2000-12-01")
    update_desc3 = models.CharField(max_length=5000)
    timestamp3 = models.DateField(null=True, blank=True, default="2000-12-01")

    def __str__(self):
        return self.update_desc[0:7] + "..."
