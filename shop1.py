import random
import json


# Define the Product class
class Product:
    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category

    def to_dict(self):
        return {
            "name": self.name,
            "price": self.price,
            "category": self.category
        }


# Define the Customer class
class Customer:
    def __init__(self, name, products, loyalty_card):
        self.name = name
        self.products = products
        self.loyalty_card = loyalty_card

    def to_dict(self):
        return {
            "name": self.name,
            "products": [product.to_dict() for product in self.products],
            "loyalty_card": self.loyalty_card
        }


# Define the Cashier class
class Cashier:
    def __init__(self, name):
        self.name = name

    def process_customer(self, customer, discounts):
        total_price = sum(product.price for product in customer.products)
        discounted_price = 0
        detailed_products = []

        for product in customer.products:
            discount = self.get_discount(product, discounts)
            discounted_price += product.price * (1 - discount)
            detailed_products.append({
                "name": product.name,
                "original_price": product.price,
                "discounted_price": product.price * (1 - discount)
            })

        if customer.loyalty_card:
            discounted_price *= 0.9  # Apply an additional 10% discount for loyalty cardholders

        return {
            "customer_name": customer.name,
            "products": detailed_products,
            "total_price": total_price,
            "total_amount_spent": discounted_price,
            "cashier_name": self.name
        }

    @staticmethod
    def get_discount(product, discounts):
        applicable_discounts = [d.discount for d in discounts if d.type == 'product' and d.value == product.name]
        applicable_discounts += [d.discount for d in discounts if d.type == 'category' and d.value == product.category]
        return max(applicable_discounts, default=0)


# Define the Discount class
class Discount:
    def __init__(self, discount_type, value, discount):
        self.type = discount_type
        self.value = value
        self.discount = discount


# Generate products
def generate_products(n=100):
    categories = ['Electronics', 'Clothing', 'Groceries', 'Books', 'Toys']
    article_list = []
    for i in range(n):
        name = f"Product_{i}"
        price = round(random.uniform(5, 100), 2)
        category = random.choice(categories)
        article_list.append(Product(name, price, category))
    return article_list


global_products = generate_products()


# Generate customers
def generate_customers(articles, n=150):
    client_list = []
    for i in range(n):
        name = f"Customer_{i}"
        num_products = random.randint(1, 10)
        customer_products = random.sample(articles, num_products)
        loyalty_card = random.choice([True, False])
        client_list.append(Customer(name, customer_products, loyalty_card))
    return client_list


global_customers = generate_customers(global_products)


# Generate discounts
def generate_discounts():
    discount_list = []
    categories = ['Electronics', 'Clothing', 'Groceries', 'Books', 'Toys']
    for _ in range(5):
        discount_type = random.choice(['product', 'category'])
        value = random.choice(categories) if discount_type == 'category' else f"Product_{random.randint(0, 99)}"
        discount_amount = round(random.uniform(0.05, 0.3), 2)
        discount_list.append(Discount(discount_type, value, discount_amount))
    return discount_list


global_discounts = generate_discounts()

# Generate Cashiers
global_cashiers = [Cashier(f"Cashier_{i}") for i in range(1, 4)]  # 3 cashiers for example


# Process customers without multiprocessing
def process_customers(clients, cashiers, discounts):
    reports = []
    for customer in clients:
        cashier = random.choice(cashiers)
        report = cashier.process_customer(customer, discounts)
        reports.append(report)
    return reports


if __name__ == '__main__':
    try:
        daily_reports1 = process_customers(global_customers, global_cashiers, global_discounts)
        # Check the contents of daily_reports
        print("Daily Reports:")
        for report in daily_reports1:
            print(report)

        # Save the report to a JSON file
        with open('daily_reports1.json', 'w') as f:
            json.dump(daily_reports1, f, indent=4)
        print("Daily report generated and saved to daily_reports1.json")
    except Exception as e:
        print(f"An error occurred in the main process: {str(e)}")
