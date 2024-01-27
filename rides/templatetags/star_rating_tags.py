from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def render_stars(rating):
    # Check if rating is a valid number
    if rating in [None, '', 'None']:
        return mark_safe('<span>-Not rated-</span>')
    try:
        # Try to convert rating to a float and then round it
        rating_str = str(round(float(rating)))
    except ValueError:
        # rating can't be converted to float
        return mark_safe('<span></span>')

    if rating_str.isdigit() and 0 <= int(rating_str) <= 5:
        rating = int(rating_str)
    else:
        return mark_safe('<span></span>')

    if rating == 0:
        return mark_safe('<span>-Not rated-</span>')

    star_html = ''
    for i in range(1, 6):
        if i <= rating:
            star_html += '<i class="fa-solid fa-star"></i>'
        else:
            star_html += '<i class="fa-regular fa-star"></i>'
    return mark_safe(star_html)