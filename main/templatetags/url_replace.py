from django import template

register = template.Library()


@register.simple_tag
def url_replace(request, field, value):

    dict_ = request.GET.copy()

    dict_[field] = value

    return dict_.urlencode()

@register.simple_tag
def discount_percent(old, new):
    old = float(old)
    new = float(new)
    percent = round(((1 - new/old)*100), 0)
    return int(percent)

@register.simple_tag
def reviews_percent(all, part):
    all = float(all)
    part = float(part)
    if all == 0:
        return 0
    percent = (part/all)*100
    return int(percent)