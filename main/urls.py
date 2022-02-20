from django.urls import path
from . import views


urlpatterns = [
    path('', views.homePage, name='home'),
    path('categories/', views.categoriesPage, name='categories'),
    path('categories/<slug:category_slug>/<slug:product_slug>/',
         views.productPage, name='product_detail'),
    path('store/', views.storePage, name='store'),
    path('checkout/', views.checkoutPage, name='checkout'),
    path('wishlist/', views.wishlistPage, name='wishlist'),
    path('add_to_wishlist/<slug:wished_item>/', views.manage_wishlist, name='manage_wishlist'),
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('manage_cart/<slug:cart_slug>/', views.manage_cart, name='manage-cart'),
    path('cart/', views.cart_page, name='cart-page'),
    path('remove_from_wishlist/<slug:cart_slug>/', views.remove_from_cart, name='remove_from_cart'),
    path('create-product/', views.create_product, name='create_product'),
    path('payed/', views.payed, name='payed'),
    path('newsletter_signup/', views.newsletter_signup, name='newsletter_signup'),
    path('send_newsletter/', views.send_newsletter, name='send_newsletter'),
    path('compare/', views.compare, name='compare'),
    path('brands/', views.brands_page, name='brands')
]
