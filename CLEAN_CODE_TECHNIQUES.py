"""
CLEAN CODE TECHNIQUES - Pure Code Examples
Professional coding practices for readable, maintainable code
"""

# ============================================================================
# 1. MEANINGFUL NAMES
# ============================================================================

# ❌ BAD: Unclear, cryptic names
def calc(d):
    t = 0
    for x in d:
        t += x['p'] * x['q']
    return t

# ✅ GOOD: Clear, descriptive names
def calculate_total_revenue(orders):
    total_revenue = 0
    for order in orders:
        total_revenue += order['price'] * order['quantity']
    return total_revenue


# ❌ BAD: Single letter variables
def process(a, b, c):
    return a * b + c

# ✅ GOOD: Descriptive variable names
def calculate_order_total(unit_price, quantity, tax_amount):
    return unit_price * quantity + tax_amount


# ❌ BAD: Ambiguous names
def get_data():
    pass

# ✅ GOOD: Specific, clear names
def get_customer_orders_from_database():
    pass


# ============================================================================
# 2. FUNCTIONS SHOULD BE SMALL
# ============================================================================

# ❌ BAD: Large, complex function
def process_order(order):
    # Validate order
    if not order:
        return None
    if 'customer_id' not in order:
        return None
    if 'items' not in order:
        return None
    
    # Calculate totals
    subtotal = 0
    for item in order['items']:
        subtotal += item['price'] * item['quantity']
    
    # Apply discount
    discount = 0
    if order.get('discount_code'):
        if order['discount_code'] == 'SAVE10':
            discount = subtotal * 0.1
        elif order['discount_code'] == 'SAVE20':
            discount = subtotal * 0.2
    
    # Calculate tax
    tax = (subtotal - discount) * 0.08
    
    # Calculate total
    total = subtotal - discount + tax
    
    # Save to database
    # ... 50 more lines
    
    return total

# ✅ GOOD: Small, focused functions
def process_order(order):
    """Process order and return total amount"""
    if not is_valid_order(order):
        return None
    
    subtotal = calculate_subtotal(order['items'])
    discount = calculate_discount(subtotal, order.get('discount_code'))
    tax = calculate_tax(subtotal - discount)
    total = subtotal - discount + tax
    
    save_order_to_database(order, total)
    
    return total

def is_valid_order(order):
    """Validate order has required fields"""
    return (order and 
            'customer_id' in order and 
            'items' in order)

def calculate_subtotal(items):
    """Calculate subtotal from items"""
    return sum(item['price'] * item['quantity'] for item in items)

def calculate_discount(subtotal, discount_code):
    """Calculate discount amount based on code"""
    discount_rates = {
        'SAVE10': 0.1,
        'SAVE20': 0.2
    }
    rate = discount_rates.get(discount_code, 0)
    return subtotal * rate

def calculate_tax(amount):
    """Calculate tax amount"""
    TAX_RATE = 0.08
    return amount * TAX_RATE

def save_order_to_database(order, total):
    """Save order to database"""
    # Database logic here
    pass


# ============================================================================
# 3. DO ONE THING
# ============================================================================

# ❌ BAD: Function does multiple things
def process_customer_data(customer):
    # Validate
    if not customer['email']:
        return False
    
    # Format
    customer['name'] = customer['name'].upper()
    
    # Calculate
    customer['total_spent'] = sum(order['amount'] for order in customer['orders'])
    
    # Save
    database.save(customer)
    
    # Send email
    send_welcome_email(customer['email'])
    
    return True

# ✅ GOOD: Each function does one thing
def validate_customer(customer):
    """Only validates customer data"""
    return bool(customer.get('email'))

def format_customer_name(name):
    """Only formats customer name"""
    return name.upper()

def calculate_customer_total_spent(orders):
    """Only calculates total spent"""
    return sum(order['amount'] for order in orders)

