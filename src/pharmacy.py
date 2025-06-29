# Storing available medicine using dictionaries and using sets to prevent duplicate entries.


import json
import os

class Pharmacy:
    def __init__(self, data_file="data/inventory.json"):
        self.data_file = data_file
        self.medicine_inventory = {}  
        self.medicine_names = set()   
        self.load_data()

    def add_medicine(self, name, stock, price):
        name = name.strip().capitalize()
        if name in self.medicine_names:
            return f"{name} already exists."
        self.medicine_inventory[name] = {"stock": stock, "price": price}
        self.medicine_names.add(name)
        self.save_data()
        return f"{name} added successfully."

    def update_medicine(self, name, stock=None, price=None):
        name = name.strip().capitalize()
        if name not in self.medicine_inventory:
            return f"{name} not found."
        if stock is not None:
            self.medicine_inventory[name]["stock"] = stock
        if price is not None:
            self.medicine_inventory[name]["price"] = price
        self.save_data()
        return f"{name} updated."

    def delete_medicine(self, name):
        name = name.strip().capitalize()
        if name in self.medicine_inventory:
            del self.medicine_inventory[name]
            self.medicine_names.remove(name)
            self.save_data()
            return f"{name} removed."
        return f"{name} not found."

    def search_medicine(self, name):
        name = name.strip().capitalize()
        return self.medicine_inventory.get(name, None)

    def get_all_medicines(self):
        return self.medicine_inventory

    def save_data(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, "w") as f:
            json.dump(self.medicine_inventory, f, indent=4)

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                self.medicine_inventory = json.load(f)
                self.medicine_names = set(self.medicine_inventory.keys())


# if __name__ =="__main__":
#     ph = Pharmacy()

# # print(ph.add_medicine("Panadol", 50, 20))
# print(ph.update_medicine("Panadol", stock=60))
# # print(ph.search_medicine("Panadol"))
# # print(ph.delete_medicine("Panadol"))
