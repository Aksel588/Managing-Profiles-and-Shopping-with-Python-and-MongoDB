import random
import string
import pymongo

myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = myclient['mydatabase']
mycol = mydb["customers"]


def user_info():
    """Collect user information and return it."""
    name = input("What is your name? ")
    age = int(input("What is your age? "))
    nick_name = input("What is your nickname? ")
    mydict = {"name": name, "age": age,"nick_name": nick_name}

    x = mycol.insert_one(mydict)
    code_pers = generate_random_string(10)  # Generate a personal code
    return name, age, nick_name, code_pers

def generate_random_string(length):
    """Generate a random string of letters and digits with the specified length."""
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

def start():
    """Start the program and handle user input."""
    user_input = input("Welcome! If you want to start, enter 'START': ")

    if user_input.lower() == "start":
        print("Ok")
        # Call user_info once and store the result
        user_details = user_info()
        command(user_details)
    else:
        print("No")

def command(user_details):
    """Display the command menu and handle user choices."""
    while True:
        print("\n1. Profile")
        print("2. Edit")
        print("3. Your personal code")
        print("4. Shop")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            profile(user_details)
        elif choice == "2":
            user_details = edit(user_details)
        elif choice == "3":
            code_pers(user_details)
        elif choice == "4":
            shop(user_details)
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

def profile(user_details):
    """Display user profile information."""
    name, age, nick_name, _ = user_details
    print("\nProfile Information:")
    print(f"Name: {name}")
    print(f"Age: {age}")
    print(f"Nickname: {nick_name}")

def edit(user_details):
    """Functionality to edit user information."""
    _, _, _, code_pers = user_details

    # Get the new information from the user
    new_name = input("What is your new name? ")
    while True:
        try:
            new_age = int(input("What is your new age? "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid number for age.")
    new_nick_name = input("What is your new nickname? ")

    # Update the user details with new values
    return new_name, new_age, new_nick_name, user_details[3]  # Keep the same personal code

def code_pers(user_details):
    """Display the personal code."""
    _, _, _, code_pers = user_details
    print(f"Your personal code is: {code_pers}")

def shop(user_details):
    """Functionality for shop."""
    name, _, _, code_pers = user_details
    print(f"Welcome to the shop, dear {name}!")

    products = {
        "1": {"name": "Widget", "price": 10.00},
        "2": {"name": "Gadget", "price": 15.00},
        "3": {"name": "Doodad", "price": 20.00},
        "4": {"name": "Thingamajig", "price": 25.00},
        "5": {"name": "Contraption", "price": 30.00},
        "6": {"name": "Doohickey", "price": 35.00},
        "7": {"name": "Gizmo", "price": 40.00},
        "8": {"name": "Device", "price": 45.00},
        "9": {"name": "Machine", "price": 50.00},
        "10": {"name": "Apparatus", "price": 55.00},
    }

    basket = []  # Initialize an empty basket

    while True:
        if not basket:  # If the basket is empty, show the product list and menu
            print("\nAvailable products:")
            for key, product in products.items():
                print(f"{key}. {product['name']} - ${product['price']:.2f}")

            print("\n1. View product details")
            print("2. Add product to basket")
            print("3. View basket and checkout")
            print("4. Back to main menu")

        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            view_product_details(products)
        elif choice == "2":
            add_to_basket(products, basket)
        elif choice == "3":
            if checkout(basket, code_pers):
                break  # Exit the loop if the purchase is successful
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

def view_product_details(products):
    """View details of a specific product."""
    product_id = input("Enter the product number to view details: ")
    product = products.get(product_id)
    if product:
        print(f"\nProduct: {product['name']}")
        print(f"Price: ${product['price']:.2f}")
    else:
        print("Product not found.")

def add_to_basket(products, basket):
    """Add a specific product to the basket."""
    product_id = input("Enter the product number to add to the basket: ")
    product = products.get(product_id)
    if product:
        basket.append(product)
        print(f"\n{product['name']} has been added to your basket.")
    else:
        print("Product not found.")

def checkout(basket, code_pers):
    """View basket contents and proceed to checkout."""
    if not basket:
        print("Your basket is empty.")
        return

    print("\nYour basket:")
    total = 0
    for product in basket:
        print(f"{product['name']} - ${product['price']:.2f}")
        total += product['price']

    print(f"\nTotal: ${total:.2f}")
    confirm = input("Do you want to buy product(s)? (yes/no): ")
    if confirm.lower() == "yes":
        if buy_pro(code_pers):
            basket.clear()  # Empty the basket after successful checkout
            return  # Exit the checkout function after successful purchase
    else:
        print("Checkout canceled.")

def buy_pro(code_pers):
    """Verify personal code before completing purchase."""
    code_ver = input("Please enter your personal code to complete the purchase: ")
    if code_ver == code_pers:
        print("Thanks for buying!")
        return True  # Indicate successful purchase
    else:
        print("Invalid code. Please check your code and try again.")
        return False  # Indicate failed purchase


# Call the start function to begin the script
start()
