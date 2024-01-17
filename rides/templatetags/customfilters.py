from django import template
register = template.Library()

@register.filter(expects_localtime=True)
def HMM(td):
    hours = td.seconds // 3600
    minutes = (td.seconds % 3600) // 60
    return '{:01d}:{:02d}'.format(hours, minutes)

@register.filter
def DMY(value):
    return value.strftime('%d.%m.%y')

@register.filter(expects_localtime=True)
def HHMM(value):
    return value.strftime('%H:%M')



