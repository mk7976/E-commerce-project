from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("about/", views.about, name='About Us'),
    path("tracker/", views.tracker, name='Traking status'),
    path("trackOrder/", views.trackOrder, name='track'),
    path("contect/", views.contact, name='contact'),
    # path("contects/", views.contactsubmit, name='contactsubmit'),
    path("products/<int:myid>", views.productView, name="ProductView"),
    path("checkout/", views.checkout, name='checkout'),
    path("checkorderplace/", views.checkoutOrderpalce, name='checkoutplace'),
    path("handlerequest/", views.Handlerequest, name="handlerequest"),
    path("search/", views.Search, name="Search"),

]
