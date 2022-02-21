from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from .models import (Brands, Cart, ProductImage, Product_feature, Feature,
                     Products, Categories, User, Wishlist, Custumer, Reviews, Newsletter)
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .forms import CheckoutForm, MyUserCreationForm
from cloudipsp import Api, Checkout
from django.urls import reverse
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings
from email.mime.image import MIMEImage
from django.core.mail import EmailMultiAlternatives
import os
    


def homePage(request):

    catalog = Products.objects.all()
    categories = Categories.objects.all()
    wishlist = Wishlist.objects.all()

    new = catalog.order_by('-creaton_date')[:6]

    top_selling = catalog.order_by('-bought_count')[:18]

    try:
        user = request.user
        custumer, created = Custumer.objects.get_or_create(user=user)
        cart_items = Cart.objects.filter(owner=custumer)
    except:
        try:
            device = request.COOKIES['device']
            custumer, created = Custumer.objects.get_or_create(device=device)
            cart_items = Cart.objects.filter(owner=custumer)
        except:
            cart_items = []
    total_price = 0
    for p in cart_items:
        for i in p.product.all():
            total_price += i.price
    wishlist_query = wishlist.values_list('wish__product_slug')
    wishlist_slugs = []
    for j in wishlist_query:
        for i in j:
            wishlist_slugs.append(i)
    context = {'catalog': catalog, 'new': new, 'total_price': total_price,
               'categories': categories, 'title': 'Home page', 'page': 'Home', 'wishlist': wishlist,
               'wishlist_slugs': wishlist_slugs,
               'cart_items': cart_items, 'top_selling': top_selling}
    return render(request, 'store/index.html', context)


def productPage(request, category_slug, product_slug):
    categories = Categories.objects.all()
    product = Products.objects.get(product_slug=product_slug)
    product_images = ProductImage.objects.filter(product=product)
    try:
        user = request.user
        custumer, created = Custumer.objects.get_or_create(user=user)
        cart_items = Cart.objects.filter(owner=custumer)
    except:
        try:
            device = request.COOKIES['device']
            custumer, created = Custumer.objects.get_or_create(device=device)
            cart_items = Cart.objects.filter(owner=custumer)
        except:
            cart_items = []
    total_price = 0
    for p in cart_items:
        for i in p.product.all():
            total_price += i.price

    if request.method == 'POST':
        if request.user.is_authenticated:
            text = request.POST.get('text')
            rate = request.POST.get('rating')
            rate = request.POST.get('rating') if request.POST.get(
                'rating') != None else 1
            Reviews.objects.create(
                user=request.user, rate=rate, text=text, product=product, empty_stars=5-int(rate))
            messages.add_message(request, messages.SUCCESS, 'Review added.')
        else:
            messages.add_message(request, messages.WARNING,
                                 'You have to be logged in to leave feedback.')

    reviews = Reviews.objects.filter(
        product=product).order_by('-creation_date')
    avg_score = 0
    for review in reviews:
        avg_score += review.rate
    if reviews.count() > 0:
        avg_score = avg_score / reviews.count()
    empty = (5-round(avg_score))

    ratings = {
        '5': reviews.filter(rate=5),
        '4': reviews.filter(rate=4),
        '3': reviews.filter(rate=3),
        '2': reviews.filter(rate=2),
        '1': reviews.filter(rate=1),
    }

    if request.method == 'POST':
        if request.user.is_authenticated:
            product.rate = round(avg_score, 1)
            product.empty = empty
            product.save()
            return redirect('product_detail', product.category.slug, product.product_slug)

    related = Products.objects.filter(~Q(product_slug=product.product_slug) &
                                      (Q(category__slug__icontains=product.category.slug) |
                                      Q(brand__name__icontains=product.brand.name) |
                                      Q(product_name__icontains=product.product_name) |
                                      Q(description__icontains=product.description)
                                       )).order_by("-bought_count")[:4]

    features = Product_feature.objects.filter(product=product)


    paginator = Paginator(reviews, 3)
    page_number = request.GET.get('reviews')
    page_obj = paginator.get_page(page_number)
    context = {'product': product, 'title': product.product_name, 'real_avg': round(avg_score, 1), 'ratings': ratings, 'related': related,
               'product_images': product_images, 'categories': categories, 'avg_score': round(avg_score), 'empty': empty, 'features':features,
               'cart_items': cart_items, 'total_price': total_price, 'page_obj': page_obj}
    return render(request, 'store/product.html', context)


