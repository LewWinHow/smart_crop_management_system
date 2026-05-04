from django.db import models


# Create your models here.
# 分区
class Zone(models.Model):
    zone_name = models.IntegerField(db_comment="1 = A, 2 = B, 3 = C, 4 = D")
    n_value = models.FloatField(db_comment="Nitrogen (mg/kg)")
    p_value = models.FloatField(db_comment="Phosphorus (mg/kg)")
    k_value = models.FloatField(db_comment="Potassium (mg/kg)")
    ph = models.FloatField()
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'zone'


# 天气
class WeatherData(models.Model):
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name="weather_data")
    temperature = models.FloatField()
    humidity = models.FloatField()
    rainfall = models.FloatField()
    duration = models.FloatField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'weather_data'


# 具体疾病
class Sick(models.Model):
    sick_name = models.IntegerField(db_comment=
                                    "1 = healthy; "
                                    "2 = detect Ganoderma; "  # 检测到疑似感染 Ganoderma 真菌
                                    "3 = Ganoderma Fungus; "  # 已确认感染 Ganoderma 真菌
                                    "4 = unproductive_hollow_stem; "  # 树干空心，典型 Ganoderma 症状
                                    "5 = unproductive_moldy; "  # 树体或果穗发霉，真菌病害相关
                                    )

    class Meta:
        db_table = 'sick'


# 生产力
class ProductivityStatus(models.Model):
    productivity_status = models.IntegerField(db_comment=
                                              "1 = productive_fruiting; "  # 健康且结果
                                              "2 = productive_non_fruiting; "  # 健康但未结果
                                              "3 = unproductive_desiccated; "  # 干枯失去生产力
                                              )

    class Meta:
        db_table = 'productivity_status'


# 油棕树
class PalmTree(models.Model):
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name="palmtrees")
    status = models.IntegerField(db_comment="1=healthy, 2=sick")
    productivity = models.ForeignKey(ProductivityStatus, on_delete=models.SET_NULL, blank=True, null=True)
    column = models.IntegerField()
    row = models.IntegerField()
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'palm_tree'
        unique_together = ('zone', 'row', 'column')


# PalmTree 与 Sick 中间表
class PalmTreeSick(models.Model):
    palm_tree = models.ForeignKey(PalmTree, on_delete=models.CASCADE)
    sick = models.ForeignKey(Sick, on_delete=models.CASCADE)

    detected_at = models.DateTimeField(auto_now_add=True)
    recovered_at = models.DateTimeField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'palm_tree_sick'


# 建立 ManyToMany（through）
PalmTree.add_to_class(
    'sick',
    models.ManyToManyField(Sick, through='PalmTreeSick')
)
