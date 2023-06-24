from django import template


register = template.Library()


@register.filter
def ru_pluralize(value: int, variants: str) -> str:
    """Фильтр окончаний кириллицы."""
    default = ""
    if not variants:
        return default

    variants = variants.split(",")
    value = abs(int(value))
    if value % 10 == 1 and value % 100 != 11:
        variant = 0
    elif 2 <= value % 10 <= 4 and (value % 100 < 10 or value % 100 >= 20):
        variant = 1
    else:
        variant = 2

    try:
        return variants[variant]
    except IndexError:
        return default
