# from django.contrib import admin
#
# from core.models import People
#
#
# class PeopleAdmin(admin.ModelAdmin):
#     list_display = ('user_person', 'country', 'dob', 'favourite_actor',)
#     search_fields = ('user_person__username',)
#
#
# admin.site.register(People, PeopleAdmin)
from django.contrib import admin
from django.contrib.admin import TabularInline
from taggit.models import Tag

from core.models import Creator, Post


class CustomPost(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",), }


admin.site.register(Creator)
admin.site.register(Post, CustomPost)
