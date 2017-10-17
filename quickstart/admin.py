from django.contrib import admin

# Register your models here.
from models import User

class UserAdmin(admin.ModelAdmin):
  list_display = ('age', 'gender', 'country', 'city', 'imgUrl', 'rank')

admin.site.register(User, UserAdmin)