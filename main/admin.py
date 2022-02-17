from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.User)


admin.site.register(models.Wishlist)
admin.site.register(models.Custumer)
admin.site.register(models.Cart)
admin.site.register(models.ProductImage)
admin.site.register(models.Brands)
admin.site.register(models.Newsletter)
class OrdersAdmin(admin.ModelAdmin):
    list_display  = ('owner', 'price', 'phone')

class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')

class Product_featureAdmin(admin.ModelAdmin):
    list_display = ('feature', 'product', 'product_feature_value')

admin.site.register(models.Feature)
admin.site.register(models.Product_feature, Product_featureAdmin)
admin.site.register(models.Categories)
admin.site.register(models.Products)
admin.site.register(models.Reviews, ReviewsAdmin)
admin.site.register(models.Orders, OrdersAdmin)

