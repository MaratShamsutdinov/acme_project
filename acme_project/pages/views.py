from typing import Any
from django.views.generic import TemplateView

from birthday import models

# from django.shortcuts import render


# def homepage(request):
#     return render(request, 'pages/index.html')


class HomePage(TemplateView):
    # В атрибуте template_name обязательно указывается имя шаблона,
    # на основе которого будет создана возвращаемая страница.
    template_name = 'pages/index.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        # Получаем словарь контекста из родительского метода.
        context = super().get_context_data(**kwargs)
        # Добавляем в словарь ключ total_count;
        # значение ключа — число объектов модели Birthday.
        context['total_count'] = models.Birthday.objects.count()
        # Возвращаем изменённый словарь контекста.
        return context
