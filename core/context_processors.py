from users.forms import BusinessManSignInForm, IndividualSignInForm, EntitySignInForm
from pages.models import Page
from core.models import Index, TitleTag


def context_info(request):
    bs_form = BusinessManSignInForm()
    is_form = IndividualSignInForm()
    es_form = EntitySignInForm()

    seo_titles = TitleTag.objects.filter(url=request.path).first()

    pages = Page.objects.filter(is_active=True)

    try:
        main_phone = Index.objects.first().phone
    except:
        main_phone = ''

    footer_menu = Page.objects.filter(in_footer=True)

    context = {
        'bs_form': bs_form,
        'is_form': is_form,
        'es_form': es_form,
        'seo_titles': seo_titles,
        'pages': pages,
        'main_phone': main_phone,
        'footer_menu': footer_menu,
    }
    return context