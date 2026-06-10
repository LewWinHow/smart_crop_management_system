import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.views import View

from monitoring.models import *


class GetCropZoneData(LoginRequiredMixin, View):
    template_name = 'monitoring/monitoring.html'

    def get(self, request):
        zones = Zone.objects.all().prefetch_related("oil_palm_tree")

        zone_list = []

        # =========================
        # 🔝 GLOBAL AGGREGATION
        # =========================
        total_trees = 0
        total_healthy = 0
        total_nutrient_deficiency = 0
        total_sick = 0
        total_unknown = 0

        # =========================
        # 🌤️ FARM-WIDE WEATHER HISTORY
        # =========================
        weather_dates = []
        weather_temp_history = []
        weather_hum_history = []
        weather_rain_history = []

        # Get recent weather records from database
        recent_weather = Weather.objects.order_by("-created_time")[:7]
        for w in reversed(list(recent_weather)):
            weather_dates.append(w.created_time.strftime("%m-%d %H:%M"))
            weather_temp_history.append(float(w.temperature))
            weather_hum_history.append(float(w.humidity))
            weather_rain_history.append(float(w.rainfall))

        # Get latest weather for KPI display
        latest_weather = Weather.objects.order_by("-created_time").first()
        current_temp = round(latest_weather.temperature, 1) if latest_weather else None
        current_humidity = round(latest_weather.humidity, 1) if latest_weather else None
        current_rainfall = round(latest_weather.rainfall, 1) if latest_weather else None

        # =========================
        # 📊 CHART DATA HOLDERS
        # =========================
        zone_labels = []
        infection_rates = []
        productivity_fruiting = []
        productivity_non_fruiting = []
        productivity_unknown = []
        disease_map = {}
        # Per-zone health status data
        zone_healthy = []
        zone_nutrient_deficiency = []
        zone_sick = []
        zone_unknown = []
        # Per-zone disease data
        zone_none = []
        zone_ganoderma = []
        zone_leaf_spot = []
        zone_anthracnose = []
        zone_disease_unknown = []
        health_status_map = {
            1: 0,  # Healthy
            2: 0,  # Nutrient Deficiency
            3: 0,  # Sick
            4: 0   # Unknown
        }

        # Disease name mapping
        disease_name_map = {
            1: 'None',
            2: 'Ganoderma Disease',
            3: 'Leaf Spot',
            4: 'Anthracnose',
            5: 'Unknown'
        }

        # =========================
        # 🟩 PER ZONE PROCESSING
        # =========================
        for zone in zones:
            trees = zone.oil_palm_tree.all()

            total = trees.count()
            healthy = trees.filter(status=1).count()
            nutrient_deficiency = trees.filter(status=2).count()
            sick = trees.filter(status=3).count()
            unknown = trees.filter(status=4).count()

            total_trees += total
            total_healthy += healthy
            total_nutrient_deficiency += nutrient_deficiency
            total_sick += sick
            total_unknown += unknown

            # infection rate
            rate = round((sick / total * 100), 2) if total else 0

            # productivity counting (productivity field: 1=Producing, 2=Not Producing, 3=Unknown)
            fruiting = trees.filter(productivity=1).count()
            non_fruiting = trees.filter(productivity=2).count()
            unknown_productivity = trees.filter(productivity=3).count()

            # disease counting
            disease_counts = trees.values('disease').annotate(count=Count('id'))
            disease_dict = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
            for d in disease_counts:
                disease_id = d['disease']
                if disease_id in disease_dict:
                    disease_dict[disease_id] = d['count']
                disease_name = disease_name_map.get(disease_id, 'Unknown')
                disease_map[disease_name] = disease_map.get(disease_name, 0) + d['count']

            # Append per-zone disease data
            zone_none.append(disease_dict[1])
            zone_ganoderma.append(disease_dict[2])
            zone_leaf_spot.append(disease_dict[3])
            zone_anthracnose.append(disease_dict[4])
            zone_disease_unknown.append(disease_dict[5])

            # health status counting
            status_counts = trees.values('status').annotate(count=Count('id'))
            for s in status_counts:
                status_id = s['status']
                if status_id in health_status_map:
                    health_status_map[status_id] += s['count']

            # append chart data
            zone_labels.append(f"Zone {zone.zone_name}")
            infection_rates.append(rate)
            productivity_fruiting.append(fruiting)
            productivity_non_fruiting.append(non_fruiting)
            productivity_unknown.append(unknown_productivity)
            # Append per-zone health status
            zone_healthy.append(healthy)
            zone_nutrient_deficiency.append(nutrient_deficiency)
            zone_sick.append(sick)
            zone_unknown.append(unknown)

            zone_list.append({
                "id": zone.id,
                "zone_name": zone.zone_name,
                "n_value": zone.n_value,
                "p_value": zone.p_value,
                "k_value": zone.k_value,
                "ph": zone.ph,
                "total_trees": total,
                "healthy_trees": healthy,
                "nutrient_deficiency_trees": nutrient_deficiency,
                "sick_trees": sick,
                "unknown_trees": unknown,
                "producing_trees": fruiting,
                "not_producing_trees": non_fruiting,
                "unknown_productivity_trees": unknown_productivity,
                "infection_rate": rate,
            })

        # =========================
        # 🔝 GLOBAL KPI
        # =========================
        global_data = {
            "zone_count": zones.count(),
            "total_trees": total_trees,
            "healthy": total_healthy,
            "nutrient_deficiency": total_nutrient_deficiency,
            "sick": total_sick,
            "unknown": total_unknown,
        }

        return render(request, self.template_name, {
            "zones": zone_list,
            "global": global_data,
            "current_temp": current_temp,
            "current_humidity": current_humidity,
            "current_rainfall": current_rainfall,
            "zone_labels": json.dumps(zone_labels),
            "infection_rates": json.dumps(infection_rates),
            "productivity_fruiting": json.dumps(productivity_fruiting),
            "productivity_non_fruiting": json.dumps(productivity_non_fruiting),
            "productivity_unknown": json.dumps(productivity_unknown),
            "zone_healthy": json.dumps(zone_healthy),
            "zone_nutrient_deficiency": json.dumps(zone_nutrient_deficiency),
            "zone_sick": json.dumps(zone_sick),
            "zone_unknown": json.dumps(zone_unknown),
            "zone_none": json.dumps(zone_none),
            "zone_ganoderma": json.dumps(zone_ganoderma),
            "zone_leaf_spot": json.dumps(zone_leaf_spot),
            "zone_anthracnose": json.dumps(zone_anthracnose),
            "zone_disease_unknown": json.dumps(zone_disease_unknown),
            "health_status_labels": json.dumps(['Healthy', 'Nutrient Deficiency', 'Sick', 'Unknown']),
            "health_status_data": json.dumps([health_status_map[1], health_status_map[2], health_status_map[3], health_status_map[4]]),
            "disease_labels": json.dumps(list(disease_map.keys())),
            "disease_data": json.dumps(list(disease_map.values())),
            "weather_dates": json.dumps(weather_dates),
            "weather_temp_history": json.dumps(weather_temp_history),
            "weather_hum_history": json.dumps(weather_hum_history),
            "weather_rain_history": json.dumps(weather_rain_history),
        })


