# from django.core.paginator import Paginator
# from django.shortcuts import get_object_or_404, redirect, render
# from django.http import
# from django.contrib.auth.decorators import login_required


from django.shortcuts import get_object_or_404

from django.urls import reverse

from django.contrib.auth.mixins import UserPassesTestMixin

from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CongratulationForm


from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from django.urls import reverse_lazy


from . import forms, models, utils


class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class BirthdayListView(ListView):
    # Указываем модель, с которой работает CBV...
    model = models.Birthday
    # По умолчанию этот класс
    # выполняет запрос queryset = Birthday.objects.all(),
    # но мы его переопределим:
    queryset = models.Birthday.objects.prefetch_related(
        'tags',
    ).select_related(
        'author',
    )
    # ...сортировку, которая будет применена при выводе списка объектов:
    ordering = ['birthday']
    # ...и даже настройки пагинации:
    paginate_by = 4


class BirthdayCreateView(LoginRequiredMixin, CreateView):

    # Указываем модель, с которой работает CBV...
    model = models.Birthday
    # Указываем имя формы:
    form_class = forms.BirthdayForm

    def form_valid(self, form):
        # Присвоить полю author объект пользователя из запроса.
        form.instance.author = self.request.user
        # Вызываем обязательный метод form_valid,
        # который вернет форму, если она валидна.
        return super().form_valid(form)


class BirthdayUpdateView(OnlyAuthorMixin, LoginRequiredMixin, UpdateView):

    model = models.Birthday
    form_class = forms.BirthdayForm


class BirthdayDetailView(DetailView):
    model = models.Birthday

    def get_context_data(self, **kwargs):
        # Получаем словарь контекста:
        context = super().get_context_data(**kwargs)
        # Добавляем в словарь новый ключ:
        # ключ 'birthday_countdown' и содержимое - дни до дня рождения.
        context['birthday_countdown'] = utils.calculate_birthday_countdown(
            # Дату рождения берём из объекта в словаре context:
            self.object.birthday
        )
        # Записываем в переменную form пустой объект формы.
        context['form'] = CongratulationForm()
        # Запрашиваем все поздравления для выбранного дня рождения.
        context['congratulations'] = (
            # Дополнительно подгружаем авторов комментариев,
            # чтобы избежать множества запросов к БД.
            self.object.congratulations.select_related('author')
        )
        # Возвращаем словарь контекста.
        return context


class BirthdayDeleteView(OnlyAuthorMixin, LoginRequiredMixin, DeleteView):
    model = models.Birthday
    success_url = reverse_lazy('birthday:list')


class CongratulationCreateView(LoginRequiredMixin, CreateView):
    birthday = None
    model = models.Congratulation
    form_class = CongratulationForm

    # Переопределяем dispatch()
    def dispatch(self, request, *args, **kwargs):
        self.birthday = get_object_or_404(models.Birthday, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    # Переопределяем form_valid()
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.birthday = self.birthday
        return super().form_valid(form)

    # Переопределяем get_success_url()
    def get_success_url(self):
        return reverse(
            'birthday:detail',
            kwargs={'pk': self.birthday.pk},
        )


# @login_required
# def simple_view(request):
#     return HttpResponse('Страница для залогиненных пользователей!')

# def birthday(request, pk=None):
#     if pk is not None:
#         instance = get_object_or_404(models.Birthday, pk=pk)
#     else:
#         instance = None
#     form = forms.BirthdayForm(
#         request.POST or None,
#         request.FILES or None,
#         instance=instance)
#     context = {'form': form}
#     if form.is_valid():
#         form.save()  # Сохраняем данные в базу данных
#         birthday_countdown = utils.calculate_birthday_countdown(
#             form.cleaned_data['birthday']
#         )
#         context.update({'birthday_countdown': birthday_countdown})
#     return render(request, 'birthday/birthday.html', context)


# class BirthdayMixin:
#     # Указываем модель, с которой работает CBV...
#     model = models.Birthday
#     # Указываем namespace:name страницы, куда будет
#       перенаправлен пользователь
#     # после создания объекта:
#     success_url = reverse_lazy('birthday:list')


# class BirthdayFormMixin:
#     # Указываем имя формы:
#     form_class = forms.BirthdayForm
#
#    # Этот класс сам может создать форму на основе модели!
#    # Нет необходимости отдельно создавать форму через ModelForm.
#    # Явным образом указываем шаблон:
#    # template_name = 'birthday/birthday.html'


# class BirthdayCreateView(LoginRequiredMixin, CreateView):
#     # success_url = reverse_lazy('birthday:list')
#     # Указываем поля, которые должны быть в форме:
#     # fields = '__all__'
#     # template_name = 'birthday/birthday.html'

#     # Указываем модель, с которой работает CBV...
#     model = models.Birthday
#     # Указываем имя формы:
#     form_class = forms.BirthdayForm

#     def form_valid(self, form):
#         # Присвоить полю author объект пользователя из запроса.
#         form.instance.author = self.request.user
#         # Вызываем обязательный метод form_valid,
#         # который вернет форму, если она валидна.
#         return super().form_valid(form)


# class BirthdayUpdateView(OnlyAuthorMixin, LoginRequiredMixin, UpdateView):
#     # success_url = reverse_lazy('birthday:list')
#     # template_name = 'birthday/birthday.html'
#     model = models.Birthday
#     form_class = forms.BirthdayForm


# def delete_birthday(request, pk):
#     # Получаем объект модели или выбрасываем 404 ошибку.
#     instance = get_object_or_404(models.Birthday, pk=pk)
#     # В форму передаём только объект модели;
#     # передавать в форму параметры запроса не нужно.
#     form = forms.BirthdayForm(instance=instance)
#     context = {'form': form}
#     # Если был получен POST-запрос...
#     if request.method == 'POST':
#         # ...удаляем объект:
#         instance.delete()
#         # ...и переадресовываем пользователя на страницу со списком записей.
#         return redirect('birthday:list')
#     # Если был получен GET-запрос — отображаем форму.
#     return render(request, 'birthday/birthday.html', context)


# def accepted(request):
#     # print(request.GET)
#     return render(request, 'birthday/accepted.html')


# def birthday_list(request):
#     # Получаем список всех объектов с сортировкой по дню рождения.
#     birthdays = models.Birthday.objects.all().order_by('birthday')
#     # Создаём объект пагинатора с количеством 5 записей на страницу.
#     paginator = Paginator(birthdays, 4)
#     # Получаем номер текущей страницы из GET-параметра.
#     page_number = request.GET.get('page')
#     # Получаем объекты для текущей страницы.
#     page_obj = paginator.get_page(page_number)
#     # Передаём объекты для текущей страницы в контекст шаблона.
#     context = {'page_obj': page_obj}
#     return render(request, 'birthday/birthday_list.html', context)


# @login_required
# def add_comment(request, pk):
#     # Получаем объект дня рождения или выбрасываем 404 ошибку.
#     birthday = get_object_or_404(models.Birthday, pk=pk)
#     # Функция должна обрабатывать только POST-запросы.
#     form = CongratulationForm(request.POST)
#     if form.is_valid():
#         # Создаём объект поздравления, но не сохраняем его в БД.
#         congratulation = form.save(commit=False)
#         # В поле author передаём объект автора поздравления.
#         congratulation.author = request.user
#         # В поле birthday передаём объект дня рождения.
#         congratulation.birthday = birthday
#         # Сохраняем объект в БД.
#         congratulation.save()
#     # Перенаправляем пользователя назад, на страницу дня рождения.
#     return redirect('birthday:detail', pk=pk)
