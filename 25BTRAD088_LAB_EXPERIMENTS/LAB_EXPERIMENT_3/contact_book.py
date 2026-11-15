# Contact Book Program
# Data structure: a dictionary maps each contact name to a list [phone,
email].

contacts = {}

def add_contact(name, phone, email):
if name in contacts:

print(f"Contact '{name}' already exists.")
else:
contacts[name] = [phone, email]
print(f"Contact '{name}' added successfully.")

def search_contact(name):
if name in contacts:
print(f"Name: {name} | Phone: {contacts[name][0]} | Email:
{contacts[name][1]}")
else:
print(f"Contact '{name}' not found.")

def update_contact(name, phone, email):
if name in contacts:
contacts[name] = [phone, email]
print(f"Contact '{name}' updated successfully.")
else:
print(f"Contact '{name}' not found.")

def delete_contact(name):
if name in contacts:
del contacts[name]
print(f"Contact '{name}' deleted successfully.")
else:
print(f"Contact '{name}' not found.")

def display_contacts():
if not contacts:
print("The contact book is empty.")
else:
print("\n--- Contact List ---")
for name, details in contacts.items():
print(f"Name: {name} | Phone: {details[0]} | Email:
{details[1]}")

# Example Usage (Testing)
add_contact("Ramu", "7765435210", "Ram@email.com")
add_contact("om raut", "8214367890", "om@email.com")
add_contact("nickel;", "6050008209", "nick@email.com") # duplicate
check
search_contact("Ramu")
search_contact("Bob") # not found check
update_contact("Ramu", "8689398703", "Ram_new@email.com")
display_contacts()
delete_contact("Bob")
delete_contact("Bob") # already deleted check
display_contacts()