class ZoneDetailView(LoginRequiredMixin, View):
    template_name = 'monitoring/zone_detail.html'

    def get(self, request, zone_id):
        # Get specific Zone with related data
        zone = get_object_or_404(Zone, id=zone_id)
        trees = zone.oil_palm_tree.all()

        # Zone level KPI statistics
        total_trees = trees.count()
        healthy_trees = trees.filter(status=1).count()
        nutrient_deficiency_trees = trees.filter(status=2).count()
        sick_trees = trees.filter(status=3).count()
        unknown_trees = trees.filter(status=4).count()
        infection_rate = round((sick_trees / total_trees * 100), 2) if total_trees else 0

        # Disease name mapping
        disease_name_map = {
            1: 'None',
            2: 'Ganoderma Disease',
            3: 'Leaf Spot',
            4: 'Anthracnose',
            5: 'Unknown'
        }

        # Extract tree details list
        tree_list = []
        for t in trees:
            tree_list.append({
                "id": t.id,
                "row": t.row,
                "col": t.column,
                "status": t.status,
                "productivity": t.productivity,
                "disease": t.disease,
                "disease_name": disease_name_map.get(t.disease, 'Unknown'),
                "age": t.age
            })

        context = {
            "zone": zone,
            "total_trees": total_trees,
            "healthy_trees": healthy_trees,
            "nutrient_deficiency_trees": nutrient_deficiency_trees,
            "sick_trees": sick_trees,
            "unknown_trees": unknown_trees,
            "infection_rate": infection_rate,
            "tree_list": json.dumps(tree_list),
        }
        return render(request, self.template_name, context)


class TreeDetailView(LoginRequiredMixin, View):
    template_name = 'monitoring/tree_detail.html'

    def get(self, request, tree_id):
        # Get specific tree with related Zone
        tree = get_object_or_404(
            OilPalmTree.objects.select_related('zone'),
            id=tree_id
        )

        # Mapping dictionaries
        disease_map = {
            1: 'None',
            2: 'Ganoderma Disease',
            3: 'Leaf Spot',
            4: 'Anthracnose',
            5: 'Unknown'
        }

        production_map = {
            0: 'None',
            1: 'Yes'
        }

        status_map = {
            1: 'Healthy',
            2: 'Nutrient Deficiency',
            3: 'Sick',
            4: 'Unknown'
        }

        # Get disease info
        disease_name = disease_map.get(tree.disease, 'Unknown')
        is_clean = tree.disease == 1

        # Get productivity status
        prod_name = production_map.get(tree.productivity, 'Unknown')

        context = {
            'tree': tree,
            'zone': tree.zone,
            'disease_name': disease_name,
            'is_clean': is_clean,
            'prod_name': prod_name,
            'productivity': tree.productivity,
            'status_name': status_map.get(tree.status, 'Unknown'),
        }
        return render(request, self.template_name, context)
