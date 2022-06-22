from .models import *



class DataMixin:
    def get_user_context(self, request, **kwargs):
        context = kwargs
        categories = Categories.objects.all()
        context['categories'] = categories
        if 'cart_items' not in context:
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
            context['total_price'] = total_price
            context['cart_items'] = cart_items
        
        if 'wishlist' not in context or 'wishlist_slugs' not in context:
            if request.user.is_authenticated:
                wishlist = Wishlist.objects.filter(owner=request.user)
                wishlist_query = wishlist.values_list('wish__product_slug')
                wishlist_slugs = []
                for j in wishlist_query:
                    for i in j:
                        wishlist_slugs.append(i)
            else:
                wishlist = ''
                wishlist_slugs = []
            context['wishlist'] = wishlist
            context['wishlist_slugs'] = wishlist_slugs
       
        return context
   
