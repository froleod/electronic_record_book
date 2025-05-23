from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from records.views import home
urlpatterns = [

    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('records/', include('records.urls')),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]