def save_customer(customer):
    """Only saves customer to database"""
    database.save(customer)

def send_customer_welcome_email(email):
    """Only sends welcome email"""
    send_welcome_email(email)


# ============================================================================
# 4. DRY - DON'T REPEAT YOURSELF
# ============================================================================

# ❌ BAD: Repeated code
def calculate_outlet_revenue_galle():
    orders = get_orders_by_outlet('Galle')
    total = 0
    for order in orders:
        total += order['amount']
    return total

def calculate_outlet_revenue_colombo():
    orders = get_orders_by_outlet('Colombo')
    total = 0
    for order in orders:
        total += order['amount']
    return total

def calculate_outlet_revenue_kandy():
    orders = get_orders_by_outlet('Kandy')
    total = 0
    for order in orders:
        total += order['amount']
    return total

# ✅ GOOD: Reusable function
def calculate_outlet_revenue(outlet_name):
    """Calculate revenue for any outlet"""
    orders = get_orders_by_outlet(outlet_name)
    return sum(order['amount'] for order in orders)

# Usage
galle_revenue = calculate_outlet_revenue('Galle')
colombo_revenue = calculate_outlet_revenue('Colombo')
kandy_revenue = calculate_outlet_revenue('Kandy')


# ============================================================================
# 5. PROPER ERROR HANDLING
# ============================================================================

# ❌ BAD: Silent failures
def load_customer_data(customer_id):
    try:
        return database.get(customer_id)
    except:
        return None  # What went wrong?

# ✅ GOOD: Explicit error handling
def load_customer_data(customer_id):
    """Load customer data with proper error handling"""
    if not customer_id:
        raise ValueError("Customer ID is required")
    
    try:
        customer = database.get(customer_id)
        if not customer:
            raise ValueError(f"Customer {customer_id} not found")
        return customer
    except DatabaseConnectionError as e:
        raise RuntimeError(f"Database connection failed: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Failed to load customer: {str(e)}")


# ❌ BAD: Catching all exceptions
def process_payment(amount):
    try:
        # Process payment
        pass
    except:  # Too broad!
        return False

# ✅ GOOD: Specific exception handling
def process_payment(amount):
    """Process payment with specific error handling"""
    try:
        validate_payment_amount(amount)
        charge_customer(amount)
        return True
    except InvalidAmountError as e:
        log_error(f"Invalid amount: {e}")
        raise
    except PaymentGatewayError as e:
        log_error(f"Payment gateway error: {e}")
        raise
    except Exception as e:
        log_error(f"Unexpected error: {e}")
        raise


# ============================================================================
# 6. COMMENTS AND DOCUMENTATION
# ============================================================================

# ❌ BAD: Obvious comments
def calculate_total(items):
    # Loop through items
    total = 0
    for item in items:
        # Add price to total
        total += item['price']
    # Return total
    return total

# ✅ GOOD: Meaningful docstrings
def calculate_order_total_with_discounts(items, customer_tier):
    """
    Calculate order total with tier-based discounts.
    
    Args:
        items: List of order items with 'price' and 'quantity'
        customer_tier: Customer loyalty tier ('bronze', 'silver', 'gold')
    
    Returns:
        float: Total amount after applying tier discount
    
    Raises:
        ValueError: If customer_tier is invalid
    
    Example:
        >>> items = [{'price': 100, 'quantity': 2}]
        >>> calculate_order_total_with_discounts(items, 'gold')
        180.0  # 200 with 10% gold discount
    """
    subtotal = sum(item['price'] * item['quantity'] for item in items)
    discount_rate = get_tier_discount_rate(customer_tier)
    return subtotal * (1 - discount_rate)


# ❌ BAD: Commented-out code
def process_order(order):
    # old_total = calculate_old_way(order)
    # if old_total > 1000:
    #     apply_discount()
    
    total = calculate_new_way(order)
    return total

