import uuid



def unique(product_id: str = str(uuid.uuid4())):
    return product_id

for _ in range(5):
    print(unique())

