from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product
from .models import Contact
from .models import Order
from math import ceil
from .models import OrderUpdate
from django.views.decorators.csrf import csrf_exempt
# import  logging library
import logging
from paytmchecksum import PaytmChecksum

MERCHANT_KEY = "kbzk1DSbJiV_03p5";

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


def index(request):
    # products = Product.objects.all()
    # print(products)
    # n = len(products)
    # nSlides = n//4 + ceil((n/4)-(n//4))

    allProds = []
    catprods = Product.objects.values('category', 'product_id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    # params = {'no_of_slides':nSlides, 'range': range(1,nSlides),'product': products}
    # allProds = [[products, range(1, nSlides), nSlides],
    #             [products, range(1, nSlides), nSlides]]
    params = {'allProds': allProds}
    a = Product.objects.all().count()
    # print(a)

    return render(request, 'shop/index.html', {'allProds': allProds, "lan": a})


def productView(request, myid):
    product = Product.objects.filter(product_id=myid)
    prod = Product.objects.all().count()
    # print(myid)
    # print(product)
    return render(request, "shop/prodView.html", {"prodid": product, "totalprod": prod})


def about(request):
    return render(request, 'shop/About.html')


def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        desc = request.POST['desc']
        f = Contact(Name=name, Email=email, Phone=phone, Desc=desc)
        f.save()
        Thank = True
        return render(request, 'shop/contact.html', {"thank": Thank})
    return render(request, 'shop/contact.html')


def tracker(request):
    return render(request, "shop/tracker.html")


def trackOrder(request):
    if request.method == "POST":
        orderId = request.POST['orderId']
        email = request.POST['email']
        track = OrderUpdate.objects.filter(order_id=orderId)
        if len(track) > 0:
            track1 = OrderUpdate.objects.get(order_id=orderId)
            Trackorderdetail = Order.objects.get(order_id=orderId)
            a = Trackorderdetail.Item_json
            productname = ""
            product = []

            for i in a:

                if i != ",":
                    productname = productname + i

                if i == ",":
                    product.append(productname)

            s = a.replace(",", "")
            product.append(s)
            # print(product)
            l = len(product)
            p = []
            p.append(product[0])
            for products in product:
                for i in range(0, len(product)):
                    d = product[i + 1].removeprefix(product[i])
                    # print(d)
                    p.append(d)
                    # print(i)

                    if (i == (l - 2)):
                        break

                        # print(p)
            productlist = []
            for product in p:
                if product not in productlist:
                    productlist.append(product)
            # print(productlist)
            proddict = {}
            for product in productlist:
                for i in range(0, len(product) - 1):
                    if product[i] == "-":
                        proddict[product[0:i]] = product[i + 1:]
            print(proddict)

            text = track1.update_desc
            time = track1.timestamp
            text1 = track1.update_desc1
            time1 = track1.timestamp1
            text2 = track1.update_desc2
            time2 = track1.timestamp2
            text3 = track1.update_desc3
            time3 = track1.timestamp3

        return render(request, "shop/tracker.html",
                      {"text": text, "time": time, "text1": text1, "time1": time1, "text2": text2, "time2": time2,
                       "text3": text3, "time3": time3,
                       "Trackorderdetails": proddict})

    else:
        return render(request, "shop/tracker.html", {
            "text11": "Sorry, We are not able to fetch this order id and email. Make sure to type correct order Id and email"})

    return render(request, "shop/tracker.html")


def search(request):
    return HttpResponse("We are at search")


def checkout(request):
    return render(request, "shop/checkout.html")


def checkoutOrderpalce(request):
    if request.method == "POST":
        item_json = request.POST['item_json']
        amount = request.POST['amount']
        name = request.POST['name']
        email = request.POST['email']
        address = request.POST['address']
        address2 = request.POST['address2']
        city = request.POST['city']
        state = request.POST['state']
        zip = request.POST['zip']
        phone_number = request.POST['phone_number']
        order = Order(Item_json=item_json, Amount=amount, Name=name, Email=email, Address=address, Address2=address2,
                      City=city,
                      State=state, Zip_code=zip,
                      Phone_number=phone_number)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True

        id = order.order_id
        param_dict = {

            'MID': 'WorldP64425807474247',
            'ORDER_ID': str(order.order_id),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/shop/handlerequest/',
        }
        param_dict['CHECKSUMHASH'] = PaytmChecksum.calculateChecksum(param_dict, MERCHANT_KEY, salt="2334343")
        print(param_dict)
        return render(request, 'shop/paytm.html', {"param_dict": param_dict})
        # return render(request, 'shop/tracker.html', {"op": update.update_desc, 'id': "Your order-id is " + str(id)})
        # request paytm to transfer the amount to your account after payment by user

    return render(request, "shop/checkout.html")


# paytm  will send post request
@csrf_exempt
def Handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]
            verify = PaytmChecksum.verifySignatureByString(response_dict, MERCHANT_KEY, checksum)
            if verify:
                if response_dict['RESPCODE'] == '01':
                    print('order successful')
                else:
                    print('order was not successful because' + response_dict['RESPMSG'])

    return render(request, 'shop/paymentstatus.html', {'response': response_dict})


def Search(request):
    if request.method == "POST":
        Search_name = request.POST["search"]
        listofSearch_result = Product.objects.filter(product_name=Search_name)
        if len(listofSearch_result) == 0:
            print("AAA:", "Not Found")
        else:
            print(listofSearch_result)
        # print(Search_result.product_name)
        # print(Search_result.price)
        # print(type(Search_result))
    return render(request, "shop/prodview.html", {"prodid": listofSearch_result})
