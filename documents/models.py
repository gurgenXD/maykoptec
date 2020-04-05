from django.db import models
from uuid import uuid1


class Document(models.Model):
    DOC_TYPES = [
        ('regulations', 'Нормативные документы'),
        ('info_disclosure', 'Раскрытие информации'),
        ('purchase', 'Закупки'),
    ]
    doc_type = models.CharField('Где отображать', max_length=250, choices=DOC_TYPES, blank=True, null=True)
    name = models.TextField(verbose_name='Название документа')

    def get_document_url(self, filename):
        ext = filename.split('.')[-1]
        filename = '{0}.{1}'.format(uuid1(), ext)
        return 'documents/{0}/{1}'.format(self.doc_type, filename)

    document = models.FileField(upload_to=get_document_url, max_length=500, verbose_name='Файл')

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'

    def __str__(self):
        return self.name