# ✅ GOOD: Clean code without commented code
def process_order(order):
    """Process order using current calculation method"""
    return calculate_order_total(order)


# ============================================================================
# 7. CONSISTENT FORMATTING
# ============================================================================

# ❌ BAD: Inconsistent formatting
def calculate_revenue(orders):
    total=0
    for order in orders:
        if order['status']=='completed':
            total+=order['amount']
    return total

# ✅ GOOD: Consistent formatting (PEP 8)
def calculate_revenue(orders):
    """Calculate total revenue from completed orders"""
    total = 0
    for order in orders:
        if order['status'] == 'completed':
            total += order['amount']
    return total


# ============================================================================
# 8. AVOID MAGIC NUMBERS
# ============================================================================

# ❌ BAD: Magic numbers
def calculate_discount(amount):
    if amount > 1000:
        return amount * 0.1
    elif amount > 500:
        return amount * 0.05
    return 0

# ✅ GOOD: Named constants
LARGE_ORDER_THRESHOLD = 1000
MEDIUM_ORDER_THRESHOLD = 500
LARGE_ORDER_DISCOUNT_RATE = 0.1
MEDIUM_ORDER_DISCOUNT_RATE = 0.05

def calculate_discount(amount):
    """Calculate discount based on order amount"""
    if amount > LARGE_ORDER_THRESHOLD:
        return amount * LARGE_ORDER_DISCOUNT_RATE
    elif amount > MEDIUM_ORDER_THRESHOLD:
        return amount * MEDIUM_ORDER_DISCOUNT_RATE
    return 0


# ============================================================================
# 9. USE DESCRIPTIVE CONDITIONALS
# ============================================================================

# ❌ BAD: Complex conditional
def process_order(order):
    if order['amount'] > 1000 and order['customer']['tier'] == 'gold' and len(order['items']) > 5:
        apply_special_discount(order)

# ✅ GOOD: Named boolean variables
def process_order(order):
    """Process order with special discount logic"""
    is_large_order = order['amount'] > 1000
    is_gold_customer = order['customer']['tier'] == 'gold'
    has_many_items = len(order['items']) > 5
    
    if is_large_order and is_gold_customer and has_many_items:
        apply_special_discount(order)


# ❌ BAD: Nested conditionals
def get_discount_rate(customer):
    if customer:
        if customer['tier']:
            if customer['tier'] == 'gold':
                return 0.2
            elif customer['tier'] == 'silver':
                return 0.1
    return 0

# ✅ GOOD: Early returns
def get_discount_rate(customer):
    """Get discount rate based on customer tier"""
    if not customer or not customer.get('tier'):
        return 0
    
    tier_discounts = {
        'gold': 0.2,
        'silver': 0.1,
        'bronze': 0.05
    }
    
    return tier_discounts.get(customer['tier'], 0)


# ============================================================================
# 10. FUNCTION PARAMETERS
# ============================================================================

# ❌ BAD: Too many parameters
def create_order(customer_id, items, shipping_address, billing_address, 
                payment_method, discount_code, gift_message, gift_wrap,
                delivery_date, special_instructions):
    pass

# ✅ GOOD: Use objects/dictionaries
def create_order(order_data):
    """
    Create order from order data dictionary.
    
    Args:
        order_data: Dictionary containing:
            - customer_id: Customer identifier
            - items: List of order items
            - shipping_address: Shipping address dict
            - billing_address: Billing address dict
            - payment_method: Payment method string
            - discount_code: Optional discount code
            - gift_options: Optional gift options dict
            - delivery_options: Optional delivery options dict
    """
    customer_id = order_data['customer_id']
    items = order_data['items']
    # ... process order
    pass


# ❌ BAD: Boolean parameters
def get_customers(include_inactive, include_deleted, include_test):
    pass

# ✅ GOOD: Separate functions or options object
def get_active_customers():
    """Get only active customers"""
    return get_customers_by_status('active')

