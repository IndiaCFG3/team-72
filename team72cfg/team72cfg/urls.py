"""team72cfg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from users import views as users_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from students import views as students_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',users_views.home,name='home'),
    path('profile/', users_views.profile,name='profile'),
    path('register/', users_views.register,name='register'),
    path('login/',auth_views.LoginView.as_view(template_name='users/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='users/logout.html'),name='logout'),
    path('mystudents/<int:id>/',students_views.mystudents,name='mystudents'),
    path('mystudents/<int:id>/<int:sid>/details',students_views.details,name='details'),
    path('mystudents/<int:id>/<int:sid>/details/form',students_views.detailsform,name='details-form'),
    path('students/register/',students_views.register,name='student-register'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




    
