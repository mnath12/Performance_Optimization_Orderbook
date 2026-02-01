"""
Optimized Order Book Implementation

This implementation uses efficient data structures to improve performance:
- Dictionary for O(1) order ID lookup
- Dictionary for O(1) price level access
- Heaps for O(log n) insertion and O(1) best bid/ask retrieval
"""

import heapq


class OptimizedOrderBook:
    """
    An optimized order book implementation using efficient data structures.
    
    Data Structures:
    - orders_by_id: dict mapping order_id -> order dict (O(1) lookup)
    - bids_by_price: dict mapping price -> list of orders at that price (O(1) access)
    - asks_by_price: dict mapping price -> list of orders at that price (O(1) access)
    - bid_heap: min-heap of NEGATED bid prices (allows O(log n) insertion, best bid is heap[0] when negated)
    - ask_heap: min-heap of ask prices (allows O(log n) insertion, best ask is heap[0])
    
    Time Complexities:
    - add_order: O(log n) - heap insertion
    - amend_order: O(1) - dictionary lookup and update
    - delete_order: O(log n) amortized - lazy deletion from heap + list.remove O(k) where k is orders at price
    - lookup_order: O(1) - dictionary lookup
    - get_orders_at_price: O(1) - dictionary lookup
    - get_best_bid/get_best_ask: O(log n) amortized - heap cleanup of deleted prices
    """
    
    def __init__(self):
        """Initialize empty data structures."""
        # O(1) lookup by order ID
        self.orders_by_id = {}
        
        # O(1) access to orders at a price level
        self.bids_by_price = {}  # price -> list of orders
        self.asks_by_price = {}  # price -> list of orders
        
        # Heaps for efficient best bid/ask retrieval
        # bid_heap stores negated prices (min-heap of negated = max-heap of actual prices)
        # ask_heap stores prices directly (min-heap)
        self.bid_heap = []
        self.ask_heap = []
    
    def add_order(self, order_dict):
        """
        Add an order to the appropriate structures.
        
        Args:
            order_dict: Dictionary with keys:
                - order_id (int): Unique order identifier
                - price (float): Order price
                - quantity (int): Order quantity
                - side (str): "bid" or "ask"
        """
        order_id = order_dict["order_id"]
        price = order_dict["price"]
        side = order_dict["side"]
        
        if order_id in self.orders_by_id:
            raise ValueError(f"Order ID {order_id} already exists")
        
        # Store order in orders_by_id for O(1) lookup
        self.orders_by_id[order_id] = order_dict
        
        if side == "bid":
            # Add to bids_by_price
            if price not in self.bids_by_price:
                self.bids_by_price[price] = []
                # Insert negated price into min-heap (for max-heap behavior)
                negated_price = -price
                heapq.heappush(self.bid_heap, negated_price)
            self.bids_by_price[price].append(order_dict)
            
        elif side == "ask":
            # Add to asks_by_price
            if price not in self.asks_by_price:
                self.asks_by_price[price] = []
                # Insert price into min-heap
                heapq.heappush(self.ask_heap, price)
            self.asks_by_price[price].append(order_dict)
        else:
            raise ValueError(f"Invalid side: {side}. Must be 'bid' or 'ask'")
    
    def amend_order(self, order_id, new_quantity):
        """
        Find an order by ID, update its quantity.
        No re-sorting needed since price doesn't change.
        
        Args:
            order_id (int): The ID of the order to amend
            new_quantity (int): The new quantity for the order
            
        Returns:
            bool: True if order was found and amended, False otherwise
        """
        if order_id not in self.orders_by_id:
            return False
        
        # O(1) lookup and update
        order = self.orders_by_id[order_id]
        order["quantity"] = new_quantity
        
        return True
    
    def delete_order(self, order_id):
        """
        Find an order by ID, remove it from all structures.
        
        Args:
            order_id (int): The ID of the order to delete
            
        Returns:
            bool: True if order was found and deleted, False otherwise
        """
        if order_id not in self.orders_by_id:
            return False
        
        order = self.orders_by_id[order_id]
        price = order["price"]
        side = order["side"]
        
        # Remove from orders_by_id
        del self.orders_by_id[order_id]
        
        if side == "bid":
            # Remove from bids_by_price
            if price in self.bids_by_price:
                self.bids_by_price[price].remove(order)
                # If no more orders at this price, remove price level
                # Note: We use lazy deletion - the price stays in the heap but gets cleaned up
                # when we access get_best_bid() and it's no longer in bids_by_price
                if not self.bids_by_price[price]:
                    del self.bids_by_price[price]
        
        elif side == "ask":
            # Remove from asks_by_price
            if price in self.asks_by_price:
                self.asks_by_price[price].remove(order)
                # If no more orders at this price, remove price level
                # Note: We use lazy deletion - the price stays in the heap but gets cleaned up
                # when we access get_best_ask() and it's no longer in asks_by_price
                if not self.asks_by_price[price]:
                    del self.asks_by_price[price]
        
        return True
    
    def lookup_order(self, order_id):
        """
        Lookup an order by its ID. O(1) operation.
        
        Args:
            order_id (int): The ID of the order to find
            
        Returns:
            dict or None: The order dictionary if found, None otherwise
        """
        return self.orders_by_id.get(order_id)
    
    def get_orders_at_price(self, price, side=None):
        """
        Retrieve all orders at a given price level. O(1) operation.
        
        Args:
            price (float): The price level to query
            side (str, optional): "bid", "ask", or None. If None, returns orders from both sides.
            
        Returns:
            list: List of orders at the specified price level
        """
        result = []
        
        if side is None or side == "bid":
            if price in self.bids_by_price:
                result.extend(self.bids_by_price[price])
        
        if side is None or side == "ask":
            if price in self.asks_by_price:
                result.extend(self.asks_by_price[price])
        
        return result
    
    def get_best_bid(self):
        """
        Return the best (highest) bid. O(log n) amortized due to lazy deletion cleanup.
        
        Returns:
            dict or None: The best bid order if bids exist, None otherwise
        """
        # Clean up deleted prices from heap (lazy deletion)
        while self.bid_heap:
            negated_price = self.bid_heap[0]
            best_price = -negated_price
            # Check if this price still exists in bids_by_price
            if best_price in self.bids_by_price and self.bids_by_price[best_price]:
                # Found valid best bid
                return self.bids_by_price[best_price][0]  # Return first order at best price
            else:
                # This price was deleted, remove it from heap
                heapq.heappop(self.bid_heap)
        
        return None
    
    def get_best_ask(self):
        """
        Return the best (lowest) ask. O(log n) amortized due to lazy deletion cleanup.
        
        Returns:
            dict or None: The best ask order if asks exist, None otherwise
        """
        # Clean up deleted prices from heap (lazy deletion)
        while self.ask_heap:
            best_price = self.ask_heap[0]
            # Check if this price still exists in asks_by_price
            if best_price in self.asks_by_price and self.asks_by_price[best_price]:
                # Found valid best ask
                return self.asks_by_price[best_price][0]  # Return first order at best price
            else:
                # This price was deleted, remove it from heap
                heapq.heappop(self.ask_heap)
        
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
    ob = OptimizedOrderBook()
    
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

