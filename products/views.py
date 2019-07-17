from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product
from django.utils import timezone


def home(request):
    products = Product.objects.all
    return render(request, 'products/home.html', {'products':products})


@login_required(login_url='/accounts/signup')
def create(request):

    title = request.POST.get('title')
    body = request.POST.get('body')
    url = request.POST.get('url')
    image = request.FILES.get('image')
    icon = request.FILES.get('icon')

    if request.method=='POST':
        if title and body and url and image and icon:
            product = Product()
            product.title = title
            product.body  = body
            if url.startswith("http://") or url.startswith("https://"):
                product.url = url
            else:
                product.url = "http://" + url
            product.icon = icon
            product.image = image
            product.pub_date = timezone.datetime.now()
            product.votes_total = 1
            product.hunter = request.user
            product.save()
            return redirect('/products/'+ str(product.id))
        else:
            context = 'Hey! All fields are mandatory'
            return render(request, 'products/create.html', {'error':context})
    return render(request, 'products/create.html')


def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products/detail.html', {'product':product})

@login_required(login_url='/accounts/signup')
def upvote(request, product_id):
    if request.method=='POST':
        product = get_object_or_404(Product, pk=product_id)
        product.votes_total += 1
        product.save()
        return redirect('/products/' + str(product.id))
