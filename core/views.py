from django.shortcuts import render, redirect
from django.views import View
# from directions.models import Direction
# from news.models import News
# from feedback.forms import FeedBackForm
# from core.models import Index


class IndexView(View):
    def get(self, request):
        # directions = Direction.objects.filter(is_active=True)[:3]
        # news = News.objects.filter(is_active=True)[:5]
        # feedback_form = FeedBackForm()
        # index = Index.objects.first()

        context = {
            # 'directions': directions,
            # 'news': news,
            # 'feedback_form': feedback_form,
            # 'index': index,
        }
        return render(request, 'core/index.html', context)


# class ChangeView(View):
#     def get(self, request):
#         is_lo = request.session.get('is_lo')

#         request.session['is_lo'] = True if not is_lo else False

#         return redirect('index')
