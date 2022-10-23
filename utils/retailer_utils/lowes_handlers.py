import requests
import json


def get_lowes_shipment_status(link: str):

    url = link.split('/')
    url.pop()
    url = ''.join(url)
    headers = {
        "cookie": 'region=east; AKA_A2=A; bm_sz=14A0211F061B03C327768A1CAE69BA84~YAAQiIIsF83ueuiDAQAAGrQu9hGV8s6m'
                  '+w3XvFnMZ3nEW8urhckyRnyXKMn/l68WJE/GDtHMpifqoIP+T0iSyV0XGdtt2tCf5vuzn5fj+B4Sg9Umimn0Pb2rsDLSH8'
                  '/gEDAGQGeBVbaSYiFe6uw3edT2DaEZWIPFEsAQFLOTeDoVVOwFL2UEsMRsUx5YWIPkhcyE69HiI+s5KWDD//yiVeIZdV'
                  '+AYJLW0rZTkRpeo+K4QeKA1oOJsQXphz/7pXIyl83RQaBWvhIu2yOKLXsrvGW7UQK/eYCAbs2VQADFMM47xQ==~3163448~4403524'
                  '; dbidv2=e6956729-e7d5-4ef3-81c1-3cde6f376516; '
                  'al_sess=FuA4EWsuT07UWryyq/3foLNQrtG+fkPHcP13Hu6liywMuye12gApaPWotKQgicr8; '
                  'EPID=ZTY5NTY3MjktZTdkNS00ZWYzLTgxYzEtM2NkZTZmMzc2NTE2; sn=2383; sd=[object Object]; '
                  'discover-exp-1=abt10789b; purchase-test-checkout-version=cic; discover-exp-2=abt9613b; '
                  'discover-exp-3=abt10951c; AMCVS_5E00123F5245B2780A490D45%40AdobeOrg=1; g_amcv_refreshed=1; '
                  '_lgsid=1666282602781; fs_uid=#Q8RZE#5627571563106304:6190376573964288:::#360b21a7#/1697818602; '
                  'fs_cid=1.0; AMCV_5E00123F5245B2780A490D45%40AdobeOrg=-1303530583%7CMCIDTS%7C20017%7CMCMID'
                  '%7C74806438674993025600995114644267407225%7CMCAAMLH-1666887404%7C7%7CMCAAMB-1666887404'
                  '%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1666289804s%7CNONE%7CvVersion%7C3.3'
                  '.0; _gcl_au=1.1.25047124.1666282604; REVLIFTER={"w":"0l554347-da15-447f-9091-6e8941024cdc",'
                  '"u":"d1962878-14a5-46d0-9495-0bcd941007dd","s":"d2405668-4fd7-4390-a209-bc98f11b752e",'
                  '"se":1668874606}; _pin_unauth=dWlkPVpEWmhPRFl5TlRndE56Z3dOQzAwWVdNeExUazRNakF0TjJReE0yVXpPVEJsWkRneA; '
                  'IR_gbd=lowes.com; _abck=E19AA0C86B330D0A8AD5964D707164E6~0~YAAQiIIsF'
                  '+T7euiDAQAApd8u9giaT9lXUsw7Nck0Hh30AzVjubI4uXMvSAJdB6e6f/nXdOfUyAYzG'
                  '/N8d6LwrZYGKgsx49Kcy7ldGeQK0cXkTO9bPIVxA9ah+A19HMv4xPcec51l3o1UMH8bbzMWbUw1dusS8L'
                  '+1jaXXoP5VeHsXZplys8pWSjngpCq9Cpys+GCZI/MFwFJ4BKQyCtdHu5sy9UqaGeBpOT8B92dHp1m6ot+CYJY5hCsZoeuaxRY'
                  '/BXVByyT3AbygkzO2PmN1DzDb8yv2ShmByUhx+Irox8EZ+39FU3z'
                  '+/0pI8wGzPcE6OMjojJP03HDei7fOyzXCYWNdzLmXr1WdmUGXrHZTLkYisCIiIr8REREkCeGCB44XYbw4hEgBWNEhxS0F7z695e3oSWB4tfPFbQB8Ww+PIgB5cXG/lmJLTUwc4cRm9fk0HGbOJznt2g==~-1~-1~-1; p13n=%7B%22zipCode%22%3A%2206416%22%2C%22storeId%22%3A%222383%22%2C%22state%22%3A%22CT%22%2C%22audienceList%22%3A%5B%5D%7D; mdLogger=false; kampyle_userid=4574-1ef9-3048-7ea5-e8b8-b61a-2a2a-d6c8; kampyleUserSession=1666282616548; kampyleUserSessionsCount=1; kampyleUserPercentile=21.089975295482375; _tt_enable_cookie=1; _ttp=e346a0a9-fe3d-4579-aba4-295b6eb54e49; _clck=1kzz5k8|1|f5v|0; LPVID=Y5OTVlYTY3NDJjZWE1Nzc4; LPSID-22554410=3BeJxgJZTzyTv9QGCOK9mw; ak_bmsc=2C5AA7AF94CC70200C03773C8B94D75C~000000000000000000000000000000~YAAQl4IsF3wSFPaDAQAAPCox9hHI0zpV4NNQhplGVdEcJtUTApaiTmEvk117WYNJ1YGQ2U4draObjruoqFMn+Z3MiQsq8Sp7y0PbmTAxm0TeyYHUxs/u9M75RbNjbDB9nWYVJnoQC/UFS2J8D9ZBfKYrAngta8Xu+Mjb1ROUdPp4bJ4x0IUOdBMLZTLTwyJVIFZ0MZ5mgNCHJYweXMev1LViJ4BhJe2APhRj+cvXKyXIV1+NyXAPcz2LZ9gKxu9VUkijBpjT4vt4DfvUsXwkkpSPiQHkbSl4Qw7Z1VL68zCYX6GudhVRLjCn9qSmPyMHmzStFFvRAK+ZRJXlO2tw0wBfSItVO86KGUi4AYLQfV2YTCTWZJzoH7PdHBC2y8hHX3AiB0siJL+rFRQOpVqSSuyxtji51hpgCStW5ZJcSuUwJzzGXYnjynJoogIevc/9HcNeQlDA5xcReQQ8PRt6/vdHK/EX9F7F1ZBGwPUYKNQTmMJdFaVD/Jk3yjVdTpNqty0tr8cSRF87h5GNrk8il4+dholmyb4/WyMBC9cHOUPipnTlTU3itpvYCt/T; prodNumber=3; notice_behavior=implied,eu; akavpau_cart=1666283076~id=461472ee7cde646cbe6964d97cc5221f; salsify_session_id=39adf710-966e-4898-a57f-42e71c391fc0; IR_12374=1666282785787%7C0%7C1666282785787%7C%7C; g_previous=%7B%22gpvPageLoadTime%22%3A%220.00%22%2C%22gpvPageScroll%22%3A%2215%7C22%7C7%7C6702%22%2C%22gpvSitesections%22%3A%22electrical%2Celectronics%2Caudio%2Cheadphones%22%2C%22gpvSiteId%22%3A%22desktop%22%2C%22gpvPageType%22%3A%22product-display%22%7D; kampyleSessionPageCounter=4; ecrSessionId=48BDBCF273B4A0318258E6E5A8F01DE5; _uetsid=9fa1bfa0509211ed995b25aaaeaff008; _uetvid=9fa207c0509211ed9908ffe512e5e5f0; _clsk=1a8mc3e|1666282787682|4|0|h.clarity.ms/collect; BVBRANDID=0e652ec4-32b8-49fd-b046-b4bfaf51e3e3; BVBRANDSID=2145ca3c-6c29-4c68-9e86-106808e8a1fc; bm_sv=656ABEFF6441E3D8A6CBBB0DDDF49242~YAAQl4IsF0T1FPaDAQAA+3Qy9hFboqmAhuxE7MskdyWzv/A90iBEH6Y1W3+noRMtRn+OxdnfYPii7BLMz2e0juEhh8F1E5Lcm9Ns/3yCqD3jr8HjTaP7m0zawnurnjI1GsMj1OvgOBtxJ7HUevwdvv3l2Jg6suDTONuFcppkQZyIQz1LNSm+eOqpjK+e+9eYIsnHrQgV9vT/0Jh3lL+KgvpIgPfcHirf4HBEMJEtFNuOzzfZwqYpK+wWj9RZ8dVf~1; akavpau_default=1666283187~id=9c0b5eea1655429998af3202c21bd16e; akaalb_prod_dual=1666369287~op=PROD_GCP_EAST_CTRL_DFLT:PROD_DEFAULT_EAST|~rv=67~m=PROD_DEFAULT_EAST:0|~os=352fb8a62db4e37e16b221fb4cefd635~id=622ec67a59202f44ec8d4105d97fc6e8; RT="z=1&dm=lowes.com&si=e9a85e18-67e3-45b9-b79d-22f680a1dea8&ss=l9h9mxll&sl=6&tt=hd4&bcn=%2F%2F173bf104.akstat.io%2F&ld=409t&nu=9y8m6cy&cl=4j99&ul=66o9&hd=677n"',
        'authority': "www.lowes.com",
        'accept': "application/json, text/plain, */*",
        'accept-language': "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,la;q=0.6",
        'referer': link,
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': "?0",
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': "empty",
        'sec-fetch-mode': "cors",
        'sec-fetch-site': "same-origin",
        'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
    }

    r = requests.request("GET", 'https://www.lowes.com/pd/1001181690/productdetail/2383/Guest', headers=headers)
    print(r.text)
    data = json.loads(r.text)
    pick_up = data['inventory']['inventoryDisplay']['pickup']['availabilityStatus']
    to_be_delivered = data['inventory']['inventoryDisplay']['delivery']['availabilityStatus']

    retailer = headers.get('authority')
    product_name = headers.get('referer')

    return retailer, product_name, 'No location specified', f"In-stock - {pick_up or to_be_delivered}", \
           f'Pick up - {pick_up}, Delivery - {to_be_delivered}'
