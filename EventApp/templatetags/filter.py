import base64
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def to_base64(image):
    try:
        img_str = base64.b64encode(image.read()).decode('utf-8')
        return mark_safe(f"data:image/jpeg;base64,{img_str}")
    except Exception as e:
        print(f"Error encoding image to Base64: {e}")
        return ""