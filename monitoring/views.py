from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.views import View

from monitoring.models import *


#class GetCropZoneData(LoginRequiredMixin, View):
class GetCropZoneData(View):
    template_name = 'monitoring/monitoring.html'

    def get(self, request):
        zones = Zone.objects.all().prefetch_related("palmtrees", "weather_data")

        zone_list = []

        # =========================
        # 🔝 GLOBAL AGGREGATION
        # =========================
        total_trees = 0
        total_healthy = 0
        total_sick = 0

        # =========================
        # 📊 CHART DATA HOLDERS
        # =========================
        zone_labels = []

        infection_rates = []
        productivity_fruiting = []
        productivity_non_fruiting = []
        productivity_dead = []

        temp_avg = []
        humidity_avg = []
        rainfall_avg = []

        disease_map = {}

        # =========================
        # 🟩 PER ZONE PROCESSING
        # =========================
        for zone in zones:

            trees = zone.palmtrees.all()

            total = trees.count()
            healthy = trees.filter(status=1).count()
            sick = trees.filter(status=2).count()

            total_trees += total
            total_healthy += healthy
            total_sick += sick

            # infection rate
            rate = round((sick / total * 100), 2) if total else 0

            # productivity
            prod = trees.values("productivity__productivity_status") \
                        .annotate(count=Count("id"))

            fruiting = 0
            non_fruiting = 0
            dead = 0

            for p in prod:
                if p["productivity__productivity_status"] == 1:
                    fruiting = p["count"]
                elif p["productivity__productivity_status"] == 2:
                    non_fruiting = p["count"]
                elif p["productivity__productivity_status"] == 3:
                    dead = p["count"]

            # weather
            weather_qs = zone.weather_data.order_by("-end_time")[:7]

            if weather_qs:
                temp_avg_val = sum(w.temperature for w in weather_qs) / len(weather_qs)
                humidity_avg_val = sum(w.humidity for w in weather_qs) / len(weather_qs)
                rainfall_avg_val = sum(w.rainfall for w in weather_qs) / len(weather_qs)
            else:
                temp_avg_val = 0
                humidity_avg_val = 0
                rainfall_avg_val = 0

            # disease
            disease_data = PalmTreeSick.objects.filter(
                palm_tree__zone=zone,
                is_active=True
            ).values("sick__sick_name").annotate(count=Count("id"))

            for d in disease_data:
                name = str(d["sick__sick_name"])
                disease_map[name] = disease_map.get(name, 0) + d["count"]

            # append chart data
            zone_labels.append(f"Zone {zone.zone_name}")
            infection_rates.append(rate)
            productivity_fruiting.append(fruiting)
            productivity_non_fruiting.append(non_fruiting)
            productivity_dead.append(dead)

            temp_avg.append(round(temp_avg_val, 2))
            humidity_avg.append(round(humidity_avg_val, 2))
            rainfall_avg.append(round(rainfall_avg_val, 2))

            zone_list.append({
                "id": zone.id,
                "zone_name": zone.zone_name,
                "n_value": zone.n_value,
                "p_value": zone.p_value,
                "k_value": zone.k_value,
                "ph": zone.ph,

                "total_trees": total,
                "healthy_trees": healthy,
                "sick_trees": sick,
                "infection_rate": rate,

                "productivity": list(prod),

                "latest_weather": weather_qs.first() if weather_qs else None,
            })

        # =========================
        # 🔝 GLOBAL KPI
        # =========================
        global_data = {
            "zone_count": zones.count(),
            "total_trees": total_trees,
            "healthy": total_healthy,
            "sick": total_sick,
            "infection_rate": round((total_sick / total_trees * 100), 2) if total_trees else 0
        }

        return render(request, self.template_name, {
            "zones": zone_list,
            "global": global_data,

            # charts
            "zone_labels": zone_labels,
            "infection_rates": infection_rates,
            "productivity_fruiting": productivity_fruiting,
            "productivity_non_fruiting": productivity_non_fruiting,
            "productivity_dead": productivity_dead,

            "temp_avg": temp_avg,
            "humidity_avg": humidity_avg,
            "rainfall_avg": rainfall_avg,

            "disease_labels": list(disease_map.keys()),
            "disease_data": list(disease_map.values()),
        })


