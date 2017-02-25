# coding=utf-8

import requests
import re

KEY = "&key=2d849c62d67a4b9e94607d0f1c744561"
CITY = "city=深圳"
APIURL = "https://free-api.heweather.com/v5/"
USERNAME = "Acring"
s = requests.session()


class HeWeather(object):
    now_text = ""
    now_raw = []
    city_text = ""
    city_raw = []

    def __init__(self):
        self.city()

    # 利用获取IP地址的网页，获取本地城市名
    @staticmethod
    def getcity():
        inf = s.get("http://ip.lockview.cn/ShowIP.aspx").text
        cityname = re.findall(r"省(.*?)市", inf)[0]
        return cityname

    # 实况天气
    def now(self):
        api_type = "now?"
        # url = https://free-api.heweather.com/v5/now?city=深圳&key=2d849c62d67a4b9e94607d0f1c744561
        url = APIURL + api_type + CITY + KEY
        raw_json = s.get(url).json()
        if raw_json["HeWeather5"][0]["status"] != "ok":
            return
        self.now_raw = raw_json
        now_basic = raw_json["HeWeather5"][0]["basic"]
        now_now = raw_json["HeWeather5"][0]["now"]
        basic_city = now_basic["city"]  # 城市
        basic_cnty = now_basic["cnty"]  # 国家
        basic_id = now_basic["id"]  # 城市代码
        basic_lat = now_basic["lat"]  # 城市纬度
        basic_lon = now_basic["lon"]  # 城市经度
        basic_loc = now_basic["update"]["loc"]  # 当地时间
        now_tmp = now_now["tmp"]  # 实时气温
        now_cond = now_now["cond"]["txt"]  # 天气描述
        now_vis = now_now["vis"]  # 能见度
        now_hum = now_now["hum"]  # 相对湿度
        now_fl = now_now["fl"]  # 体感温度
        now_pcpn = now_now["pcpn"]  # 降雨量
        now_pres = now_now["pres"]  # 气压
        now_deg = now_now["wind"]["deg"]  # 风向(360度)
        now_dir = now_now["wind"]["dir"]  # 风向
        now_sc = now_now["wind"]["sc"]  # 风力
        now_spd = now_now["wind"]["spd"]  # 风速(kmph)

        text = """
实时天气:
亲爱的 {},您所在的地区为 {} ,
现在{}的天气是 {}天,
气温为 {}°
体感气温为 {}°
风向 {},
风速 {}

                """.format(USERNAME, basic_city, basic_loc, now_cond, now_tmp, now_fl, now_dir, now_spd)
        self.now_text = text
        return text

    def city(self):
        cityname = self.getcity()
        apitype = "search?city="
        # url = https://free-api.heweather.com/v5/search?city=host&key=2d849c62d67a4b9e94607d0f1c744561
        url = APIURL + apitype + cityname + KEY

        raw_json = s.get(url).json()
        if raw_json["HeWeather5"][0]["status"] != "ok":
            return "获取天气失败:", raw_json["HeWeather5"][0]["status"]

        basic = raw_json["HeWeather5"][0]["basic"]
        self.city_raw = basic
        basic_city = basic["city"]
        basic_cnty = basic["cnty"]
        basic_id = basic["id"]
        basic_prov = basic["prov"]  # 所属省会

        city = "&city=" + basic_city

        global CITY
        CITY = city
        city = "国家:{} 城市:{} 所属省会:{} 城市代码:{}".format(basic_cnty, basic_city, basic_prov, basic_id)
        self.city_text = city
        return


if __name__ == '__main__':
    heWeather = HeWeather()
    now = heWeather.now()
    print(now)