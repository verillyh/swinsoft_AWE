from classes.product import Product, Brand, Category

class ProductCatalogue:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self.allProducts: list[Product] = []
            self._initialized = True

    def removeProduct(self, productID: int):
        for product in self.allProducts:
            if productID == product.id:
                self.allProducts.remove(product)
                return True
        return False

    def addProduct(self, product: Product) -> bool:
        if isinstance(product, Product):
            self.allProducts.append(product)
            return True
        return False
    
    def fetchProductDetail(self, keyword: str):
        keyword_lower = keyword.lower()
        matches = []

        for product in self.allProducts:
            if (keyword_lower in product.brand.name.lower() or
                keyword_lower in product.name.lower() or
                keyword_lower in product.category.name.lower() or
                keyword_lower in product.description.lower()):
                matches.append(product) 

        return matches  
