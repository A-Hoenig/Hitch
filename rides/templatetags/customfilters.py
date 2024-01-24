from datetime import datetime, timedelta
from django import template


register = template.Library()

@register.filter(expects_localtime=True)
def HMM(td):
    hours = td.seconds // 3600
    minutes = (td.seconds % 3600) // 60
    return '{:01d}:{:02d}'.format(hours, minutes)

@register.filter(expects_localtime=True)
def HHMM(value):
    return value.strftime('%H:%M')

@register.filter
def DMY(value):
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    if value == today:
        return 'Today'
    elif value == tomorrow:
        return 'Tomorrow'
    else:
        return value.strftime('%d.%b.%y')

@register.filter
def DM(value):
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    if value == today:
        return 'Today'
    elif value == tomorrow:
        return 'Tomorrow'
    else:
        return value.strftime('%d.%b')


@register.filter(name='custom_range')
def custom_range(value):
    return range(value)