def categoriesPage(request):
    try:
        user = request.user
        custumer, created = Custumer.objects.get_or_create(user=user)
        cart_items = Cart.objects.filter(owner=custumer)
    except:
        try:
            device = request.COOKIES['device']
            custumer, created = Custumer.objects.get_or_create(device=device)
            cart_items = Cart.objects.filter(owner=custumer)
        except:
            cart_items = []
    categories = Categories.objects.all()
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(owner=request.user)
        wishlist_query = wishlist.values_list('wish__product_slug')
        wishlist_slugs = []
        for j in wishlist_query:
            for i in j:
                wishlist_slugs.append(i)
    else:
        wishlist = ''
    context = {'categories': categories, 'wishlist': wishlist,
               'title': 'Categories', 'cart_items': cart_items}
    return render(request, 'store/categories.html', context)


def storePage(request):

    c_search = request.GET.get('c_search') if request.GET.get(
        'c_search') != None else ''
    search = request.GET.get('search') if request.GET.get(
        'search') != None else ''
    brand = request.GET.get('brand') if request.GET.get(
        'brand') != None else ''
    count = request.GET.get('count') if request.GET.get(
        'count') != None else 15
    min = round(float(request.GET.get('min')),
                0) if request.GET.get('min') != None else 1
    max = round(float(request.GET.get('max')), 0) if request.GET.get(
        'max') != None else 999999
    sort = request.GET.get('sort') if request.GET.get('sort') != None else None

    if max == 9999:
        max = 999999
    all = Products.objects.all()
    products = all.filter(
        Q(brand__slug__icontains=brand) &
        Q(category__slug__icontains=c_search) &
        Q(price__gte=min) &
        Q(price__lte=max) &
        (Q(product_name__icontains=search) |
         Q(description__icontains=search))
    )

    if sort == 'top_price':
        products = products.order_by('-price')
    elif sort == 'low_price':
        products = products.order_by('price')
    else:
        products = products.order_by('-bought_count')

    paginator = Paginator(products, int(count))
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(owner=request.user)
        wishlist_query = wishlist.values_list('wish__product_slug')
        wishlist_slugs = []
        for j in wishlist_query:
            for i in j:
                wishlist_slugs.append(i)
    else:
        wishlist = ''
        wishlist_slugs=[]
    brands = Brands.objects.all()
    top_selling = all.order_by('-bought_count')
    categories = Categories.objects.all()

    try:
        user = request.user
        custumer, created = Custumer.objects.get_or_create(user=user)
        cart_items = Cart.objects.filter(owner=custumer)
    except:
        try:
            device = request.COOKIES['device']
            custumer, created = Custumer.objects.get_or_create(device=device)
            cart_items = Cart.objects.filter(owner=custumer)
        except:
            cart_items = []
    total_price = 0
    for p in cart_items:
        for i in p.product.all():
            total_price += i.price

    context = {'products': products, 'brands': brands, 'wishlist': wishlist, 'wishlist_slugs': wishlist_slugs,
               'categories': categories, 'top_selling': top_selling, 'cart_items': cart_items,
               'page_obj': page_obj, 'title': 'Store', 'total_price': total_price}
    return render(request, 'store/store.html', context)


def checkoutPage(request):
    try:
        user = request.user
        custumer, created = Custumer.objects.get_or_create(user=user)
        cart_items = Cart.objects.filter(owner=custumer)
    except:
        try:
            device = request.COOKIES['device']
            custumer, created = Custumer.objects.get_or_create(device=device)
            cart_items = Cart.objects.filter(owner=custumer)
        except:
            cart_items = []
    total_price = 0
    for p in cart_items:
        for i in p.product.all():
            total_price += i.price

    if request.method == 'POST':
        api = Api(
            merchant_id=1397120,
            secret_key='test',
            response_url=reverse('payed'),
        )
        checkout = Checkout(api=api)
        data = {
            "currency": "USD",
            "amount": int(round(total_price, 2) * 100),
        }
        url = checkout.url(data).get('checkout_url')
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.price = "1000"
            order.save()
            return redirect(url)
    else:
        form = CheckoutForm()
    categories = Categories.objects.all()
    context = {'form': form, 'total_price': total_price, 'categories': categories}
    return render(request, 'store/checkout.html', context)


