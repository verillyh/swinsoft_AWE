from product import Product, Brand, Category

class ProductCatalogue:
    def __init__(self):
        self.allProducts = []

    def addProduct(self, p: Product) -> bool:
        if isinstance(p, Product):
            self.allProducts.append(p)
            return True
        return False

    def productUI(self):
        output = "\n# ==================================================\n"
        output += "                PRODUCT CATALOGUE\n"
        output += "# ==================================================\n\n"

        if not self.allProducts:
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


# ================== MAIN ==================

if __name__ == "__main__":
    catalogue = ProductCatalogue()

    # Preload sample products
    catalogue.addProduct(Product("TV", "4K Smart LED TV", 899.99, 8, Category.Television, Brand.A))
    catalogue.addProduct(Product("Phone", "Latest 5G model", 1099.50, 12, Category.MobilePhone, Brand.B))
    catalogue.addProduct(Product("Laptop", "Gaming powerhouse", 1999.00, 5, Category.Computer, Brand.C))

    # Display product UI
    catalogue.productUI()

   

    # Add new product interactively
    catalogue.addProductUI()
