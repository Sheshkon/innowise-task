from django.contrib import admin
from pages.models import Page, Tag, Post


admin.site.register([Page, Tag, Post])
