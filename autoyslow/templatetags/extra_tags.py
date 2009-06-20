from django import template

register = template.Library()

def lookup(value, arg):
    "Looks up the arg in the value (assuming value is a dictionary)"
    try:
        return value[arg]
    except:
        return ""

register.filter('lookup', lookup)
