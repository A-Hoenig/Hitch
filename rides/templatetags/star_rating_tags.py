from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def render_stars(rating):
    print(rating)
    if str(rating).isdigit() and 0 <= int(rating) <= 5:
        rating = int(rating)
    else:
        return mark_safe('<span></span>')

    if rating == 0:
        return mark_safe('<span></span>')

    star_html = ''
    for i in range(1, 6):
        if i <= rating:
            star_html += '<i class="fa-solid fa-star"></i>'
        else:
            star_html += '<i class="fa-regular fa-star"></i>'
    return mark_safe(star_html)