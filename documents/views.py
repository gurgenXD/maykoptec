from django.shortcuts import render
from django.views import View
from django.http import Http404
from documents.models import Document


class DocumentsView(View):
    def get(self, request, doc_type):
        title = None
        for key, value in Document.DOC_TYPES:
            if key == doc_type:
                title = value
                break

        if not title:
            raise Http404('Страница не найдена')

        documents = Document.objects.filter(doc_type=doc_type)

        context = {
            'title': title,
            'documents': documents,
        }
        return render(request, 'documents/documents.html', context)
