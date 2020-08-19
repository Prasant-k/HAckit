import subprocess
import optparse
import re
print('''
       __  ___                 ________                               
      /  |/  /___ ______      / ____/ /_  ____ _____  ____ ____  _____
     / /|_/ / __ `/ ___/_____/ /   / __ \/ __ `/ __ \/ __ `/ _ \/ ___/
    / /  / / /_/ / /__/_____/ /___/ / / / /_/ / / / / /_/ /  __/ /    
   /_/  /_/\__,_/\___/      \____/_/ /_/\__,_/_/ /_/\__, /\___/_/     

''')

def args():
    input_object = optparse.OptionParser()
    input_object.add_option("-i", "--interface", dest="interface", help="Enter interface name")
    input_object.add_option("-m", "--mac", dest="mac", help="Enter new mac address")
    values=input_object.parse_args()[0]
    if not values.interface:
        input_object.error("[-] Please specify the interface , use --help for more info")
    elif not values.mac:
        input_object.error("[-] Please specify the MAC address , use --help for more info")
    elif re.match(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", values.mac)==None:
        input_object.error("[-] Invalid MAC address [00:00:00:00:00:00]")
    return values

def change_mac(interface,mac):
    print("[+] Changing MAC address of " + interface + " to " +mac)
    try:
        subprocess.call(["ifconfig", interface, "down"])
        subprocess.call(["ifconfig", interface, "hw", "ether", mac])
        subprocess.call(["ifconfig", interface, "up"])
    except:
        print("[-] use ifconfig to view network interface")
        exit()
    return check_mac(interface)                    ##return changed mac
def check_mac(interface):
    try:
        output_result = subprocess.check_output(["ifconfig", interface])      ## handling error if interface not found
    except:
        print("[-] use ifconfig to view network interface")
        exit()
    mac_address = re.search(r" \w\w:\w\w:\w\w:\w\w:\w\w:\w\w ", str(output_result))
    if mac_address:
        return mac_address.group(0).strip()             ## return mac address and strip to remove traling an leading spaces and tab
    else:
        print("[-] No MAC address found")
        exit()

values=args()
previous_mac=check_mac(values.interface)
print("Current MAC = "+previous_mac)
current_mac=change_mac(values.interface, values.mac)
if previous_mac != current_mac:
    print("[+] MAC address is successfully changed to "+current_mac)
else:
    print("[-] MAC address did not changed")
