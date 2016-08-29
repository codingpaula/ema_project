from django import template
register = template.Library()

@register.filter(name='add_attrs')
def add_attrs(field, attributes):
    attrs = {}
    definition = attributes.split(',')

    for d in definition:
        if ':' not in d:
            attrs['class'] = d
        else:
            t, v = d.split(':')
            attrs[t] = v

    return field.as_widget(attrs=attrs)
