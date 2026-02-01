"""
Baseline Naïve Order Book Implementation

This implementation uses simple Python lists and sorts after each modification.
"""


class NaiveOrderBook:
    """
    A naïve order book implementation using two Python lists.
    Orders are stored as dictionaries and lists are sorted after each modification.
    """
    
    def __init__(self):
        """Initialize empty bid and ask lists."""
        self.bids = []
        self.asks = []
    
    def add_order(self, order_dict):
        """
        Add an order to the appropriate list and sort.
        
        Args:
            order_dict: Dictionary with keys:
                - order_id (int): Unique order identifier
                - price (float): Order price
                - quantity (int): Order quantity
                - side (str): "bid" or "ask"
        """
        if order_dict["side"] == "bid":
            self.bids.append(order_dict)
            # Sort bids descending by price (highest first)
            self.bids.sort(key=lambda x: x["price"], reverse=True)
        elif order_dict["side"] == "ask":
            self.asks.append(order_dict)
            # Sort asks ascending by price (lowest first)
            self.asks.sort(key=lambda x: x["price"])
        else:
            raise ValueError(f"Invalid side: {order_dict['side']}. Must be 'bid' or 'ask'")
    
    def amend_order(self, order_id, new_quantity):
        """
        Find an order by ID, update its quantity, and re-sort the list.
        
        Args:
            order_id (int): The ID of the order to amend
            new_quantity (int): The new quantity for the order
            
        Returns:
            bool: True if order was found and amended, False otherwise
        """
        # Search in bids
        for order in self.bids:
            if order["order_id"] == order_id:
                order["quantity"] = new_quantity
                # Re-sort bids descending by price
                self.bids.sort(key=lambda x: x["price"], reverse=True)
                return True
        
        # Search in asks
        for order in self.asks:
            if order["order_id"] == order_id:
                order["quantity"] = new_quantity
                # Re-sort asks ascending by price
                self.asks.sort(key=lambda x: x["price"])
                return True
        
        return False
    
    def delete_order(self, order_id):
        """
        Find an order by ID, remove it, and re-sort the list.
        
        Args:
            order_id (int): The ID of the order to delete
            
        Returns:
            bool: True if order was found and deleted, False otherwise
        """
        # Search in bids
        for i, order in enumerate(self.bids):
            if order["order_id"] == order_id:
                self.bids.pop(i)
                # Re-sort bids descending by price
                self.bids.sort(key=lambda x: x["price"], reverse=True)
                return True
        
        # Search in asks
        for i, order in enumerate(self.asks):
            if order["order_id"] == order_id:
                self.asks.pop(i)
                # Re-sort asks ascending by price
                self.asks.sort(key=lambda x: x["price"])
                return True
        
        return False
    
    def lookup_order(self, order_id):
        """
        Lookup an order by its ID.
        
        Args:
            order_id (int): The ID of the order to find
            
        Returns:
            dict or None: The order dictionary if found, None otherwise
        """
        # Search in bids
        for order in self.bids:
            if order["order_id"] == order_id:
                return order
        
        # Search in asks
        for order in self.asks:
            if order["order_id"] == order_id:
                return order
        
        return None
    
    def get_orders_at_price(self, price, side=None):
        """
        Retrieve all orders at a given price level.
        
        Args:
            price (float): The price level to query
            side (str, optional): "bid", "ask", or None. If None, returns orders from both sides.
            
        Returns:
            list: List of orders at the specified price level
        """
        result = []
        
        if side is None or side == "bid":
            for order in self.bids:
                if order["price"] == price:
                    result.append(order)
        
        if side is None or side == "ask":
            for order in self.asks:
                if order["price"] == price:
                    result.append(order)
        
        return result
    
    def get_best_bid(self):
        """
        Return the best (highest) bid.
        
        Returns:
            dict or None: The best bid order if bids exist, None otherwise
        """
        if self.bids:
            return self.bids[0]  # First element after descending sort
        return None
    
    def get_best_ask(self):
        """
        Return the best (lowest) ask.
        
        Returns:
            dict or None: The best ask order if asks exist, None otherwise
        """
        if self.asks:
            return self.asks[0]  # First element after ascending sort
        return None
    
    def get_best_bid_ask(self):
        """
        Return both best bid and best ask.
        
        Returns:
            tuple: (best_bid, best_ask) where each is a dict or None
        """
        return (self.get_best_bid(), self.get_best_ask())


# Example usage and testing
if __name__ == "__main__":
    # Create order book
    ob = NaiveOrderBook()
    
    # Add some orders
    ob.add_order({"order_id": 1, "price": 100.0, "quantity": 10, "side": "bid"})
    ob.add_order({"order_id": 2, "price": 101.0, "quantity": 5, "side": "bid"})
    ob.add_order({"order_id": 3, "price": 99.0, "quantity": 8, "side": "bid"})
    ob.add_order({"order_id": 4, "price": 102.0, "quantity": 15, "side": "ask"})
    ob.add_order({"order_id": 5, "price": 103.0, "quantity": 12, "side": "ask"})
    ob.add_order({"order_id": 6, "price": 101.0, "quantity": 7, "side": "ask"})
    
    print("Best bid:", ob.get_best_bid())
    print("Best ask:", ob.get_best_ask())
    print()
    
    # Lookup order
    order = ob.lookup_order(2)
    print(f"Lookup order 2: {order}")
    print()
    
    # Get orders at price
    orders_at_101 = ob.get_orders_at_price(101.0)
    print(f"Orders at price 101.0: {orders_at_101}")
    print()
    
    # Amend order
    ob.amend_order(1, 20)
    print(f"After amending order 1 quantity to 20: {ob.lookup_order(1)}")
    print()
    
    # Delete order
    ob.delete_order(3)
    print(f"After deleting order 3, lookup returns: {ob.lookup_order(3)}")
    print()
    
    print("Final best bid:", ob.get_best_bid())
    print("Final best ask:", ob.get_best_ask())

