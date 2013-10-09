from django import template

register = template.Library()

@register.inclusion_tag('partials/_form_header.html')
def form_header(form):
    return {'form': form}

@register.inclusion_tag('partials/_formset_errors.html')
def formset_errors(formset):
    return {'formset': formset}