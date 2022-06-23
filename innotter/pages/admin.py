from django.contrib import admin
from pages.models import Page, Tag, Post, Like


admin.site.register((Page, Tag, Post, Like))
