from django.urls import path

from monitoring.views import *

app_name = 'monitoring'

urlpatterns = [
    path('get_crop_zone_data/', GetCropZoneData.as_view(), name='get_crop_zone_data'),
    path("zone/<int:zone_id>/", ZoneDetailView.as_view(), name="zone_detail"),
    path("tree/<int:tree_id>/", TreeDetailView.as_view(), name="tree_detail"),
]
