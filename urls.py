from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("contas/", include("allauth.urls")),  # login/cadastro
    path("", RedirectView.as_view(url="/contas/login/", permanent=False)),  # Redirect root to login
    path("", include("core.urls")),            # app principal
]

# Custom 404 handler
handler404 = 'core.views.custom_404'
