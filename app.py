import json
import logging
import os


os.makedirs('logs', exist_ok=True)
logging.basicConfig(filename='logs/provisioning.log', level=logging.INFO, format='%(asctime)s - %(message)s')

class Machine:
    def __init__(self, name, os_type, cpu, ram):
        self.data = {"name": name, "os": os_type, "cpu": cpu, "ram": ram}

    def provision(self):
        msg = f"Provisioning {self.data['name']}: {self.data['os']}, {self.data['cpu']}, {self.data['ram']}"
        logging.info(msg)
        print(msg)

def get_user_input():

    name = input("Enter machine name: ")
    os_type = input("Enter OS (Ubuntu/CentOS): ")
    cpu = input("Enter CPU: ")
    ram = input("Enter RAM: ")
    return Machine(name, os_type, cpu, ram)

if __name__ == "__main__":
    print("Provisioning started.")
    
    try:

        server = get_user_input()
        server.provision()
        print(server.data)
        
    except Exception as e:
        logging.error(f"Error: {e}")
        print(f"Error: {e}")