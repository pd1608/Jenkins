import unittest
from napalm import get_network_driver

# Device credentials (update with actual info)
expected_loopback_ip = "10.1.3.1/24"

def get_loopback99_ip():
    device = {
        'hostname': '198.51.100.13',
        'username': 'lab',
        'password': 'lab123',
        'optional_args': {},
        'driver': 'ios',
    }
    try:
        driver = get_network_driver(device['driver'])
        with driver(
            hostname=device['hostname'],
            username=device['username'],
            password=device['password'],
            optional_args=device['optional_args']
        ) as device_conn:

            interfaces = device_conn.get_interfaces_ip()
            loopback_info = interfaces.get('Loopback99')

            if loopback_info:
                ipv4_info = loopback_info.get('ipv4')
                if ipv4_info:
                    ip, details = list(ipv4_info.items())[0]
                    prefix_length = details['prefix_length']
                    return f"{ip}/{prefix_length}"
            return None

    except Exception as e:
        print("Error fetching loopback IP:", e)
        return None

def get_ospf_instance_count():
    device = {
        'hostname': '198.51.100.11',
        'username': 'lab',
        'password': 'lab123',
        'optional_args': {},
        'driver': 'ios',
    }
    try:
        driver = get_network_driver(device['driver'])
        with driver(
            hostname=device['hostname'],
            username=device['username'],
            password=device['password'],
            optional_args=device['optional_args']
        ) as device_conn:

            config = device_conn.get_config(retrieve='running')['running']
            ospf_instances = []

            # Look for 'router ospf' declarations
            for line in config.splitlines():
                line = line.strip()
                if line.startswith("router ospf"):
                    parts = line.split()
                    if len(parts) >= 3:
                        ospf_instances.append(parts[2])

            unique_instances = set(ospf_instances)
            return len(unique_instances)

    except Exception as e:
        print("Error fetching OSPF instance count:", e)
        return None

def ping_from_router():
    device = {
        'hostname': '198.51.100.12',
        'username': 'lab',
        'password': 'lab123',
        'optional_args': {},
        'driver': 'ios',  # You can specify 'ios' or any other driver based on your device
    }

    # Getting the network driver for the specific device
    driver = get_network_driver(device['driver'])

    try:
        # Establish a connection to the device
        with driver(device['hostname'], device['username'], device['password'], optional_args=device['optional_args']) as device_connection:
            # Perform a ping test from the device
            # Source IP is specified in the ping command parameters.
            result = device_connection.ping('10.1.5.1', source='198.51.100.12')

            # Check if the ping was successful (checking 'success' rate)
            if result.get('success', 0) == 100:
                print("Ping successful with 100% success rate.")
                return True
            else:
                print(f"Ping failed with {result.get('success', 0)}% success rate.")
                return False

    except Exception as e:
        print("SSH/Ping Error:", e)
        return False

class TestRouterConfigNAPALM(unittest.TestCase):

    def test_loopback99_ip(self):
        """Test if Loopback99 has IP 10.1.3.1/24"""
        actual_ip = get_loopback99_ip()
        self.assertEqual(actual_ip, expected_loopback_ip,
                         f"Expected {expected_loopback_ip}, but got {actual_ip}")

    def test_single_ospf_instance(self):
        """Test if the router has only one OSPF instance"""
        count = get_ospf_instance_count()
        self.assertEqual(count, 1,
                         f"Expected 1 OSPF instance, but found {count}")
    
    def test_ping_loopback(self):
        """Test ping from R2 loopback to R5 loopback"""
        result = ping_from_router()
        self.assertTrue(result, f"Ping to R5 loopback from R2 failed")

if __name__ == '__main__':
    unittest.main()


