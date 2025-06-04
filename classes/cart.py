import itertools
from classes.cartItem import CartItem
from classes.payment import Payment
from classes.order import Order, OrderStatus

class Cart:
    def __init__(self, customerID):
        self.customer_id = customerID
        self._items: list[CartItem] = []

    def _reassignIDs(self):
        for idx, item in enumerate(self._items, start=1):
            item.setCartItemID(idx)

    # def _fetchCartRows(self):
    #     select_sql = """
    #         SELECT CartItemID, ProductID, Quantity
    #           FROM cart_item
    #          WHERE CustomerID = %s;
    #     """
    #     raw = self.db.query(select_sql, (self.customer_id,))
    #     if not isinstance(raw, list):
    #         return []
    #     rows = []
    #     for row in raw:
    #         if isinstance(row, dict):
    #             rows.append({
    #                 'CartItemID': row.get('CartItemID'),
    #                 'ProductID' : row.get('ProductID'),
    #                 'Quantity'  : row.get('Quantity')
    #             })
    #         else:
    #             cid, pid, qty = row
    #             rows.append({
    #                 'CartItemID': cid,
    #                 'ProductID' : pid,
    #                 'Quantity'  : qty
    #             })
    #     return rows

    def addToCart(self, product: dict, quantity: int):
        pid = product["id"]
        if quantity <= 0:
            return False

        for item in self._items:
            if item.getProduct()["id"] == pid:
                item.changeQuantity(item.getQuantity() + quantity)
                self._reassignIDs()
                return True

        new_item = CartItem(product, quantity)
        self._items.append(new_item)

        self._reassignIDs()
        return True
    
    def removeCartItem(self, cartItemID):
        for idx, item in enumerate(self._items):
            if item.getCartItemID() == cartItemID:
                del self._items[idx]
                self._reassignIDs()
                return True
        return False
    
    def selectCartItem(self, cartItemID):
        for item in self.__cartItems:
            if item.getCartItemID() == cartItemID:
                return item
        return None
    
    def getCartItems(self):
        return list(self._items)
    
    def checkout(self):
        if not self._items:
            return 0
        total = sum(item.getTotalPrice() for item in self._items)
        self._items.clear()
        self._reassignIDs()
        return total
    