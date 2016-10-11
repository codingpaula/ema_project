from django import template

register = template.Library()

"""
kann genutzt werden durch:
{{ objekt|add_attrs:"attribute,placeholder:'username'" }}
"""
# fuer die Nutzung in Templates registrieren
@register.filter(name='add_attrs')
def add_attrs(field, attributes):
    attrs = {}
    definition = attributes.split(',')
    # alle uebergebenen attribute durchgehen
    for d in definition:
        if ':' not in d:
            attrs['class'] = d
        else:
            t, v = d.split(':')
            attrs[t] = v

    return field.as_widget(attrs=attrs)
