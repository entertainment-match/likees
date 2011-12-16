# Some custom filters for dictionary lookup.
from django.template.defaultfilters import register
from django.utils.translation import ugettext as _
from django.utils.translation import ungettext
from datetime import datetime
import pytz

@register.filter(name='lookup')
def lookup(dict, index):
    if index in dict:
        return dict[index]
    return ''

@register.filter(name='elapsed')
def elapsed(timestamp):
    dt = datetime.now(pytz.utc) - timestamp
    
    seconds = dt.seconds
    minutes = dt.seconds / 60 
    hours = dt.seconds / 60 / 60 
    days = dt.days
    weeks = dt.days / 7

    if minutes == 0 and hours == 0 and days == 0 and weeks == 0:
        label = ungettext('%(c)s second ago', '%(c)s seconds ago', seconds) % {'c': seconds}
    elif hours == 0 and days == 0 and weeks == 0:
        label = ungettext('%(m)s minute ago', '%(m)s minutes ago', minutes) % {'m': minutes}
    elif days == 0 and weeks == 0:
        label = ungettext('%(h)s hour ago', '%(h)s hours ago', hours) % {'h': hours} 
    elif weeks == 0:
        label = ungettext('%(d)s day ago', '%(d)s days ago', days) % {'d': days} 
    else:
        label = ungettext('%(w)s week ago', '%(w)s weeks ago', weeks) % {'w': weeks} 

    return label

@register.filter
def get_range( value ):
    """
    Filter - returns a list containing range made from given value
    Usage (in template):

    <ul>{% for i in 3|get_range %}
    <li>{{ i }}. Do something</li>
    {% endfor %}</ul>

    Results with the HTML:
    <ul>
    <li>0. Do something</li>
    <li>1. Do something</li>
    <li>2. Do something</li>
    </ul>

    Instead of 3 one may use the variable set in the views
    """
    return range( value )
