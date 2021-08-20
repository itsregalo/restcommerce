from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from accounts.models import MerchantUser, CustomerUser
from PIL import Image
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.conf import settings
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager
User = settings.AUTH_USER_MODEL

#implementing categories
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.
class Category(MPTTModel):
    title=models.CharField(max_length=255)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    slug=models.SlugField(blank=True)
    thumbnail = models.ImageField(upload_to="images/products/categories/")
    description=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    is_active = models.IntegerField(default=1)
    
    def get_absolute_url(self):
        return reverse("products:category-objects", kwargs = {'slug':self.slug})
    
    def category_objects(self):
        return Product.objects.filter(is_approved=True, category=self)
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
    
    class MPTTMeta:
        order_insertion_by = ['title']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.title)
        return super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class Product(models.Model):
    slug=models.SlugField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_name=models.CharField(max_length=255)
    image = models.ImageField(upload_to="images/products/main")
    image_thumbnail = ImageSpecField(source='image',
                                   processors = [ResizeToFill(300,300)],
                                   format='JPEG',
                                   options = {'quality':100})
    brand=models.CharField(max_length=255)
    product_max_price=models.CharField(max_length=255)
    product_discount_price=models.CharField(max_length=255)
    product_description=models.TextField(blank=True, null=True)
    product_long_description=RichTextField(blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    tags = TaggableManager()
    added_by_merchant=models.ForeignKey(MerchantUser,on_delete=models.CASCADE)
    in_stock_total=models.IntegerField(default=1)
    is_approved = models.BooleanField(default=False)
    view_count = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
    
    def get_merchant_products(self):
        return Product.objects.filter(added_by_merchant=MerchantUser)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.product_name)
        return super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("products:product-detail", kwargs={"slug": self.slug})
    
    def add_to_wishlist(self):
        return reverse("products:add-to-wishlist", kwargs={"slug":self.slug})
    
    def __str__(self):
        return self.product_name


class ProductMedia(models.Model):
    product_id=models.ForeignKey(Product,on_delete=models.CASCADE)
    description = models.CharField(max_length=70)
    image =models.ImageField(upload_to="images/products/product_media")
    image_thumbnail = ImageSpecField(source='image',
                                     processors=[ResizeToFill(655,800)],
                                     format='webp',
                                     options = {'quality':100})
    created_at=models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    is_ordered = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} - {self.product.product_name}"
    
    def totalQuantityPrice(self):
        return self.quantity * int(self.product.product_discount_price)

class CustomerOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    is_ordered = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username
    
    def totalorderPrice(self):
        total=0
        for product in self.products.all():
            total += int(product.totalQuantityPrice())
        return total
    
