from django.contrib import admin
from .models import Category, Post, Comment
from django.contrib.auth.models import Group, User


admin.site.register(Post)
admin.site.register(Category)
admin.site.unregister(Group)
admin.site.register(Comment)

#Extend User Model

class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username']

#admin.site.unregister(User)
#admin.site.register(User, UserAdmin)

