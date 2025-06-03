from classes.product import Product, Brand, Category

class ProductCatalogue:
    def __init__(self):
        self.allProducts: Product = []

    def removeProduct(self, prod_id: int) -> bool:
        for p in self.allProducts:
            if prod_id == p.id:
                self.allProducts.remove(p)
                return True
            else:
                return False

    def addProduct(self, p: Product) -> bool:
        if isinstance(p, Product):
            self.allProducts.append(p)
        else:
            return False
    
    def fetchProductDetail(self, productId: int):
        for product in self.allProducts:
            if product.id == productId:
                return product
        return None  # Return None if no matching product is found

    def productUI(self):
        output = "\n# ==================================================\n"
        output += "                PRODUCT CATALOGUE\n"
        output += "# ==================================================\n\n"

        if len(self.allProducts) == 0:
            output += "No products available.\n"
        else:
            for product in self.allProducts:
                output += str(product) + "\n\n"

        output += "--------------------------------------------------\n"
        print(output)

    def addProductUI(self):
        add = ""  # initialize string for building output

        add += ("\n# ==================================================\n")
        add += ("                ADD NEW PRODUCT\n")
        add += ("# ==================================================\n\n")

        name = input("Enter Product Name    : ")

        add += "Available Brands:\n"
        for b in Brand:
            add += f"[{b.value}] {b.name}\n"
        print(add)
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
            self.addProduct(product)
            print(f"\nProduct \"{product.name}\" added with ID: #{product.id}")
        else:
            print("\nProduct not added.")

    def removeProductUI(self):
        print("\n# ==================================================")
        print("                REMOVE PRODUCT")
        print("# ==================================================\n")

        show =""
        # Display current products
        for product in self.allProducts:
            
            show += str(product) + "\n\n"
        print(show)

        # Ask for product ID to remove
        try:
            product_id = int(input("Enter Product ID to remove or [0] to return home: "))
        except ValueError:
            print("❌ Invalid input. Please enter a valid number.")
            return

        if product_id == 0:
            print("Returning to home...\n")
            return

        # Search in product list
        product = self.fetchProductDetail(product_id)

        if product:
            confirm = input(f"Are you sure you want to remove \"{product.name}\"? (y/n): ").strip().lower()
            if confirm == 'y':
                self.removeProduct(product)
                print(f"\nProduct \"{product.name}\" removed successfully.")
            else:
                print("\nProduct removal cancelled.")
        else:
            print("\n❌ Product not found.\n")

    def fetchProductDetailsUI(self):
        print("\n# ==================================================")
        print("               SEARCH PRODUCT RESULT")
        print("# ==================================================\n")

        # Ask for product ID
        try:
            product_id = int(input("Enter Product ID to view details or [0] to return home: "))
        except ValueError:
            print("❌ Invalid input. Please enter a valid number.")
            return

        if product_id == 0:
            print("Returning to home...\n")
            return

        # Search in product list
        product = self.fetchProductDetail(product_id)

        if product:
            print(f"\n[{product.id}] {product.name}")
            print(f"Brand     : {product.brand.name}")
            print(f"Category  : {product.category.name}")
            print(f"Price     : ${product.price:.2f}")
            print(f"Stock     : {product.quantity}")
            print(f"Description: {product.description}")
            print("\n--------------------------------------------------")
        else:
            print("\n❌ Product not found.\n")



# ================== MAIN ==================

if __name__ == "__main__":
    catalogue = ProductCatalogue()

    # Preload sample products
    catalogue.addProduct(Product("TV", "4K Smart LED TV", 899.99, 8, Category.Television, Brand.A))
    catalogue.addProduct(Product("Phone", "Latest 5G model", 1099.50, 12, Category.MobilePhone, Brand.B))
    catalogue.addProduct(Product("Laptop", "Gaming powerhouse", 1999.00, 5, Category.Computer, Brand.C))

# Display product UI
#catalogue.productUI()

#catalogue.fetchProductDetailsUI()

# Add new product interactively
#catalogue.addProductUI()
# catalogue.removeProductUI()
