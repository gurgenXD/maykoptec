import os
import re
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template.loader import render_to_string
from django.template import Context
from django.conf import settings


def generate_pdf(context):
    req = context['req']
    dir_name = os.path.join(settings.MEDIA_ROOT, 'requests', 'pdf')
    path = os.path.join(dir_name, '{0}_{1}.pdf'.format(req.id, req.user.user_type))
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    max_power = int(re.sub(r'[^0-9.]+', r'', req.max_power))

    if max_power <= 150:
        if req.user.user_type == 'businessman':
            tmpl_name = 'less150_businessman.html'
        elif req.user.user_type == 'entity':
            tmpl_name = 'less150_entity.html'
        else:
            tmpl_name = 'less150_individual.html'
    else:
        if req.user.user_type == 'businessman':
            tmpl_name = 'more150_businessman.html'
        elif req.user.user_type == 'entity':
            tmpl_name = 'more150_entity.html'
        else:
            tmpl_name = 'more150_individual.html'

    if max_power <= 15 and req.user.user_type == 'individual':
        tmpl_name = 'less15_individual.html'

    with open(path, 'w+b') as resultFile:
        html = render_to_string('pdf/' + tmpl_name, context=context)
        pisaStatus = pisa.CreatePDF(html, dest=resultFile, encoding='UTF-8')

    req.pdf = path
    req.save()

    return pisaStatus.err

