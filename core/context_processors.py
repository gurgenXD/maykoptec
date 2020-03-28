from pages.models import Page
from math import ceil
from contacts.models import Social, Address, Phone


def context_info(request):
    pages = Page.objects.filter(is_active=True, parent=None)
    footer_pages = Page.objects.filter(in_footer=True)
    main_phones = Phone.objects.all()[:2]
    address = Address.objects.first()

    per_group = ceil(len(footer_pages) / 3)
    socials = Social.objects.all()

    first_group = footer_pages[:per_group]
    second_group = footer_pages[per_group:per_group*2]
    third_group = footer_pages[per_group*2:]

    is_lo = request.session.get('is_lo')

    context = {
        'pages': pages,
        'first_group': first_group,
        'second_group': second_group,
        'third_group': third_group,
        'socials': socials,
        'main_phones': main_phones,
        'address': address,
        'footer_pages': footer_pages,
        'is_lo': is_lo,
    }
    return context