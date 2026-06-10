from django.db import models


# Create your models here.
# 分区
class Zone(models.Model):
    zone_name = models.IntegerField()
    n_value = models.FloatField(db_comment="Nitrogen (mg/kg)")
    p_value = models.FloatField(db_comment="Phosphorus (mg/kg)")
    k_value = models.FloatField(db_comment="Potassium (mg/kg)")
    ph = models.FloatField()
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'zone'


# 天气
class Weather(models.Model):
    temperature = models.FloatField()
    humidity = models.FloatField()
    rainfall = models.FloatField()
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'weather'


# 油棕树
class OilPalmTree(models.Model):
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name="oil_palm_tree")
    age = models.IntegerField()
    status = models.IntegerField(default=4, db_comment="1 = Healthy, 2 = Nutrient Deficiency, 3 = Sick, 4 = Unknown")
    disease = models.IntegerField(default=6,
                                  db_comment='1 = None, 2 = Ganoderma Disease, 3 = Leaf Spot, 4 = Anthracnose, 5 = Unknown')
    productivity = models.IntegerField(db_comment="1 = Producing, 2 = Not Producing, 3 = Unknown")
    column = models.IntegerField()
    row = models.IntegerField()
    describe = models.TextField(null=True, blank=True)
    image_path = models.FileField(upload_to="oil_palm_tree/", null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'oil_palm_tree'
