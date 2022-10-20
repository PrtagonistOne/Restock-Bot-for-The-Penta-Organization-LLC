import requests
import json
import time


def get_hd_shipment_status(link, zip_code):
    url = "https://www.homedepot.com/federation-gateway/graphql?opname=shipping"
    prod_id = link.split('/')[-1]
    payload = "{\"query\":\"query shipping($itemId: String!, $storeId: String, $zipCode: String, $quantity: Int!, " \
              "$price: Float!) {shipping(itemId: $itemId, storeId: $storeId, zipCode: $zipCode, quantity: $quantity, " \
              "price: $price) {    itemId    state    excludedShipStates    zipCode    services {      " \
              "deliveryTimeline      deliveryDates {        startDate        endDate      __typename      }      " \
              "deliveryCharge    dynamicEta {       hours        minutes        __typename      }      " \
              "freeDeliveryThreshold      hasFreeShipping      locations {        distance        inventory {         " \
              " isOutOfStock          isInStock          isLimitedQuantity         isUnavailable          quantity    " \
              "      __typename        }        isAnchor        locationId        storeName        storePhone        " \
              "type        __typename      }      type      totalCharge      mode {       code        desc        " \
              "group        longDesc        __typename      }      isDefault     __typename    }    __typename  }}\"," \
              "\"variables\":{" + f"\"itemId\":\"{prod_id}\",\"price\":0,\"quantity\":1," \
                                  f"\"zipCode\":\"{zip_code}\"" + "}}"

    headers = {
        'authority': 'www.homedepot.com',
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,la;q=0.6',
        'apollographql-client-name': 'general-merchandise',
        'apollographql-client-version': '0.0.0',
        'content-type': 'application/json',
        'cookie': 'HD_DC=origin; akacd_usbeta=3843268210~rv=89~id=276b6d6d8ba19eb228a27d7414ca8d6e; at_check=true; AMCVS_F6421253512D2C100A490D45%40AdobeOrg=1; THD_CACHE_NAV_PERSIST=; thda.s=a47f8083-c4cb-d9a6-ed1f-853b7c9c2ae9; thda.u=50d02070-e41e-47fd-12f9-74b5660be793; ajs_user_id=null; ajs_group_id=null; ajs_anonymous_id=%22a2afa466-a5b4-4b70-8e88-28bca017cf3f%22; _meta_bing_beaconFired=true; _meta_facebookPixel_beaconFired=true; _meta_movableInk_mi_u=a2afa466-a5b4-4b70-8e88-28bca017cf3f; _meta_metarouter_timezone_offset=-180; _meta_neustar_mcvisid=78372466863377560650494464534344233592; _meta_googleGtag_library_loaded=1666033141369; thda.m=78372466863377560650494464534344233592; _meta_pinterest_derived_epik_failure=true; _ga=GA1.1.1879859827.1666033141; _gcl_au=1.1.883767044.1666033143; LPVID=EzMDA2YTk3YWMxNmMxMDg2; DELIVERY_ZIP_TYPE=USER; _ga_9H2R4ZXG4J=GS1.1.1666033142.1.0.1666033209.60.0.0; _meta_googleGtag_ga=GA1.1.1879859827.1666033141; QSI_SI_2lVW226zFt4dVJ3_intercept=true; _meta_mediaMath_iframe_counter=5; _pxvid=75583752-4ec7-11ed-b001-6d6a656a7874; _px_f394gi7Fvmc43dfg_user_id=NzU5YTJjNTAtNGVjNy0xMWVkLWEyYTctODMzYWEwZDI2ODgx; _meta_tapAd_id=425fb915-f177-448b-a5ed-d2cf854544a4; _meta_yahooMedia_yahoo_id=y-C9COUUdE2r1V1QJe71M3B_Bhdo.76p492u7gNutnhaWOEEEJM9kIEffbMJLMqNbGiS8Xw4eh~A; trx=7894223971713754943; _meta_revjet_revjet_vid=7894223971713754943; _meta_acuityAds_auid=685339640668; _meta_acuityAds_cauid=auid=685339640668; _meta_inMarket_userNdat=E2874F2D23724E63FE71D24D02C78011; _meta_mediaMath_mm_id=175a62d8-6dd6-4000-8d97-c32608449aae; _meta_mediaMath_cid=175a62d8-6dd6-4000-8d97-c32608449aae; aam_mobile=seg%3D1131078; aam_uuid=78284202513336416840485241094413376525; _meta_amobee_uid=7910763352670746520; QuantumMetricUserID=689bc9afb6b6ae04d44b51b7362c0a5f; _meta_adobe_aam_uuid=78284202513336416840485241094413376525; _meta_adobe_fire_sync_chain={"xandr":false,"revjet":true,"mediaMath":true}; _meta_adobe_neustar=true; _meta_adobe_google=true; _meta_adobe_microsoft=true; _meta_neustar_aam=78284202513336416840485241094413376525; THD_PERSIST=C6%3d%7b%22I1%22%3a%221%22%7d%3a%3bC6%5fEXP%3d1668677510; THD_MCC_ID=6895d429-52ff-43ad-9ac2-3f589b5bd0ca; cart_activity=a9cacff1-88ec-488d-8088-d47b012e7c8e; ecrSessionId=F2D172BF96146AF59A981897A0A80276; THD_SESSION=C16%3d97217%2c4007%2c0%3a%3b; DELIVERY_ZIP=97217; THD_CACHE_NAV_SESSION=; AKA_A2=A; _abck=95158423A4414B8293D53F462A02E5D3~0~YAAQjoIsF8axguCDAQAAj7Zq8Qiqqs6q+601jJJg0oGFt9SdmMzVSoQQy6/pki96Bh9cUZIN5IWx4TGgpO0S/oPdfvk8ClM12jBYT2vLvHxQLIGE0yfch6E5SDw42yvqQM6lAREQAtdOFlFEAbmgS1o45TPWhdkuEiHnInprVz4kqQqZMBmiFSDQ+3IHXN1tK/mPtO6+Axp3K+T18e11Lhx7hrXVjXdxgQTAzbn69+ogddsJfegd6hfVIR6L2aishR9heDDBHXemvrCT7dX/ZFt78GOxGZgon8gAMVXNSP8k9fhWI6kwn85oAPN98vAbtR1tH7vosnpA9Dh5DixSKz8kHzwwhbchbfD5vyqVhOanh6lHr/anWtf7dnCsL8YXugtMUaIGeIWaRxxOc9R3MfXJQGL7dB/vvbI=~-1~-1~-1; bm_sz=D4F485029645C0A410F61B336B727259~YAAQjoIsF8mxguCDAQAAkLZq8RESZ/qHp+KFm0KqSD2FmREcfFmsgETwAR+VcNmtwlUiFjWxK6kHj5j+q3L0GVd9cNKfGelTXqfRKjGp1qc+oOzvgZoCTUFXk6ZmszDOru9MNZtv5AK3RMYMtKwg6p5iiGFqrvDH41ebag6xAq5HaTJ7oU/pK5bAQVRdAYGNqHL3YTotJ7TiTt8pwY0F/qVMkor74WKaAaK+G0cDnxIreuetMJN9xF3z0fLmI6kFAoZQeXBGI3SST0ISJox3TU1iGBt0sNjj638F+K1toTSn1zugjLM=~3359553~4339001; THD_NR=1; ak_bmsc=150781D816865A348FF80DAC69AC12C7~000000000000000000000000000000~YAAQjoIsFwe0guCDAQAAO79q8RFULurIKaSzlX/6BjUAxNjdVED9VpWhs5uQV3JpP2vDLmHtNQkZCKqMQ74Rsh8qos3eJbSnVM2E+sKiE7MDVO6mClQvpUSOptFRDw+xXs5zX29qsIEb0ALsIXdd44RonMUZFVxSKhpussK7U94hfv51gNenSE+qHtEos2DoWg6wWnuZPDoEXa6Xf+QhA4ETCfwtwxpZ+zaaFFJfMYxx1tDKY3x7Fpn6NDm8Z5fu/TNIIwmXhxeWtChVBDzicI9usO0Z2TEqaquHMGL61pVp6XEfKbyMcgYQwGQ5bWTzzT068s1fp5xP1Cz1qhTeImbz5ymGzn9OQSfOIqTclINOq7wk6fllSLDjm4JNiTtLRH13TJlMZ0K88OJNlGaAKamWcFLA2Z/vXY1ehTXrhx7psn/rxRD1tMbanB/ocilRYK0z3sQ3lwsorK7BudeYGUgRCVxmCB4AVh6ZHrRPr8j6dXZVBek1ZCFennf36tXX; THD_LOCALIZER=%257B%2522WORKFLOW%2522%253A%2522LOCALIZED_BY_STORE%2522%252C%2522THD_FORCE_LOC%2522%253A%25220%2522%252C%2522THD_INTERNAL%2522%253A%25220%2522%252C%2522THD_LOCSTORE%2522%253A%25224007%252BJantzen%2520Beach%2520-%2520Portland%252C%2520OR%252B%2522%252C%2522THD_STRFINDERZIP%2522%253A%252297217%2522%252C%2522THD_STORE_HOURS%2522%253A%25221%253B7%253A00-20%253A00%253B2%253B6%253A00-21%253A00%253B3%253B6%253A00-21%253A00%253B4%253B6%253A00-21%253A00%253B5%253B6%253A00-21%253A00%253B6%253B6%253A00-21%253A00%253B7%253B6%253A00-21%253A00%2522%252C%2522THD_STORE_HOURS_EXPIRY%2522%253A1666206249%257D; AMCV_F6421253512D2C100A490D45%40AdobeOrg=1585540135%7CMCMID%7C78372466863377560650494464534344233592%7CMCAAMLH-1666807452%7C7%7CMCAAMB-1666807452%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1666209852s%7CNONE%7CMCCIDH%7C1521153318%7CvVersion%7C4.4.0; QuantumMetricSessionID=c49f0592e13194bb20cd4f74c839e540; LPSID-31564604=dVdwVyJXSlCHx38KMPzy0Q; mbox=PC#bed3f8f78ed948abb278e16adbec8698.35_0#1729447476|session#eab96ae33df24246a4a317683658ee5e#1666204536; _px=Ebo6pW1Py1zL3eB7UltuTZZY2OYMU9/6oeis1V+dIsGjevRIzfv49B4F2D8KIHXGiLweStI9o/2fAYaQu1bQZw==:1000:4JuiEhf8lggZaMnEFpFpWhoHCoMxL7qLsFblBRy2abh4NZl4L57KfkVa4E5XXWry7gKJ/26FzUOVATTBy2rgCyfVg1NYtQ9rh7TAvAzeq5VD7UdYeXTHl1t6yMjGws5fozzjDKVosVfue09sZb8f+NlGy5kDDsdBGqDLv53yLT2nezP4zVuSQduZ+hIJDxBpinvlCiXeSAc+mSS8YprYPwSC0KiLElYAjc1wjfyNk2NM4jB1TOVKYOFkjGVhzS2KpQ5JTks1cbrgcfoa1iUt5Q==; forterToken=19559a1b17c94149b2028025b0451245_1666202676373__UDF43_13ck; RT="z=1&dm=www.homedepot.com&si=0f56789b-d9b0-4179-abc6-798d767b7a79&ss=l9fy18lo&sl=2&tt=3tm&obo=1&rl=1&nu=5c7al69e&cl=rr5"; QSI_HistorySession=https%3A%2F%2Fwww.homedepot.com%2Fb%2FKitchen-Tableware-Bar-Drinkware-Beer-Glasses%2FN-5yc1vZ2fkp5qa~1666202662455%7Chttps%3A%2F%2Fwww.homedepot.com%2Fb%2FKitchen-Tableware-Bar-Drinkware%2FN-5yc1vZ2fkp36v~1666202663168%7Chttps%3A%2F%2Fwww.homedepot.com%2Fs%2Fear%2520buds%3FNCNI-5~1666202677294%7Chttps%3A%2F%2Fwww.homedepot.com%2Fp%2FKlein-Tools-Bluetooth-Jobsite-Earbuds-AESEB1%2F316914084~1666202680980; akaau=1666202981~id=962163b1945fa560b6ca5ce844379623; akavpau_prod=1666202981~id=3991bc08dfe784d6cb1debe68c7baad8; s_sess=%20s_cc%3Dtrue%3B%20s_pv_pName%3Dproductdetails%253E316914084%3B%20s_pv_pType%3Dpip%3B%20s_pv_cmpgn%3D%3B%20s_pv_pVer%3D%3B%20stsh%3D%3B; _pxde=89dc46796681659bd423e59c6d2464e712127c11b46a090eaff8c0d96def0f7c:eyJ0aW1lc3RhbXAiOjE2NjYyMDI3MDY3NDd9; s_pers=%20productnum%3D16%7C1668794676609%3B%20s_nr365%3D1666203020554-Repeat%7C1697739020554%3B%20s_dslv%3D1666203020559%7C1760811020559%3B; s_sq=homedepotglobalproduction%3D%2526c.%2526a.%2526activitymap.%2526page%253Dproductdetails%25253E316914084%2526link%253DUpdate%2526region%253Dzip-code-availability-form%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253Dproductdetails%25253E316914084%2526pidt%253D1%2526oid%253DUpdate%2526oidt%253D3%2526ot%253DSUBMIT; _abck=95158423A4414B8293D53F462A02E5D3~-1~YAAQRRAgF7xMrNWDAQAAndp88Qjjy4Lir23E+azXxGcLWzU3eaDOZ8Qt945+6os+BGIDNcnl4dN+oz8Fq6aYcfFPFZOJv1ZyzVqDfj+FFYQqvJVdZz0Z0Y2q1lSrBpdAoCvI38fy9l2C4VRHaeg1Okwm9k8LW/6Y05MSyoBSuDtg+z+Esveq9Yf8xWULTtYnDUuF0jf7vpDbIQvinJ14+eK4zmuGDTfrLNy088m2MyOZPqolIol33YsQWBhkxvAQK12gygqUu+vyiIl+QO4sbEuKDyj0hhtFCysbh6G9Io8eIS2h4pX6t7YqwJY9EjuD8gBNASCLC2qD20PlIGGl5paCJg2u9MAU1/vEtom6U2EskO4iSf1dU4TlVFTCtaLXC+FbnzxtVGUT/WZV+MQLlezSYO+RoVzgVWo=~0~-1~-1',
        'origin': 'https://www.homedepot.com',
        'referer': link,
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'x-api-cookies': '{"x-user-id":"50d02070-e41e-47fd-12f9-74b5660be793"}',
        'x-current-url': link.split('homedepot.com')[-1],
        'x-debug': 'false',
        'x-experience-name': 'general-merchandise',
        'x-hd-dc': 'origin'
    }

    r = requests.request("POST", url, headers=headers, data=payload)

    data = json.loads(r.text)
    print(data)
    zip_code = data['data']['shipping']['zipCode']
    is_available_at_location = data['data']['shipping']['services'][0]['locations'][0]['inventory']['isInStock']
    if len(data['data']['shipping']['services']) == 1:
        type_of_delivery = 'Send to Home' if data['data']['shipping']['services'][0][
                                                 'type'] == 'sth' else "No home delivery"
    else:
        type_of_delivery = 'Send to Home' if data['data']['shipping']['services'][1][
                                                 'type'] == 'sth' else "No home delivery"
    retailer = headers.get('authority')
    product_name = headers.get('x-current-url').split('/')[-2]

    return retailer, product_name, zip_code, f"In-stock - {is_available_at_location}", type_of_delivery

#
# product_link = 'https://www.homedepot.com/p/Klein-Tools-Bluetooth-Jobsite-Earbuds-AESEB1/316914084'
#
# print(get_hd_shipment_status(product_link, 97217))

#
# try:
#     while True:
#         time.sleep(300)
# except Exception as e:
#     print(e)
