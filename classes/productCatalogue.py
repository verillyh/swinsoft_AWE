from classes.product import Product, Brand, Category

class ProductCatalogue:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self._initialized = True

    def _row_to_product(self, row: tuple):
        (prod_id, name, description, price, stock_qty, cat_name, brand_name) = row
        try:
            category_enum = Category[cat_name]
        except (KeyError, TypeError):
            category_enum = Category.Television

        try:
            brand_enum = Brand[brand_name]
        except (KeyError, TypeError):
            brand_enum = Brand.BrandA

        return Product(name, description, price, stock_qty, category_enum, brand_enum)
    
    def removeProduct(self, productID: int, db):
        try:
            pid = int(productID)
        except ValueError:
            return False

        delete_sql = f"DELETE FROM productgood WHERE ProductID = {pid};"
        result = db.query(delete_sql)
        return True

    def addProduct(self, product: Product, db):
        if not isinstance(product, Product):
            return False

        name_esc        = product.name.replace("'", "''")
        desc_esc        = product.description.replace("'", "''")
        cat_name        = product.category.value
        brand_name      = product.brand.value
        price_val       = int(product.price)
        stock_val       = int(product.quantity)

        insert_sql = f"""
        INSERT INTO productgood (Name, Description, Price, StockQuantity, Category, Brand)
        VALUES (
            '{name_esc}',
            '{desc_esc}',
            {price_val},
            {stock_val},
            {cat_name},
            {brand_name}
        );
        """
        result = db.query(insert_sql)
        return True
    
    def fetchAllProducts(self, db):
        select_sql = """
        SELECT 
            ProductID,
            Name,
            Description,
            Price,
            StockQuantity,
            Category,
            Brand 
        FROM productgood
        """
        raw = db.query(select_sql)

        if not isinstance(raw, list):
            print("Warning: fetchAllProducts expected list of tuples but got", type(raw))
            return []

        products = []
        for row in raw:
            if isinstance(row, tuple) and len(row) == 7:
                tup = row
            elif isinstance(row, dict):
                try:
                    tup = (
                        row["ProductID"],
                        row["Name"],
                        row["Description"],
                        row["Price"],
                        row["StockQuantity"],
                        row["Category"],
                        row["Brand"]
                    )
                except KeyError:
                    continue
            else:
                continue
            prod_obj = self._row_to_product(tup)
            products.append(prod_obj)

        return products
    
    def fetchProductDetail(self, keyword: str, db):
        kw = keyword.strip().lower().replace("'", "''")
        select_sql = f"""
        SELECT 
            ProductID,
            Name,
            Description,
            Price,
            StockQuantity,
            Category,
            Brand
        FROM productgood
        WHERE 
        LOWER(Name)        LIKE '%{kw}%' 
        OR LOWER(Description) LIKE '%{kw}%' 
        OR LOWER(Category)    LIKE '%{kw}%' 
        OR LOWER(Brand)       LIKE '%{kw}%';
        """
        raw = db.query(select_sql)

        if not isinstance(raw, list) or len(raw) == 0:
            return []

        matches = []
        for row in raw:
            if isinstance(row, tuple) and len(row) == 7:
                tup = row
            elif isinstance(row, dict):
                try:
                    tup = (
                        row["ProductID"],
                        row["Name"],
                        row["Description"],
                        row["Price"],
                        row["StockQuantity"],
                        row["Category"],
                        row["Brand"],
                    )
                except KeyError:
                    continue
            else:
                continue
            prod_obj = self._row_to_product(tup)
            matches.append(prod_obj)

        return matches
    def fetchProductByID(self, productID: int, db):
        try:
            pid = int(productID)
        except (ValueError, TypeError):
            return None

        select_sql = """
            SELECT
                ProductID,
                Name,
                Description,
                Price,
                StockQuantity,
                Category,
                Brand
            FROM productgood
            WHERE ProductID = %s
            LIMIT 1;
        """
        params = (pid,)

        raw = db.query(select_sql, params)

        if not isinstance(raw, list) or len(raw) == 0:
            return None

        row = raw[0]

        if isinstance(row, tuple) and len(row) == 7:
            return self._row_to_product(row)

        if isinstance(row, dict):
            try:
                pid_val        = row["ProductID"]
                name           = row["Name"]
                description    = row["Description"]
                price          = row["Price"]
                stock_qty      = row["StockQuantity"]
                category_str   = row["Category"]
                brand_str      = row["Brand"]
            except KeyError:
                return None
            
            return Product(
                name=name,
                description=description,
                price=float(price),
                quantity=int(stock_qty),
                category=Category[category_str],
                brand=Brand[brand_str]
            )

        return None
    
    def modifyProduct(self, productID: int, field, newValue, db):
        try:
            pid = int(productID)
        except ValueError:
            return None

        update_sql = f"UPDATE productgood SET `{field}` = %s WHERE ProductID = %s;"
        params     = (newValue, pid)
        result = db.query(update_sql, params)

        return True
