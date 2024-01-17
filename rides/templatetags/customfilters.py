from django import template
register = template.Library()

@register.filter(expects_localtime=True)
def format_duration(td):
    hours = td.seconds // 3600
    minutes = (td.seconds % 3600) // 60
    return '{:01d}:{:02d}'.format(hours, minutes)