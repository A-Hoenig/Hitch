from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def render_stars(rating):
    # initial valid check
    if rating in [None, '']:
        return mark_safe('<span>Not rated yet</span>')

    # Try converting rating to an integer
    try:
        rating = int(rating)
    except (ValueError, TypeError):
        return mark_safe('<span>Invalid rating</span>')

    # Check if rating is in the correct range
    if not 0 <= rating <= 5:
        return mark_safe('<span>Invalid rating</span>')

    if rating == 0:
        return mark_safe('<span>----</span>')

    star_html = ''
    for i in range(1, 6):
        if i <= rating:
            star_html += '<i class="fa-solid fa-star"></i>'
        else:
            star_html += '<i class="fa-regular fa-star"></i>'
    return mark_safe(star_html)