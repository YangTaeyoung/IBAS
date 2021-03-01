import logging
from django import template

register = template.Library()

@register.simple_tag
def test_tag():
   return 'test tag'
