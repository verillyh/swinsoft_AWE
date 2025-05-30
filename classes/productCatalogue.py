from product import Product, Category

class ProductCatalogue:
    def __init__(self):
        self.allProducts = []  # List[Product]

    # + addProduct(p: Product): Boolean
    def addProduct(self, p: Product) -> bool:
        if isinstance(p, Product):
            self.allProducts.append(p)
            return True
        return False

    # + removeProduct(productId: int): Boolean
    def removeProduct(self, productId: int) -> bool:
        for product in self.allProducts:
            if product.id == productId:
                self.allProducts.remove(product)
                return True
        return False

    # + fetchProductDetail(productId: int): Product
    def fetchProductDetail(self, productId: int) -> Product:
        for product in self.allProducts:
            if product.id == productId:
                return product
        return None

    # + browseCatalogue(): List<Category>
    def browseCatalogue(self) -> list:
        categories = set()
        for product in self.allProducts:
            categories.add(product.category)
        return list(categories)

    # + searchProduct(desc: str): List<Product>
    def searchProduct(self, desc: str) -> list:
        desc = desc.lower()
        return [
            product for product in self.allProducts
            if desc in product.description.lower()
        ]

    # + modifyProductDetails(accountPrivilege: int): Boolean
    def modifyProductDetails(self, accountPrivilege: int) -> bool:
        return accountPrivilege >= 1
