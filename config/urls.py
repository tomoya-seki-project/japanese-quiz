"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from errorHandler.views import error400, error403, error404, error500

handler400 = error400
handler403 = error403
handler404 = error404
handler500 = error500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name="core/index.html"), name="HomePage"),
    path('accounts/', include('accounts.urls')),
    path('core/', include('core.urls')),
    path('dictionary/', include('dictionary.urls')),
    path('quiz/', include('quiz.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        path(
            'ui-confirm/',
            TemplateView.as_view(template_name='config/ui_confirm.html'),
            name='ui_confirm',
        ),
        path(
            'ui-confirm/account-activation/confirm/',
            TemplateView.as_view(
                template_name='accounts/user_activate.html',
                extra_context={
                    'activation_status': 'confirm',
                    'ui_preview': True,
                },
            ),
            name='ui_confirm_activation_confirm',
        ),
        path(
            'ui-confirm/account-activation/success/',
            TemplateView.as_view(
                template_name='accounts/user_activate.html',
                extra_context={
                    'activation_status': 'success',
                    'ui_preview': True,
                },
            ),
            name='ui_confirm_activation_success',
        ),
        path(
            'ui-confirm/account-activation/already-active/',
            TemplateView.as_view(
                template_name='accounts/user_activate.html',
                extra_context={
                    'activation_status': 'already_active',
                    'ui_preview': True,
                },
            ),
            name='ui_confirm_activation_already_active',
        ),
        path(
            'ui-confirm/account-activation/invalid/',
            TemplateView.as_view(
                template_name='accounts/user_activate.html',
                extra_context={
                    'activation_status': 'invalid',
                    'ui_preview': True,
                },
            ),
            name='ui_confirm_activation_invalid',
        ),
        path(
            'ui-confirm/quiz/no-question/',
            TemplateView.as_view(
                template_name='config/ui_confirm_no_question.html',
            ),
            name='ui_confirm_quiz_no_question',
        ),
        path(
            'ui-confirm/error/400/',
            TemplateView.as_view(template_name='errorHandler/error400.html'),
            name='ui_confirm_error400',
        ),
        path(
            'ui-confirm/error/403/',
            TemplateView.as_view(template_name='errorHandler/error403.html'),
            name='ui_confirm_error403',
        ),
        path(
            'ui-confirm/error/404/',
            TemplateView.as_view(template_name='errorHandler/error404.html'),
            name='ui_confirm_error404',
        ),
        path(
            'ui-confirm/error/500/',
            TemplateView.as_view(template_name='errorHandler/error500.html'),
            name='ui_confirm_error500',
        ),
    ]
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
