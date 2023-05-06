from django.urls import path

from core.views import WorkShiftAPI

app_name = 'core'

urlpatterns = [
    path('create/', WorkShiftAPI.as_view(), name='shift-create')
]
