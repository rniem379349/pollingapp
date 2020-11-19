from django import template

register = template.Library()

@register.filter(name='setupinputfield')
def setupinputfield(value, arg):
    print(type(value))
    return value.as_widget(attrs={'class': 'input', 'placeholder': arg})
