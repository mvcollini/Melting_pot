from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from .models import Recipe, Category, Follow, SavedRecipe,CustomUser



class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('profile_image',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('profile_image',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Recipe)
admin.site.register(Category)
admin.site.register(Follow)
admin.site.register(SavedRecipe)