def get_all_customers():
    """Get all customers including inactive"""
    return get_customers_by_status('all')

def get_customers_by_status(status):
    """Get customers filtered by status"""
    pass


# ============================================================================
# 11. AVOID SIDE EFFECTS
# ============================================================================

# ❌ BAD: Function with side effects
total_revenue = 0

def calculate_order_total(order):
    global total_revenue
    order_total = sum(item['price'] for item in order['items'])
    total_revenue += order_total  # Side effect!
    return order_total

# ✅ GOOD: Pure function without side effects
def calculate_order_total(order):
    """Calculate order total without side effects"""
    return sum(item['price'] for item in order['items'])

def calculate_total_revenue(orders):
    """Calculate total revenue from all orders"""
    return sum(calculate_order_total(order) for order in orders)


# ============================================================================
# 12. USE MEANINGFUL DATA STRUCTURES
# ============================================================================

# ❌ BAD: Unclear data structure
def process_customer(data):
    # What is data[0]? data[1]?
    name = data[0]
    email = data[1]
    age = data[2]
    tier = data[3]

# ✅ GOOD: Clear dictionary/object
def process_customer(customer):
    """Process customer with clear data structure"""
    name = customer['name']
    email = customer['email']
    age = customer['age']
    tier = customer['tier']


# ❌ BAD: Multiple return values as tuple
def get_customer_stats(customer_id):
    # What does each value mean?
    return (150, 25000, 4.5, 'gold')

# ✅ GOOD: Return dictionary with named values
def get_customer_stats(customer_id):
    """Get customer statistics as dictionary"""
    return {
        'total_orders': 150,
        'total_spent': 25000,
        'average_rating': 4.5,
        'loyalty_tier': 'gold'
    }


# ============================================================================
# 13. AVOID DEEP NESTING
# ============================================================================

# ❌ BAD: Deep nesting
def process_order(order):
    if order:
        if order.get('customer'):
            if order['customer'].get('email'):
                if validate_email(order['customer']['email']):
                    if order.get('items'):
                        if len(order['items']) > 0:
                            # Process order
                            pass

# ✅ GOOD: Guard clauses and early returns
def process_order(order):
    """Process order with guard clauses"""
    if not order:
        raise ValueError("Order is required")
    
    if not order.get('customer'):
        raise ValueError("Customer is required")
    
    email = order['customer'].get('email')
    if not email or not validate_email(email):
        raise ValueError("Valid email is required")
    
    items = order.get('items', [])
    if not items:
        raise ValueError("Order must have items")
    
    # Process order - no nesting!
    return process_order_items(items)


# ============================================================================
# 14. USE LIST COMPREHENSIONS WISELY
# ============================================================================

# ❌ BAD: Complex list comprehension
result = [item['price'] * item['quantity'] * (1 - item.get('discount', 0)) 
          for item in orders if item['status'] == 'completed' 
          and item['customer']['tier'] in ['gold', 'silver'] 
          and item['amount'] > 100]

# ✅ GOOD: Break down complex comprehensions
def is_eligible_order(item):
    """Check if order is eligible for calculation"""
    return (item['status'] == 'completed' and
            item['customer']['tier'] in ['gold', 'silver'] and
            item['amount'] > 100)

def calculate_item_total(item):
    """Calculate total for single item"""
    discount = item.get('discount', 0)
    return item['price'] * item['quantity'] * (1 - discount)

# Clear and readable
eligible_orders = [item for item in orders if is_eligible_order(item)]
result = [calculate_item_total(item) for item in eligible_orders]


# ============================================================================
# 15. PROPER VARIABLE SCOPE
# ============================================================================

# ❌ BAD: Global variables
current_user = None
current_order = None

def process_order():
    global current_user, current_order
    # Modifying global state
    pass

# ✅ GOOD: Pass parameters explicitly
def process_order(user, order):
    """Process order with explicit parameters"""
    validated_order = validate_order(order)
    authorized_user = authorize_user(user)
    return complete_order(validated_order, authorized_user)


