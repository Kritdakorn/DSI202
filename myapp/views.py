
from dataclasses import dataclass
from statistics import median
from django.shortcuts import render, redirect
from myapp.models import *
from django.views.generic.edit import CreateView
from django.views.generic import ListView, View, FormView
from django.urls import reverse
from django.contrib.auth.models import User
from myapp.forms import *
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, redirect
import json
import random

class Create_product(CreateView):
    model = Product_list
    template_name = 'image_create.html'
    fields = ['image', 'name', 'description', 'type_product', 'price']

    def get_success_url(self):
        return reverse('home')


class Home(ListView):
    model = Product_list
    template_name = 'home.html'


class Promotions(ListView):
    model = Product_list
    template_name = 'promotions.html'

def transactionview(request):
    user = request.user.customer
    transaction = Transaction.objects.filter(customer=user)
    title_image = []
    for i in transaction:
        title_image.append(Order.objects.filter(transaction=i)[0])
    
    transaction = zip(transaction, title_image)
    context = {
        "items": transaction
    }
    return render(request, 'transaction.html', context)

def detail_transaction(request, tran):
    user = request.user.customer
    tran = Transaction.objects.get(transaction=tran)
    list_product = Order.objects.filter(transaction_id=tran)
    total_price = []
    for i in list_product:
        total_price.append(i.quantity * i.product.price)
    print(total_price)
    list_product = zip(list_product ,total_price)
    context = {
        "items": list_product
    }
    return render(request, "list_order.html", context)

def type_view(request):
    soft = Product_list.objects.filter(type_product='low')
    medium = Product_list.objects.filter(type_product='medium')
    hight = Product_list.objects.filter(type_product='hight')
    print(soft)
    context = {
        'soft': soft,
        "medium": medium,
        "hight": hight
    }
    return render(request, 'type.html', context)

def cart (request):
    list_item = []
    info_item = [[],[]]
    hash = (random.getrandbits(128))
    transaction = ("%010x" % hash)
    form = Createtransaction(request.POST or None)

    if request.method == 'POST':
        form = Createtransaction(request.POST, request.FILE)
        if form.is_valid():
            form.save
    try:
        data = json.loads(request.COOKIES.get('cart'))['data']

        for d in data:
            print(d['name'],'D')
            list_item.append(d['name'])
            info_item[0].append((d['total_price']))
            info_item[1].append(d['quantity'])
            
    except:
        data = []
    print(list_item,':D')
    print(info_item,'info')
    print(data)
    # items = Product_list.objects.filter(name__in = list_item)
    items = list(map(lambda name: Product_list.objects.get(name=name), list_item))

    print(items,':D')
    items = zip(items, info_item[0], info_item[1])
    context = {
        'items': items, 
        'total': info_item[0],
        'price_total': sum(info_item[0]),
        "mobile":"0863624849",
        "amount": float(sum(info_item[0])),
        "form":form}
    return render(request, 'cart.html', context)

def createTransaction (request):
    data = json.loads(request.COOKIES.get('cart'))['data']
    customer = request.user.customer
    hash = (random.getrandbits(128))
    transaction = ("%010x" % hash)[0:20]
    print(transaction)
    print(customer)
    total_price = 0
    transac, created = Transaction.objects.get_or_create(
    customer=customer, transaction=transaction,
    stats=0)
    transaction = Transaction.objects.get(transaction = transaction)
    for i in data:
        product = Product_list.objects.get(name=i['name'])
        Order.objects.create(transaction=transaction, product=product,
        quantity=i['quantity'])
        total_price += i['total_price']
    transac.total = total_price
    transac.save()

    dictionary = {"data": []}
    json_object = json.dumps(dictionary, indent = 4)
    print(json_object)
    response = redirect('transaction')
    response.set_cookie('cart', json_object)
    return response


class Report(CreateView):
    template_name = 'help.html'
    form_class = Report_Problem
    success_url = reverse_lazy('home')


    def get_success_url(self):
        return reverse('home')


