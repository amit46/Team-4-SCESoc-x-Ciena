"""
Project Completed By:
    Amit Kunkulol
    Sanvi Kaushik
    Justin Koops
"""

import time

class IPManager:
    LEASE_DURATION = 60  # Lease duration

    def __init__(self):
        self.leased_ips = {} # To store the leased

    def allocate_ip(self):
        if not self.leased_ips:
            # If no leased IPs, create the first one
            ip = "0.0.0.0"
        else:
            # Find the highest leased IP and increment it, handling carryover
            highest_ip = max(self.leased_ips, key=self.leased_ips.get)
            ip_parts = list(map(int, highest_ip.split('.')))
            ip_parts[3] += 1

            # Incrementing the ip
            for i in range(3, 0, -1):
                if ip_parts[i] > 255:
                    ip_parts[i] = 0
                    ip_parts[i-1] += 1

            ip = ".".join(map(str, ip_parts)) 

        self.leased_ips[ip] = time.time()
        return ip

    def release_ip(self, ip):
        # Releases ip
        if ip in self.leased_ips:
            del self.leased_ips[ip]
            return ip
        return None

    def is_ip_available(self, ip):
        # Checks status
        return ip not in self.leased_ips

    def renew_ip(self, ip):
        # Renews ip - resetting time
        current_time = time.time()
        if ip in self.leased_ips:
            self.leased_ips[ip] = current_time
            return True
        return False

    def check_expired_leases(self):
        # Runs through all ips to check if lease expired
        current_time = time.time()
        expired_ips = [ip for ip, timestamp in self.leased_ips.items() if current_time - timestamp >= self.LEASE_DURATION]
        for expired_ip in expired_ips:
            print(f"Lease expired for IP: {expired_ip}")
            del self.leased_ips[expired_ip]

    def cleanup(self):
        # Performing cleanup
        self.leased_ips.clear()


ip_manager = IPManager()
try:
    while True:
        user_input = input("Enter command (ASK/RELEASE/RENEW/STATUS/EXIT): ").upper()

        # Split the user input into command and optional IP address
        command_parts = user_input.split(maxsplit=1)
        command = command_parts[0]

        if command == "ASK":
            allocated_ip = ip_manager.allocate_ip()
            print(f"Allocated IP: {allocated_ip}")

        elif command == "RELEASE":
            if len(command_parts) == 2:
                ip_to_release = command_parts[1]
                released_ip = ip_manager.release_ip(ip_to_release)
                if released_ip:
                    print(f"Released IP: {released_ip}")
                else:
                    print(f"IP {ip_to_release} not found in leased IPs.")
            else:
                print("Invalid Input!")

        elif command == "RENEW":
            if len(command_parts) == 2:
                ip_to_renew = command_parts[1]
                if ip_manager.renew_ip(ip_to_renew):
                    print(f"Lease renewed for IP: {ip_to_renew}")
                else:
                    print(f"IP {ip_to_renew} not found in leased IPs.")
            else:
                print("Invalid Input!")

        elif command == "STATUS":
            if len(command_parts) == 2:
                ip_to_check = command_parts[1]
                availability_status = ip_manager.is_ip_available(ip_to_check)
                print(f"IP {ip_to_check} is available: {availability_status}")
            else:
                print("Invalid Input!")

        elif command == "EXIT":
            print("Exiting.")
            break

        else:
            print("Invalid command. Valid commands are ASK, RELEASE, STATUS, and EXIT.")

        ip_manager.check_expired_leases()

except KeyboardInterrupt:
    print("\nKeyboardInterrupt detected. Cleaning up...")
    ip_manager.cleanup()
    print("Cleanup complete. Exiting.")
except Exception as e:
    print(f"An error occurred: {str(e)}")
    ip_manager.cleanup()
    print("Cleanup complete. Exiting.")