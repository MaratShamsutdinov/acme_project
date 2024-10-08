from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView

from users import forms

from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import include, path, reverse_lazy

from typing import List


handler404 = 'core.views.page_not_found'


urlpatterns: List[path] = [
    path(
        'auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=forms.CustomUserCreationForm,
            success_url=reverse_lazy('pages:homepage'),
        ),
        name='registration',
        ),
    path(
        'auth/',
        include('django.contrib.auth.urls')
        ),
    path(
        '',
        include('pages.urls')
        ),
    path(
        'admin/',
        admin.site.urls
        ),
    path(
        'birthday/',
        include('birthday.urls')
        ),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (
        path(
            '__debug__/',
            include(debug_toolbar.urls)
            ),
            )

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
    )
