from django import template
register = template.Library()


def replace_str_end_to_br(value):
    return value.replace('\n', '<br>')


register.filter('replace_str_end_to_br', replace_str_end_to_br)
