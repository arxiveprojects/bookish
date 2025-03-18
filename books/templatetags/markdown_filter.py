# /templatetags/markdown_filter.py
from django import template
import markdown
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='markdown')
def markdown_filter(value):
    return mark_safe(markdown.markdown(
        value,
        extensions=[
            'fenced_code',
            'tables',
            'codehilite',
            'nl2br'
        ],
        extension_configs={
            'codehilite': {
                'linenums': False,
                'use_pygments': False
            }
        }
    ))