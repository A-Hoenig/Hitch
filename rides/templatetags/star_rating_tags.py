from django import template

register = template.Library()


@register.simple_tag
def render_stars(rating):
    if rating == 0:
        return '<span>Not rated yet</span>'

    star_html = ''
    for i in range(1, 6):
        if i <= rating:
            star_html += '<i class="fa-solid fa-star"></i>'
        else:
            star_html += '<i class="fa-regular fa-star"></i>'
    return star_html