
from product import Product  

class ProductCatalogue:
    def __init__(self):
        self.allProducts = []  # List[Product]

    def addProduct(self, p):
        if isinstance(p, Product):
            self.allProducts.append(p)
            return True
        return False

    def removeProduct(self, productId):
        for product in self.allProducts:
            if product.id == productId:
                self.allProducts.remove(product)
                return True
        return False

    def fetchProductDetail(self, productId):
        for product in self.allProducts:
            if product.id == productId:
                return product
        return None

    def browseCatalogue(self):
        categories = set()
        for product in self.allProducts:
            categories.add(product.category)
        return list(categories)

    def searchProduct(self, desc):
        return [product for product in self.allProducts if desc.lower() in product.description.lower()]

    def modifyProductDetails(self, accountPrivilege):
        # Example: only modify if accountPrivilege is above a threshold
        if accountPrivilege >= 1:
            # Placeholder logic; actual modifications would need more input
            return True
        return False
