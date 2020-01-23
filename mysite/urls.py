from django.contrib import admin
from django.urls import path, include
from user import views as user_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('daily_tasks.urls')),
    path('register/', user_views.register, name="register"),
    path('profile/', user_views.profile_view, name="profile"),
    path('login/', user_views.login, name="login"),
    path('logout/', user_views.logout_view, name="logout"),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)