# ============================================================================
# 16. CONSISTENT NAMING CONVENTIONS
# ============================================================================

# ❌ BAD: Inconsistent naming
def GetCustomer(id):  # PascalCase for function
    customer_Name = "John"  # Mixed case
    CustomerAge = 25  # PascalCase for variable
    return customer_Name

# ✅ GOOD: Consistent naming (PEP 8)
def get_customer(customer_id):
    """Get customer by ID - snake_case for functions"""
    customer_name = "John"  # snake_case for variables
    customer_age = 25
    return customer_name

class CustomerService:  # PascalCase for classes
    """Customer service class"""
    
    MAX_RETRIES = 3  # UPPER_CASE for constants
    
    def get_customer_by_id(self, customer_id):
        """snake_case for methods"""
        pass


# ============================================================================
# 17. AVOID PREMATURE OPTIMIZATION
# ============================================================================

# ❌ BAD: Premature optimization
def calculate_total(items):
    # Trying to optimize before measuring
    total = 0
    items_len = len(items)
    for i in range(items_len):
        total += items[i]['price']
    return total

# ✅ GOOD: Clear, readable code first
def calculate_total(items):
    """Calculate total - optimize later if needed"""
    return sum(item['price'] for item in items)


# ============================================================================
# 18. USE TYPE HINTS (Python 3.5+)
# ============================================================================

# ❌ BAD: No type hints
def calculate_discount(amount, rate):
    return amount * rate

# ✅ GOOD: Clear type hints
def calculate_discount(amount: float, rate: float) -> float:
    """
    Calculate discount amount.
    
    Args:
        amount: Order amount in currency
        rate: Discount rate (0.0 to 1.0)
    
    Returns:
        Discount amount
    """
    return amount * rate

from typing import List, Dict, Optional

def get_customer_orders(customer_id: str) -> List[Dict[str, any]]:
    """Get all orders for a customer"""
    pass

def find_customer(customer_id: str) -> Optional[Dict[str, any]]:
    """Find customer by ID, returns None if not found"""
    pass


# ============================================================================
# 19. PROPER STRING FORMATTING
# ============================================================================

# ❌ BAD: String concatenation
def format_customer_message(name, amount, date):
    return "Hello " + name + ", your order of $" + str(amount) + " on " + date + " is ready"

# ✅ GOOD: f-strings (Python 3.6+)
def format_customer_message(name: str, amount: float, date: str) -> str:
    """Format customer message using f-strings"""
    return f"Hello {name}, your order of ${amount:.2f} on {date} is ready"


# ============================================================================
# 20. CLEAN IMPORTS
# ============================================================================

# ❌ BAD: Messy imports
from module import *
import sys, os, json
from package import function1, function2, function3, function4, function5

# ✅ GOOD: Organized imports (PEP 8)
# Standard library imports
import json
import os
import sys

# Third-party imports
import pandas as pd
import numpy as np

# Local application imports
from backend.services import analytics_service
from backend.repositories import data_repository


# ============================================================================
# SUMMARY: CLEAN CODE CHECKLIST
# ============================================================================

"""
✅ Use meaningful, descriptive names
✅ Keep functions small (< 20 lines ideally)
✅ Each function does ONE thing
✅ Don't repeat yourself (DRY)
✅ Handle errors explicitly
✅ Write clear documentation
✅ Format consistently (PEP 8)
✅ Avoid magic numbers
✅ Use descriptive conditionals
✅ Limit function parameters
✅ Avoid side effects
✅ Use meaningful data structures
✅ Avoid deep nesting
✅ Use comprehensions wisely
✅ Proper variable scope
✅ Consistent naming conventions
✅ Avoid premature optimization
✅ Use type hints
✅ Proper string formatting
✅ Organize imports cleanly
"""
