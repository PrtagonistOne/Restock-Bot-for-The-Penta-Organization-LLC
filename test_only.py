# # string = '"operationName":"shipping","variables":{"itemId":"316914084","price":73,"quantity":1,"storeId":"121","zipCode":"97217"},"query":"query shipping($itemId: String!, $storeId: String, $zipCode: String, $quantity: Int!, $price: Float!) {\n  shipping(itemId: $itemId, storeId: $storeId, zipCode: $zipCode, quantity: $quantity, price: $price) {\n    itemId\n    state\n    excludedShipStates\n    zipCode\n    services {\n      deliveryTimeline\n      deliveryDates {\n        startDate\n        endDate\n        __typename\n      }\n      deliveryCharge\n      dynamicEta {\n        hours\n        minutes\n        __typename\n      }\n      freeDeliveryThreshold\n      hasFreeShipping\n      locations {\n        distance\n        inventory {\n          isOutOfStock\n          isInStock\n          isLimitedQuantity\n          isUnavailable\n          quantity\n          __typename\n        }\n        isAnchor\n        locationId\n        storeName\n        storePhone\n        type\n        __typename\n      }\n      type\n      totalCharge\n      mode {\n        code\n        desc\n        group\n        longDesc\n        __typename\n      }\n      isDefault\n      __typename\n    }\n    __typename\n  }\n}\n"'
# #
# # string.replace('\n', '')
# #
# # print(string)
#
# import time
#
# import asyncio
#
# async def print_cube():
#     while True:
#         print('every 3 second')
#         await asyncio.sleep(3)
#
#
# async def print_square():
#     c = 1
#     while True:
#         print(f'every {c} second')
#         await asyncio.sleep(1)
#         c += 1
#
#
# async def async_print():
#     while True:
#         pr_str = input('Say someth: ')
#         print(pr_str)
#         if pr_str == 'q':
#             break
#
#
# if __name__ == "__main__":
#     loop = asyncio.get_event_loop()
#
#     asyncio.ensure_future(print_cube())
#     asyncio.ensure_future(print_square())
#     asyncio.ensure_future(async_print())
#
#     loop.run_forever()
#
# url = 'https://www.lowes.com/pd/Jasco-8-ft-USB-to-USB-C-Cable/1001073408'
# url = url.split('/')
# print(f'https://www.lowes.com/pd/{url[-1]}/productdetail/2383/Guest')
from utils.db_handlers import check_for_the_same_entry

check_for_the_same_entry(
    'https://www.homedepot.com/p/skullcandy-sesh-in-ear-anc-noise-canceling-true-wireless-stereo-bluetooth-earbuds'
    '-with-microphone-in-true-black-s2tew-p740/321137680',
    19713)
