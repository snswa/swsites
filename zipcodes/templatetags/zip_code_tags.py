import re
from django.core.exceptions import ObjectDoesNotExist
from django.template import Library, Node, Variable
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from zipcodes.models import ZipCode


register = Library()


@register.tag
def zip_code_object(parser, token):
    # Split token and process 'as' if it exists.
    split = token.split_contents()
    as_index = None
    context_var = None
    for i, bit in enumerate(split):
        if bit == 'as':
            as_index = i
            break
    if as_index is not None:
        try:
            context_var = split[as_index + 1]
        except IndexError:
            raise template.TemplateSyntaxError('Context variable assignment '
                'must take the form of {% {0!r} zip_code_string as '
                'context_var_name %}'.format(split[0]))
        del split[as_index:as_index + 2]
    if len(split) == 2:
        return ZipCodeObjectNode(split[1], context_var=context_var)
    else:
        raise template.TemplateSyntaxError('{0!r} takes one required '
            'argument and one optional argument'.format(split[0]))


class ZipCodeObjectNode(Node):

    def __init__(self, zip_code_var, context_var=None):
        self.zip_code_var = Variable(zip_code_var)
        self.context_var = context_var

    def render(self, context):
        key = self.zip_code_var.var
        zip_code_string = self.zip_code_var.resolve(context)
        try:
            zip_code = ZipCode.objects.get(zip_code=zip_code_string)
        except ZipCode.DoesNotExist:
            zip_code = None
        context_var = self.context_var or key
        context[context_var] = zip_code
        return u''
