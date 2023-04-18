from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from promotion import views as view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('getdatareport/', view.getdatareport),#api for get usernewuser
    path('newuser/<str:id>', view.newuser),
    path('storedata/<str:id>', view.storedata),#api for requesing from 
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