class ZoneDetailView(View):
    template_name = 'monitoring/zone_detail.html'

    def get(self, request, zone_id):
        # 1. 获取特定 Zone，并预取相关数据
        zone = get_object_or_404(Zone, id=zone_id)
        # 使用 select_related 优化外键查询，prefetch_related 优化多对多查询
        trees = zone.palmtrees.select_related('productivity').prefetch_related('sick')

        # 2. Zone 级 KPI 统计
        total_trees = trees.count()
        healthy_trees = trees.filter(status=1).count()
        sick_trees = total_trees - healthy_trees
        infection_rate = round((sick_trees / total_trees * 100), 2) if total_trees else 0

        # 3. 提取树木详情列表 (用于在前端表格展示)
        tree_list = []
        for t in trees:
            disease_ids = [sick.sick_name for sick in t.sick.all()]

            tree_list.append({
                "id": t.id,  # <--- !! 必须加上这行，前端才能知道跳去哪个页面 !!
                "row": t.row,
                "col": t.column,
                "status": t.status,
                "productivity": t.productivity.productivity_status if t.productivity else None,
                "diseases": disease_ids
            })

        # 4. 获取该 Zone 的历史天气数据 (最近10条，按时间倒序排后反转为正序供图表使用)
        weather_qs = zone.weather_data.order_by("-end_time")[:10]
        weather_dates = [w.end_time.strftime("%m-%d %H:%M") for w in weather_qs][::-1]
        weather_temp = [round(w.temperature, 2) for w in weather_qs][::-1]
        weather_hum = [round(w.humidity, 2) for w in weather_qs][::-1]
        weather_rain = [round(w.rainfall, 2) for w in weather_qs][::-1]

        context = {
            "zone": zone,
            "total_trees": total_trees,
            "healthy_trees": healthy_trees,
            "sick_trees": sick_trees,
            "infection_rate": infection_rate,

            "tree_list": tree_list,

            "weather_dates": weather_dates,
            "weather_temp": weather_temp,
            "weather_hum": weather_hum,
            "weather_rain": weather_rain,
        }
        return render(request, self.template_name, context)


class TreeDetailView(View):
    template_name = 'monitoring/tree_detail.html'

    def get(self, request, tree_id):
        # 1. 获取特定树木，预取关联的 Zone、Productivity 和 Sick 数据
        tree = get_object_or_404(
            PalmTree.objects.select_related('zone', 'productivity').prefetch_related('sick'),
            id=tree_id
        )

        # 2. 映射字典 (保证与前后端一致)
        disease_map = {
            1: 'Healthy',
            2: 'Detect Ganoderma',
            3: 'Ganoderma Fungus',
            4: 'Hollow Stem',
            5: 'Moldy'
        }

        prod_map = {
            1: 'Fruiting',
            2: 'Non-Fruiting',
            3: 'Desiccated'
        }

        # 3. 处理病害数据 (过滤掉值为 1 的 Healthy，只显示真正的病害)
        raw_diseases = [sick.sick_name for sick in tree.sick.all()]
        active_diseases = [disease_map.get(d, 'Unknown') for d in raw_diseases if d != 1]
        is_clean = len(active_diseases) == 0

        # 4. 获取生产力状态
        prod_status_val = tree.productivity.productivity_status if hasattr(tree,
                                                                           'productivity') and tree.productivity else None
        prod_name = prod_map.get(prod_status_val, 'Unknown Data')

        context = {
            'tree': tree,
            'zone': tree.zone,
            'prod_status_val': prod_status_val,
            'prod_name': prod_name,
            'active_diseases': active_diseases,
            'is_clean': is_clean,
        }
        return render(request, self.template_name, context)
