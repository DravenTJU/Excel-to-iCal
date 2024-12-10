from django.urls import path
from . import views

urlpatterns = [
    path('convert/', views.ConvertExcelToICalView.as_view(), name='convert_excel'),
    path('download/<str:filename>/', views.DownloadICalView.as_view(), name='download_ical'),
] 