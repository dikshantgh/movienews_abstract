# # template_tags/core_tags/active_user_tag.py
# from django import template
# from core.models import People
# register = template.Library()
#
#
# @register.simple_tag
# def current_user(user):
#     if user.is_authenticated:
#         query = People.objects.get(user_person=user.username)
#         return query.id
#
