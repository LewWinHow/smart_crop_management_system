from django.urls import path

from analyze.views import UploadOilPalmTreeImage

app_name = 'analyze'

urlpatterns = [
    path('upload_oil_palm_tree_image/', UploadOilPalmTreeImage.as_view(), name='upload_oil_palm_tree_image'),
]
