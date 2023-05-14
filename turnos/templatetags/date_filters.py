from django import template
from datetime import date

register = template.Library()

@register.filter(name='fecha_actual')
def is_actual_date(date):
    return date == date.today()