def profile(request):
    try:
        instance = get_object_or_404(customer, user=request.user)
        form = ProfileForm(request.POST or None, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            context = {
                'form': form,
                'user': request.user
            }
            return render(request, 'profile.html', context)
    except:
        return redirect('createprofile')

class customerlogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')


def product_detail(request, pk):
    photo = Product_list.objects.get(id=pk)
    print(photo,':D')
    recom = Product_list.objects.all()
    return render(request, 'product_detail.html', {'photo': photo, "rec":recom[0:4]})


data = []
def add_to_cart(request):
    global data
    try:
        data = json.loads(request.COOKIES.get('cart'))['data']
    except:
        pass
    print(data)
    name = request.POST.get("name", "")
    price = int(request.POST.get("price", ""))
    myitem={
        "name": name,
        "price": price,
        "total_price": price,
        "quantity": 1
        }
    
    for num, d in enumerate(data):
        if (d['name'] == name):
            data[num]['quantity'] += 1
            data[num]['total_price'] += price
            break
    else:
        data += [myitem,]
    dictionary = {"data": data}
    json_object = json.dumps(dictionary, indent = 4)
    print(json_object)
    response = redirect('home')
    response.set_cookie('cart', json_object)
    return response

def add_cart(request):
    global data
    try:
        data = json.loads(request.COOKIES.get('cart'))['data']
    except:
        pass
    print(data)
    name = request.POST.get("name", "")
    price = int(request.POST.get("price", ""))
    myitem={
        "name": name,
        "price": price,
        "total_price": price,
        "quantity": 1
        }
    
    print(myitem, 'check add\n\n')
    for num, d in enumerate(data):
        if (d['name'] == name):
            data[num]['quantity'] += 1
            data[num]['total_price'] += price
            break
    else:
        data += [myitem,]
    dictionary = {"data": data}
    json_object = json.dumps(dictionary, indent = 4)
    print(json_object)
    response = redirect('cart')
    response.set_cookie('cart', json_object)
    return response

def remove_cart(request):
    global data
    try:
        data = json.loads(request.COOKIES.get('cart'))['data']
    except:
        pass
    print(data)
    name = request.POST.get("name", "")
    price = int(request.POST.get("price", ""))
    myitem={
        "name": name,
        "price": price,
        "total_price": price,
        "quantity": 1
        }
    
    for num, d in enumerate(data):
        if (d['quantity'] == 1):
            del data[num]
            break
        elif (d['name'] == name):
            data[num]['quantity'] -= 1
            data[num]['total_price'] -= price
            break
    else:
        data += [myitem,]
    dictionary = {"data": data}
    json_object = json.dumps(dictionary, indent = 4)
    print(json_object)
    response = redirect('cart')
    response.set_cookie('cart', json_object)
    return response
 

class customerloginView(FormView):
    template_name = 'login.html'
    form_class = customerloginForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data["password"]
        usr = authenticate(username=username, password=password)
        if usr is not None and customer.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid credentials"})
        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url


class CreateProfile(CreateView):
    template_name = 'profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('home')

class customerregistrationView(CreateView):
    template_name = 'register.html'
    form_class = customerregistrationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        email = form.cleaned_data.get('email')
        user = User.objects.create_user(username, email, password)
        form.instance.user = user
        login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('home')


from django.http import HttpResponse
from PIL import Image
import libscrc
import qrcode


def calculate_crc(code):
    crc = libscrc.ccitt_false(str.encode(code))
    crc = str(hex(crc))
    crc = crc[2:].upper()
    return crc.rjust(4, '0')

def gen_code(mobile="", nid="", amount=1.23):
    code="00020101021153037645802TH29370016A000000677010111"
    if mobile:
        tag,value = 1,"0066"+mobile[1:]
        seller='{:02d}{:02d}{}'.format(tag,len(value), value)
    elif nid:
        tag,value = 2,nid
        seller='{:02d}{:02d}{}'.format(tag,len(value), value)
    else:
        raise Exception("Error: gen_code() does not get seller mandatory details")
    code+=seller
    tag,value = 54, '{:.2f}'.format(amount)
    code+='{:02d}{:02d}{}'.format(tag,len(value), value)
    code+='6304'
    code+=calculate_crc(code)
    return code

def get_qr(request,mobile="",nid="",amount=""):
    message="mobile: %s, nid: %s, amount: %s"%(mobile,nid,amount)
    print( message )
    code=gen_code(mobile=mobile, amount=float(amount))#scb
    print(code)
    img = qrcode.make(code,box_size=4)
    response = HttpResponse(content_type='image/png')
    img.save(response, "PNG")
    return response

def checkout(request):
    context={
        "mobile":"0863624849", #seller's mobile
        "amount": 0.1
    }
    return render(request, 'checkout.html', context)