import json

with open('data.json', 'r') as f:
    data = json.load(f)


# zip_code = data['data']['shipping']['zipCode']
# is_available_at_location = data['data']['shipping']['services'][0]['locations'][0]['inventory']['isInStock']
# type_of_delivery = 'Send to Home' if data['data']['shipping']['services'][0]['type'] == 'sth' else "No home delivery"

is_available_to_pick_up = data['inventory']['inventoryDisplay']['pickup']['availabilityStatus']
to_be_delivered = data['inventory']['inventoryDisplay']['delivery']['availabilityStatus']

print(is_available_to_pick_up, to_be_delivered)
