from django.contrib import admin
from . models import Product,Variation,ReviewRating,ProductGallery
# Register your models here.
from django.utils.html import format_html
import admin_thumbnails

# we use this library because we want to show the imnage inside the inlines or use the def thumbnail as a alternative way
# @admin_thumbnails.thumbnail('image')
# class ProductGalleryInline(admin.TabularInline):
#     model = ProductGallery
#     extra = 1

class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1

    def thumbnail(self, obj):
        # Return the thumbnail HTML for the image field
        if obj.image:
            return format_html('<img src="{}" width="30" style="border-radius:50%;" />', obj.image.url)
        return "No Image"

    # Use readonly_fields instead of fields to include the method in the form view
    readonly_fields = ('thumbnail',)
    fields = ('thumbnail', 'image') 
    
class ProductAdmin(admin.ModelAdmin):
  
    list_display = ('product_name','price','Category','stock','is_available','modified_date')
    prepopulated_fields = {'slug':('product_name',)}
    inlines = [ProductGalleryInline]
    
class VariationAdmin(admin.ModelAdmin):
    list_display = ('product','variation_category','variation_value','is_active')
    list_editable = ('variation_category','variation_value','is_active')
    list_filter = ('product','variation_category','variation_value')
    

admin.site.register(Product,ProductAdmin)
admin.site.register(Variation,VariationAdmin)
admin.site.register(ReviewRating)
admin.site.register(ProductGallery)