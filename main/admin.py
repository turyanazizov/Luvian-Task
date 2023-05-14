from django.contrib import admin
from .models import CustomUser, Product

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username','email','is_active']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','mehsul_adi','sekil','qiymet','istehsalci','seriya','emeliyyat_sistemi','sim_kartlarin_sayi']
    list_editable = ['mehsul_adi','sekil','sekil','qiymet','istehsalci','seriya','emeliyyat_sistemi','sim_kartlarin_sayi' ]
