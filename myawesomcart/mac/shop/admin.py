from django.contrib import admin

# Register your models here.
from .models import Product

admin.site.register(Product)

from .models import Contact

admin.site.register(Contact)

from .models import Order

admin.site.register(Order)

from .models import OrderUpdate

admin.site.register(OrderUpdate)

#from .models import OrderUpdateByAwesome

#admin.site.register(OrderUpdateByAwesome)