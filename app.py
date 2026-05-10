import json
import logging
import os
import sys

os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    filename='logs/provisioning.log', 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class Machine:
    def __init__(self, name, os_type, cpu, ram):
        self.data = {"name": name, "os": os_type, "cpu": cpu, "ram": ram}

    def provision(self):
        msg = f"Provisioning {self.data['name']}: {self.data['os']}, {self.data['cpu']}, {self.data['ram']}"
        logging.info(msg)
        print(msg)

def get_config_from_env():
    name = os.getenv("MACHINE_NAME", "default-server")
    os_type = os.getenv("MACHINE_OS", "Ubuntu")
    cpu = os.getenv("MACHINE_CPU", "1")
    ram = os.getenv("MACHINE_RAM", "1Gi")
    
    return Machine(name, os_type, cpu, ram)

if __name__ == "__main__":
    print("Provisioning service started...")
    
    try:
    
        server = get_config_from_env()
        server.provision()
        print(f"Data state: {json.dumps(server.data)}")
        
        import time
        while True:
            time.sleep(3600)
            
    except Exception as e:
        logging.error(f"Critical Error: {e}")
        print(f"Error: {e}")
        sys.exit(1)
