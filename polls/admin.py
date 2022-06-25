from django.contrib import admin

from polls.models import Category, Offer

admin.site.register(Offer)
admin.site.register(Category)