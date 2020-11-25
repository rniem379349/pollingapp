from django import template

register = template.Library()

@register.filter(name='setupinputfield')
def setupinputfield(value, arg):
    return value.as_widget(attrs={'class': 'input', 'placeholder': arg})
