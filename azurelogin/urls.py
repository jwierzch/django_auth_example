"""
URL configuration for azurelogin project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('oauth2/', include('django_auth_adfs.urls')),
    path('', include('app.urls')),
]


"""
https://django-auth-adfs.readthedocs.io/en/latest/install.html

urlpatterns = [
    ...
    path('oauth2/', include('django_auth_adfs.urls')),
]
This will add these paths to Django:

/oauth2/login where users are redirected to, to initiate the login with ADFS.

/oauth2/login_no_sso where users are redirected to, to initiate the login with ADFS but forcing a login screen.

/oauth2/callback where ADFS redirects back to after login. So make sure you set the redirect URI on ADFS to this.

/oauth2/logout which logs out the user from both Django and ADFS.

You can use them like this in your django templates:

<a href="{% url 'django_auth_adfs:logout' %}">Logout</a>
<a href="{% url 'django_auth_adfs:login' %}">Login</a>
<a href="{% url 'django_auth_adfs:login-no-sso' %}">Login (no SSO)</a> """