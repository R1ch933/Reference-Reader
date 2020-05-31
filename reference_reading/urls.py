from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'reference_reading'
urlpatterns = [
    #home page
    path('',views.index, name='index'),
    #list of files
    path('files/', views.files, name='files'),
    #references of files
    path('files/<int:file_id>/', views.cite, name='cite'),
    #add a new file
    path('new_file', views.new_file, name='new_file'),
    #download current file
    path('download/<int:file_id>', views.download, name='downloading'),
    #deleting current file
    path('delete/<int:file_id>', views.delete_file, name='delete'),
    #decors
    path('decor/<file_name>', views.decor, name='decor'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)