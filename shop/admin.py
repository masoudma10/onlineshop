from django.contrib import admin
from .models import Category,Product,SubCategory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','slug')
    prepopulated_fields = {'slug':('name',)}


def make_available(modeladmin, request, queryset):
    queryset.update(available=True)

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name','slug')
    prepopulated_fields = {'slug':('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','image','price','available')
    list_filter = ('available','created','sub_category')
    list_editable = ('price','available')
    prepopulated_fields = {'slug':('name',)}
    raw_id_fields = ('sub_category',)
    actions = (make_available,)