def payed(request):
    if request.method == 'POST':
        if request.POST.get('response_status') == 'success':
            pass
    return redirect('home')


@login_required(login_url='login')
def wishlistPage(request):
    categories = Categories.objects.all()
    wishlist = Wishlist.objects.filter(owner=request.user)
    try:
        user = request.user
        custumer, created = Custumer.objects.get_or_create(user=user)
        cart_items = Cart.objects.filter(owner=custumer)
    except:
        try:
            device = request.COOKIES['device']
            custumer, created = Custumer.objects.get_or_create(device=device)
            cart_items = Cart.objects.filter(owner=custumer)
        except:
            cart_items = []
    total_price = 0
    for p in cart_items:
        for i in p.product.all():
            total_price += i.price
    context = {'wishlist': wishlist, 'total_price': total_price,
               'categories': categories, 'cart_items': cart_items}
    return render(request, 'store/wishlist.html', context)


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
            print(user)
        except:
            messages.error(request, 'User does not exist.')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist.')

    context = {'page': page}
    return render(request, 'store/login_register.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration.')

    context = {'form': form}
    return render(request, 'store/login_register.html', context)
    


@login_required(login_url='login')
def manage_wishlist(request, wished_item):
    item = get_object_or_404(Products, product_slug=wished_item)
    wished_item, created = Wishlist.objects.get_or_create(
        wish=item, owner=request.user)
    if created:
        messages.success(request, 'The item was added to your wishlist')
    else:
        wished_item.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def manage_cart(request, cart_slug):
    item = get_object_or_404(Products, product_slug=cart_slug)
    try:
        user = request.user
        custumer, customer_created = Custumer.objects.get_or_create(user=user)
    except:
        device = request.COOKIES['device']
        custumer, device_created = Custumer.objects.get_or_create(
            device=device)

    cart_item, created = Cart.objects.get_or_create(owner=custumer)
    cart_item.product.add(item)
    messages.info(request, 'The item was added to your cart')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_from_cart(request, cart_slug):
    item = get_object_or_404(Products, product_slug=cart_slug)
    try:
        user = request.user
        custumer, customer_created = Custumer.objects.get_or_create(user=user)
    except:
        device = request.COOKIES['device']
        custumer, device_created = Custumer.objects.get_or_create(
            device=device)

    cart_item, created = Cart.objects.get_or_create(owner=custumer)
    cart_item.product.remove(item)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cart_page(request):
    try:
        user = request.user
        custumer, created = Custumer.objects.get_or_create(user=user)
        cart_items = Cart.objects.filter(owner=custumer)
    except:
        try:
            device = request.COOKIES['device']
            custumer, created = Custumer.objects.get_or_create(device=device)
            cart_items = Cart.objects.filter(owner=custumer)
        except:
            cart_items = []
    total_price = 0
    for p in cart_items:
        for i in p.product.all():
            total_price += i.price

    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(owner=request.user)
        wishlist_query = wishlist.values_list('wish__product_slug')
        wishlist_slugs = []
        for j in wishlist_query:
            for i in j:
                wishlist_slugs.append(i)
    else:
        wishlist = ''
        wishlist_slugs=[]

    categories = Categories.objects.all()
    context = {'cart_items': cart_items, 'wishlist': wishlist, 'wishlist_slugs': wishlist_slugs,
               'total_price': total_price, 'categories': categories}
    return render(request, 'store/cart.html', context)


def create_product(request):
    if request.user.is_superuser:
        features = Feature.objects.all()
        if request.method == 'POST':
            data = request.POST
            images = request.FILES.getlist('images')
            brand = Brands.objects.get(name=data['brand'])
            category = Categories.objects.get(name=data['category'])
            product = Products.objects.create(
                product_name=data['product-name'],
                brand=brand,
                price=data['price'],
                old_price = data['old-price'] if data['old-price'] != '' else None,
                description=data['desc'],
                category=category,
                product_image=images[0] if len(images)>0 else 'image-placeholder_kszdxc',
            )
            for i in features:
                name = str(i)
                feature_value = data[name] if data[name] != None else None
                if feature_value:
                    Product_feature.objects.create(
                        product = product,
                        feature = i,
                        product_feature_value = feature_value,
                    )
            if len(images) > 0:
                for i in range(1, len(images)):
                    image = ProductImage.objects.create(
                        product=product,
                        image=images[i]
                    )
        categories = Categories.objects.all()
        brands = Brands.objects.all()
        context = {'categories': categories, 'brands': brands, 'features': features}
        return render(request, 'store/create_product.html', context)
    else:
        return HttpResponse("You are not allowed here")


