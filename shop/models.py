import uuid
from django.urls import reverse
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)


    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:category',args=[self.slug])



class SubCategory(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='scategory')
    name = models.CharField(max_length=555)
    slug = models.SlugField(max_length=555,unique=True)


    def get_absolute_url(self):
        return reverse('shop:sub_category',args=[self.slug])

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name




class Product(models.Model):

    sub_category = models.ForeignKey(SubCategory,on_delete=models.CASCADE,related_name='products')
    name = models.CharField(max_length=500)
    slug = models.SlugField(max_length=500,unique=True)
    code = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='products/%Y/%m/%d')
    description = models.TextField()
    price = models.DecimalField(max_digits=10,decimal_places=3)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.slug])



