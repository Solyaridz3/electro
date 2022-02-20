from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import uuid



    

class Categories(models.Model):
    name = models.CharField(
        max_length=255, verbose_name='Category', unique=True)
    slug = models.SlugField(max_length=200, verbose_name='Slug', unique=True)
    image = models.ImageField(default='shop02_g7d53q')
    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Brands(models.Model):
    name = models.CharField(max_length=255, verbose_name='Brand', unique=True)
    slug = models.SlugField(max_length=200, verbose_name='Slug', unique=True)
    image = models.ImageField(default='shop02_g7d53q')

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"

    def __str__(self):
        return self.name


class Products(models.Model):
    product_name = models.CharField(
        max_length=255, verbose_name='Product name')
    product_slug = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    product_image = models.ImageField(
        default='image-placeholder_kszdxc', verbose_name='Image')
    creaton_date = models.DateTimeField(auto_now_add=True)
    brand = models.ForeignKey(
        Brands, verbose_name='Brand', on_delete=models.PROTECT)
    price = models.FloatField(verbose_name='Price')
    old_price = models.FloatField(verbose_name='Old Price', null=True, blank=True)
    description = models.TextField(null=True, verbose_name='Description')
    category = models.ForeignKey(
        Categories, on_delete=models.CASCADE, verbose_name='Category')
    rate = models.FloatField(verbose_name='Rate', default=0)
    empty = models.FloatField(verbose_name='Empty', default=5)
    bought_count = models.IntegerField(null=True, default=0)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    @property
    def imageURL(self):
        try:
            url = self.product_image.url
        except:
            url = ''
        return url

    def __str__(self):
        return self.product_name


class Feature(models.Model):
    feature_name = models.CharField(max_length=255, null = False)
    product_type = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True)
    feature_has_value = models.CharField(max_length = 1, null = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.feature_name

class Product_feature(models.Model):
    feature = models.ForeignKey(Feature, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True)
    product_feature_value = models.CharField(max_length=255, null = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return str(self.feature)


class ProductImage(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    image = models.ImageField()
    default = models.BooleanField(default=False)

    def __str__(self):
        return str(self.product)


class HotDeals(models.Model):
    product = models.ForeignKey(Products, on_delete=models.PROTECT)
    discount = models.FloatField(default=10)


class CustomUserManager(BaseUserManager):

    def create_superuser(self, email, username, first_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError("Superuser must be assigned staff to True")

        if other_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must be assigned superuser to True")

        return self.create_user(email, username, first_name, password, **other_fields)

    def create_user(self, email, username, first_name, password, **other_fields):

        if not email:
            raise ValueError("You must provide an email.")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, first_name=first_name,
                          **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(
        max_length=100, null=True, verbose_name="Имя")
    username = models.CharField(
        max_length=50, null=True, verbose_name="Никнейм", unique=True)
    email = models.EmailField(null=True, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'username']

    def __str__(self):
        return self.username


class Wishlist(models.Model):
    wish = models.ForeignKey(Products, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Wish"
        verbose_name_plural = "Wishlist"

    def __str__(self):
        return str(self.wish)


class Custumer(models.Model):
    user = models.OneToOneField(
        User, null=True, on_delete=models.CASCADE, blank=True)
    device = models.CharField(null=True, blank=True, max_length=200)

    def __str__(self):
        if self.user:
            return str(self.user)
        else:
            return self.device


class Cart(models.Model):
    product = models.ManyToManyField(Products)
    owner = models.OneToOneField(Custumer, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Cart-item"
        verbose_name_plural = "Cart"

    def __str__(self):
        return str(self.product)

class Orders(models.Model):
    done = models.BooleanField(default=False)
    payed = models.BooleanField(default=False)
    owner = models.CharField(max_length=200)
    email = models.EmailField()
    price = models.FloatField()
    address = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    city =  models.CharField(max_length=255)
    zip_code = models.CharField(max_length=50)
    phone = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"



class Reviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    rate = models.IntegerField(default=1)
    creation_date = models.DateTimeField(null = True, auto_now_add=True)
    empty_stars = models.IntegerField(null = True)
    text = models.TextField()
    
    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    def __str__(self): 
        return str(self.rate)


class Newsletter(models.Model):
    email = models.EmailField(unique=True)

    class Meta:
        verbose_name = "Email"
        verbose_name_plural = "Newsletter"
    
    def __str__(self): 
        return str(self.email)