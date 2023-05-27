from django.contrib import admin
from .models import Perfume, Brand, Ingredient, Cart
# Register your models here.

@admin.register(Perfume)
class PerfumeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'url_name': ('name',)}
    filter_horizontal = ('ingredients',)


admin.site.register(Brand)

admin.site.register(Ingredient)

admin.site.register(Cart)
