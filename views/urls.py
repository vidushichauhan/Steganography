"""stego URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin #for media
from django.urls import path
from .import views
from .import views1
from .import views2
from .import views3
from .import views4
from .import views5
from .import views6
from .import views7
from .import views8
from django.conf import settings #for media
from django.conf.urls.static import static #for media


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('res1/', views.res1, name='res1'),
    path('tfimage/', views.tfimage, name='tfimage'),
    path('ttext/', views.ttext, name='ttext'),
    path('taudio/', views.taudio, name='taudio'),
    path('tvideo/', views.tvideo, name='tvideo'),
    path('stegotext', views5.stegotext, name='stegotext'),
    path('destegotext', views5.destegotext, name='destegotext'),
    path('t1audio', views3.t1audio, name='t1audio'),
    path('upload3', views6.upload3, name='upload3'),
    path('detextfile', views6.detextfile, name='detextfile'),
    path('upload1', views1.upload1, name='upload1'),
    path('tfimagecode',views2.tfimagecode,name='tfimagecode'),
    path('deimagetext', views1.deimagetext, name='deimagetext'),
    path('deimagetextfile', views2.deimagetextfile, name='deimagetextfile'),
    path('deaudiotext', views3.deaudiotext, name='deaudiotext'),
    path('deaudiotextfile', views4.deaudiotextfile, name='deaudiotextfile'),
    path('tfaudiocode', views4.tfaudiocode, name='tfaudiocode')

    #path('t1image/',views.t1image,name='t1image'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

