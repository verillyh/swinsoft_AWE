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

    def __row_to_product(self, row: tuple, db):
        (product_id, product_name, product_desc, unit_price, stock_qty, cat_name, brand_name) = row
        CategoryEnum = Category(db)
        if cat_name in CategoryEnum.__members__:
            category_enum = CategoryEnum[cat_name]
        else:
            category_enum = next(iter(CategoryEnum))

        BrandEnum = Brand(db)
        if brand_name in BrandEnum.__members__:
            brand_enum = BrandEnum[brand_name]
        else:
            brand_enum = next(iter(BrandEnum))

        return Product(product_name, product_desc, unit_price, stock_qty, category_enum, brand_enum, product_id)
    
    def remove_product(self, productID: int, db):
        try:
            pid = int(productID)
        except ValueError:
            return False

        delete_sql = f"DELETE FROM productgood WHERE ProductID = {pid};"
        result = db.query(delete_sql)
        return True

    def add_product(self, productName: str, productDesc: str, unitPrice: float, quantity: int, category: Category, brand: Brand, db):
        name_esc = productName.replace("'", "''")
        desc_esc = productDesc.replace("'", "''")
        cat_name = category.value
        brand_name = brand.value

        insert_sql = """
            INSERT INTO productgood
              (Name, Description, UnitPrice, StockQuantity, CategoryID, BrandID)
            VALUES
              (%s, %s, %s, %s, %s, %s);
        """
        params = (name_esc, desc_esc, unitPrice, quantity, cat_name, brand_name)
        success = db.query(insert_sql, params)
        if not success:
            print("SQL error: could not insert new product.")
            return None

        row = db.query("SELECT LAST_INSERT_ID();")
        if not isinstance(row, list) or len(row) == 0:
            print("Error fetching new ProductID.")
            return None

        first = row[0]
        if isinstance(first, tuple):
            new_product_id = first[0]
        elif isinstance(first, dict):
            new_product_id = list(first.values())[0]
        else:
            print("Unexpected format for LAST_INSERT_ID.")
            return None

        new_product = Product(
            name=productName,
            description=productDesc,
            price=unitPrice,
            quantity=quantity,
            category=category,
            brand=brand,
            productID=new_product_id
        )
        return new_product
    
    def fetch_all_products(self, db):
        select_sql = """
        SELECT 
            pg.ProductID,
            pg.Name,
            pg.Description,
            pg.UnitPrice,
            pg.StockQuantity,
            c.CategoryName,
            b.BrandName 
        FROM productgood pg
        JOIN category c ON pg.CategoryID = c.CategoryID
        JOIN brand b ON pg.BrandID = b.BrandID;
        """
        raw = db.query(select_sql)

        if not isinstance(raw, (list, tuple)):
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
                        row["UnitPrice"],
                        row["StockQuantity"],
                        row["CategoryName"],
                        row["BrandName"]
                    )
                except KeyError:
                    continue
            else:
                continue
            prod_obj = self.__row_to_product(tup, db)
            products.append(prod_obj)
        return products
    
    def fetch_product_detail(self, keyword: str, db):
        kw = keyword.strip().lower().replace("'", "''")
        select_sql = f"""
        SELECT 
            pg.ProductID,
            pg.Name,
            pg.Description,
            pg.UnitPrice,
            pg.StockQuantity,
            c.CategoryName,
            b.BrandName
        FROM productgood pg
        JOIN category c ON pg.CategoryID = c.CategoryID
        JOIN brand b ON pg.BrandID = b.BrandID
        WHERE 
        LOWER(pg.Name)              LIKE '%{kw}%' 
        OR LOWER(pg.Description)    LIKE '%{kw}%' 
        OR LOWER(c.CategoryName)    LIKE '%{kw}%' 
        OR LOWER(b.BrandName)       LIKE '%{kw}%';
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
                        row["UnitPrice"],
                        row["StockQuantity"],
                        row["CategoryName"],
                        row["BrandName"],
                    )
                except KeyError:
                    continue
            else:
                continue
            prod_obj = self.__row_to_product(tup, db)
            matches.append(prod_obj)
        return matches
    
    def fetch_product_by_id(self, productID: int, db):
        try:
            pid = int(productID)
        except (ValueError, TypeError):
            return None

        select_sql = """
            SELECT
                pg.ProductID,
                pg.Name,
                pg.Description,
                pg.UnitPrice,
                pg.StockQuantity,
                c.CategoryName,
                b.BrandName
            FROM productgood pg
            JOIN category c ON pg.CategoryID = c.CategoryID
            JOIN brand b ON pg.BrandID = b.BrandID
            WHERE pg.ProductID = %s
            LIMIT 1;
        """
        params = (pid,)
        raw = db.query(select_sql, params)

        if not isinstance(raw, list) or len(raw) == 0:
            return None

        row = raw[0]

        if isinstance(row, tuple) and len(row) == 7:
            return self.__row_to_product(row, db)

        if isinstance(row, dict):
            try:
                pid_val        = row["ProductID"]
                name           = row["Name"]
                description    = row["Description"]
                unit_price     = row["UnitPrice"]
                stock_qty      = row["StockQuantity"]
                category_str   = row["CategoryName"]
                brand_str      = row["BrandName"]
            except KeyError:
                return None

            CategoryEnum = Category(db)
            BrandEnum = Brand(db)
            return Product(
                name=name,
                description=description,
                price=float(unit_price),
                quantity=int(stock_qty),
                category=CategoryEnum[category_str] if category_str in CategoryEnum.__members__ else next(iter(CategoryEnum)),
                brand=BrandEnum[brand_str] if brand_str in BrandEnum.__members__ else next(iter(BrandEnum)),
                productID=pid_val
            )
        return None
    
    def modify_product(self, productID: int, field, newValue, db):
        try:
            pid = int(productID)
        except ValueError:
            return None

        if field == "Category":
            update_sql = """
                UPDATE productgood
                SET CategoryID = (SELECT CategoryID FROM category WHERE CategoryName = %s)
                WHERE ProductID = %s;
            """
            params = (newValue.name, pid)
        elif field == "Brand":
            update_sql = """
                UPDATE productgood
                SET BrandID = (SELECT BrandID FROM brand WHERE BrandName = %s)
                WHERE ProductID = %s;
            """
            params = (newValue.name, pid)
        else:
            col = "UnitPrice" if field == "Price" else field
            update_sql = f"UPDATE productgood SET `{col}` = %s WHERE ProductID = %s;"
            params     = (newValue, pid)

        result = db.query(update_sql, params)
        return True
