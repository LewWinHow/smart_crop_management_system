import time
import requests
import os
import django

# =====================
# Django 初始化（很重要）
# =====================
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smart_crop_management_system.settings")
django.setup()

from monitoring.models import Weather


# =====================
# 获取天气
# =====================
def fetch_weather():
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": 3.8077,
        "longitude": 103.3260,
        "current": "temperature_2m,relative_humidity_2m,precipitation"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("API failed:", response.text)
        return None

    data = response.json()["current"]

    return {
        "temperature": data["temperature_2m"],
        "humidity": data["relative_humidity_2m"],
        "rainfall": data["precipitation"]
    }


# =====================
# 存入数据库
# =====================
def save_weather():
    data = fetch_weather()

    if not data:
        return

    Weather.objects.create(
        temperature=data["temperature"],
        humidity=data["humidity"],
        rainfall=data["rainfall"]
    )

    print("Saved:", data)


# =====================
# 主循环（每30分钟）
# =====================
def run():
    print("Weather service started...")

    while True:
        try:
            save_weather()
        except Exception as e:
            print("Error:", e)

        # 30分钟 = 1800秒
        time.sleep(1800)


# =====================
# 启动入口
# =====================
if __name__ == "__main__":
    run()