def newsletter_signup(request):

    if request.method == 'POST':
        try:
            mail_address = request.POST.get('mail')
            send_mail(
                'Signing up on the out newsletter',
                'You successfully signed up on the newsletter.',
                settings.DEFAULT_FROM_EMAIL,
                [mail_address],
                fail_silently=False,
            )
            emails = Newsletter.objects.all()
            emails.create(email=mail_address)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        except:
            messages.add_message(request, messages.WARNING,
                                 'Wrong email address or it is already added.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def send_newsletter(request):
    if request.method == 'POST':
        theme = request.POST.get('theme') if request.POST.get(
            'theme') != None else 'Not assigned'
        text = request.POST.get('text') if request.POST.get(
            'text') != None else 'Not assigned'
        images = request.FILES.getlist(
            'images') if request.FILES.getlist('images') != None else []
        emails_queryset = Newsletter.objects.all().values_list('email', flat=True)
        emails = []
        images_names = []
        for i in images:
            images_names.append(i.name)
        body_html = '''
            <html>
                <body>
                {% for image in images_names %}
                    <img src="cid:logo.png" />
                {% endfor %}
                </body>
            </html>
        '''
        for email in emails_queryset:
            emails.append(email)

        msg = EmailMultiAlternatives(theme, text,
                                     settings.DEFAULT_FROM_EMAIL, emails)

        msg.attach_alternative(body_html, "text/html")
        msg.mixed_subtype = 'related'
        img_dir = 'static/img/uploaded'

        print(images_names)
        for f in images_names:
            fp = open(os.path.join(os.path.join(img_dir), f), 'rb')
            msg_img = MIMEImage(fp.read())
            fp.close()
            msg_img.add_header('Content-ID', '<{}>'.format(f))
            msg.attach(msg_img)

        msg.send()
        return redirect('store')
        # msg = EmailMultiAlternatives(
        #     theme,
        #     text,
        #     settings.DEFAULT_FROM_EMAIL,
        #     emails,
        #     # fail_silently=False,
        # )
        # msg.mixed_subtype = 'related'
        # msg.attach_alternative(body_html, "text/html")
        # img_dir = 'static/img'
        # image = 'handy.png'
        # file_path = os.path.join(img_dir, image)
        # with open(file_path, 'r', encoding='utf-8',errors='ignore') as f:
        #     img = MIMEImage(f.read())
        #     img.add_header('Content-ID', '<{name}>'.format(name=image).decode('utf-8'))
        #     img.add_header('Content-Disposition', 'inline', filename=image)
        # msg.attach(img)
    return render(request, 'store/send_newsletter.html')


def compare(request):
    product_slug = request.GET.get('choosen') if request.GET.get('choosen') != None else None
    all_products = Products.objects.all()
    if product_slug != None:
        choosen = Products.objects.get(product_slug=product_slug)
        category_filter = all_products.filter(category=choosen.category)
        features = Product_feature.objects.filter(product=choosen)
        opposite_slug = request.GET.get('opposite') if request.GET.get('opposite') != None else None
        if opposite_slug != None:
            opposite = all_products.get(product_slug=opposite_slug)
            opposite_features = Product_feature.objects.filter(product=opposite)
        else:
            opposite, opposite_features = None, None
    else:
        category_filter = []
        features = []
        choosen = None
        opposite, opposite_features = None, []
    categories = Categories.objects.all()
    context = {'category_filter':category_filter, 'features': features, 'all_products': all_products, 'title': "Compare",
                'opposite_features': opposite_features, 'opposite': opposite, 'choosen': choosen, 'categories': categories}
    return render(request, 'store/compare.html', context)


def brands_page(request):
    brands = Brands.objects.all()
    categories = Categories.objects.all()
    context = {'brands': brands, 'categories': categories}
    return render(request, 'store/brands.html', context)