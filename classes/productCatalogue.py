from product import Product, Brand, Category
from database import Database

class ProductCatalogue:
    def __init__(self, db: Database):
        self.db = db
        self.brandFilter = [b for b in Brand]
        self.categoryFilter = [c for c in Category]

    def _fetchAllProducts(self):
        if not self.db.state:
            print("❌ Not connected to database.")
            return []

        query = "SELECT ProductID, Name, Description, Price, StockQuantity, CategoryID, BrandID FROM ProductGood"
        rows = self.db.query(query)

        products = []
        for row in rows:
            try:
                product = Product.from_db_row(row)
                products.append(product)
            except Exception as e:
                print(f"⚠️ Skipped row {row} due to error: {e}")
        return products

    def addProduct(self, p: Product) -> bool:
        if not self.db.state:
            print("❌ Not connected to database.")
            return False
        query = """
            INSERT INTO ProductGood (Name, Description, Price, StockQuantity, CategoryID, BrandID)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            p.get_name(),
            p.get_description(),
            p.get_price(),
            p.get_quantity(),
            p.get_category_id(),
            p.get_brand_id()
        )
        result = self.db.query(query, params)
        return result 

    def removeProduct(self, productId: int) -> bool:
        if not self.db.state:
            print("❌ Not connected to database.")
            return False
        query = "DELETE FROM ProductGood WHERE ProductID = %s"
        result = self.db.query(query, (productId,))
        return result

    def fetchProductDetail(self, productId: int):
        products = self._fetchAllProducts()
        return next((p for p in products if p.get_id() == productId), None)

    def browseCatalogue(self):
        products = self._fetchAllProducts()
        categories = set(p.get_category() for p in products if p.get_brand() in self.brandFilter)
        return list(categories)

    def searchProduct(self, keyword: str):
        keyword = keyword.lower()
        products = self._fetchAllProducts()
        return [
            p for p in products
            if (
                keyword in p.get_name().lower()
                or keyword in p.get_description().lower()
                or keyword in p.get_brand().name.lower()
                or keyword in p.get_category().name.lower()
            )
            and p.get_brand() in self.brandFilter
            and p.get_category() in self.categoryFilter
        ]


    def modifyProductDetails(self, accountPrivilege: int) -> bool:
        return accountPrivilege >= 1

    def modifyProductDetailsUI(self):
        print("\n# ==================================================\nMODIFY PRODUCT DETAILS\n# ==================================================\n")
        try:
            pid = int(input("Enter Product ID to modify or [0] to return: "))
        except:
            print("Invalid input.")
            return
        if pid == 0:
            return
        product = self.fetchProductDetail(pid)
        if not product:
            print("❌ Product not found.")
            return

        print(f"\nCurrent Info:\n{product}\n")
        print("[1] Update Price\n[2] Update Stock\n[3] Update Description\n[4] Update Brand\n[5] Update Category\n[0] Return to main page")
        choice = input("Enter choice: ").strip()

        query = ""
        params = ()

        if choice == "1":
            new_price = float(input("Enter new price: "))
            query = "UPDATE ProductGood SET Price = %s WHERE ProductID = %s"
            params = (new_price, pid)
        elif choice == "2":
            new_stock = int(input("Enter new stock: "))
            query = "UPDATE ProductGood SET StockQuantity = %s WHERE ProductID = %s"
            params = (new_stock, pid)
        elif choice == "3":
            new_desc = input("Enter new description: ")
            query = "UPDATE ProductGood SET Description = %s WHERE ProductID = %s"
            params = (new_desc, pid)
        elif choice == "4":
            for b in Brand:
                print(f"[{b.value}] {b.name}")
            new_brand = int(input("Enter new brand: "))
            query = "UPDATE ProductGood SET BrandID = %s WHERE ProductID = %s"
            params = (new_brand, pid)
        elif choice == "5":
            for c in Category:
                print(f"[{c.value}] {c.name}")
            new_cat = int(input("Enter new category: "))
            query = "UPDATE ProductGood SET CategoryID = %s WHERE ProductID = %s"
            params = (new_cat, pid)
        elif choice == "0":
            return
        else:
            print("❌ Invalid choice.")
            return

        result = self.db.query(query, params)
        if result:
            print("✅ Product updated successfully.")
        else:
            print("❌ Failed to update product.")

    def productUI(self):
        products = self._fetchAllProducts()
        filtered = [p for p in products if p.get_brand() in self.brandFilter and p.get_category() in self.categoryFilter]

        output = "\n# ==================================================\n"
        output += "                PRODUCT CATALOGUE\n"
        output += "# ==================================================\n\n"

        if not filtered:
            output += "No products available.\n"
        else:
            for product in filtered:
                output += str(product) + "\n\n"

        output += "--------------------------------------------------\n"
        print(output)

    def addProductUI(self):
        print("\n# ==================================================\nADD NEW PRODUCT\n# ==================================================\n")
        name = input("Enter Product Name    : ")
        print("Available Brands:")
        for b in Brand:
            print(f"[{b.value}] {b.name}")
        brand_input = int(input("Enter Brand           : "))
        brand = Brand(brand_input)

        print("Available Categories:")
        for c in Category:
            print(f"[{c.value}] {c.name}")
        category_input = int(input("Enter Category        : "))
        category = Category(category_input)

        description = input("Enter Description     : ")
        price = float(input("Enter Price ($)       : "))
        quantity = int(input("Enter Initial Stock   : "))

        confirm = input("\nConfirm add product? (y/n): ").strip().lower()
        if confirm == 'y':
            product = Product(name, description, price, quantity, category, brand)
            if self.addProduct(product):
                print(f"\nProduct \"{product.get_name()}\" added successfully.")
            else:
                print("❌ Failed to add product.")
        else:
            print("Product not added.")

    def removeProductUI(self):
        print("\n# ==================================================\nREMOVE PRODUCT\n# ==================================================\n")
        products = self._fetchAllProducts()
        for p in products:
            print(f"[{p.get_id()}] {p.get_name()}")
        try:
            pid = int(input("Enter Product ID to remove or [0] to return: "))
        except:
            print("Invalid input.")
            return
        if pid == 0:
            return
        confirm = input("Are you sure you want to remove it? (y/n): ").strip().lower()
        if confirm == 'y':
            if self.removeProduct(pid):
                print("✅ Product removed.")
            else:
                print("❌ Failed to remove.")

    def fetchProductDetailsUI(self):
        print("\n# ==================================================\nPRODUCT DETAILS\n# ==================================================\n")
        try:
            pid = int(input("Enter Product ID to view or [0] to return: "))
        except:
            print("Invalid input.")
            return
        if pid == 0:
            return
        product = self.fetchProductDetail(pid)
        if product:
            print(product)
        else:
            print("❌ Product not found.")

    def searchProductUI(self):
        print("\n# ==================================================")
        print("               SEARCH PRODUCT BY KEYWORD")
        print("# ==================================================\n")
        
        keyword = input("Enter product name or keyword: ").strip().lower()
        if not keyword:
            print("❌ No keyword entered.")
            return

        results = self.searchProduct(keyword)

        if not results:
            print("❌ No matching products found.\n")
            return

        print("\nResults:")
        for product in results:
            print(f"\n[{product.get_id()}] {product.get_name()}")
            print(f"Brand     : {product.get_brand().name}")
            print(f"Category  : {product.get_category().name}")
            print(f"Price     : ${product.get_price():.2f}")
            print(f"Stock     : {product.get_quantity()}")
            print(f"Description: {product.get_description()}")
        
        print("\n--------------------------------------------------")



# ===== MAIN TESTING =====
if __name__ == "__main__":
    db = Database("s104354565_db", user="s104354565", password="Ping13749&&")

    if db.connect("s104354565_db"):
        catalogue = ProductCatalogue(db)
        catalogue.productUI()
        #catalogue.fetchProductDetailsUI()
        # catalogue.addProductUI()
        # catalogue.removeProductUI()
        catalogue.searchProductUI()
        #catalogue.browseCatalogue()
        #catalogue.modifyProductDetailsUI()
        db.disconnect("s104354565_db")
