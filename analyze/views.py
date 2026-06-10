from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import default_storage
from django.shortcuts import render
from django.views import View

from monitoring.models import OilPalmTree, Zone
from utils import save_image
from utils.qq import pipeline
from utils.save_image import save_image


class UploadOilPalmTreeImage(LoginRequiredMixin, View):
    def get(self, request):
        all_zone = Zone.objects.all()
        all_oil_palm_tree = OilPalmTree.objects.all()
        return render(request, 'anaylze/oil_palm_tree_analyze.html',
                      {'all_zone': all_zone, 'all_oil_palm_tree': all_oil_palm_tree})

    def post(self, request):
        image = request.FILES.get('image') or None
        zone = request.POST.get('zone')
        row = request.POST.get('row')
        column = request.POST.get('column')

        # 获取所有区域和树的数据，用于页面显示
        all_zone = Zone.objects.all()
        all_oil_palm_tree = OilPalmTree.objects.all()

        if not image:
            return render(request, 'anaylze/oil_palm_tree_analyze.html',
                          {'all_zone': all_zone, 'all_oil_palm_tree': all_oil_palm_tree})
        else:
            image_path = save_image(image, 'oil_palm_tree')
            response, Dict = pipeline(image_path)

            oil_palm_tree = OilPalmTree.objects.filter(row=row, column=column, zone=zone).first()
            if oil_palm_tree:
                oil_palm_tree.status = Dict.get('status')
                oil_palm_tree.disease = Dict.get('disease')
                oil_palm_tree.productivity = Dict.get('productivity')
                oil_palm_tree.describe = response
                oil_palm_tree.image_path = image_path
                oil_palm_tree.save()
            
            return render(request, 'anaylze/oil_palm_tree_analyze.html', {
                'image': image_path,
                'response': response,
                'Dict': Dict,
                'MEDIA_URL': settings.MEDIA_URL,
                'all_zone': all_zone,
                'all_oil_palm_tree': all_oil_palm_tree,
            })
