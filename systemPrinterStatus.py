import os.path
import subprocess
import requests

# printer configuration
printer_name = 'your printer name'

# domoticz configuration
DOMOTICZ_SERVER   = "127.0.0.1:8080"
DOMOTICZ_USERNAME = ""
DOMOTICZ_PASSWORD = ""
printer_device_id = 99

# app config
status_file_name = 'status.data'

def save_status_to_file(status):
    f = open(status_file_name, "w")
    f.write(status)
    f.close()
    
def read_status_from_file():
    if not os.path.isfile(status_file_name):
        return ""
    file = open(status_file_name, "r") 
    return file.read()

def obtain_printer_status():
    out = subprocess.Popen(['lpstat', '-p', printer_name], 
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
    stdout,stderr = out.communicate()
    if stdout is not None:
        stdout = str(stdout)
        if "Invalid destination" in stdout:
            return "Offline"
        elif "is idle" in stdout:
            return "Idle"
        else:
            return "Active"
            
def send_to_domoticz(status):
    request_url = 'http://' + DOMOTICZ_SERVER + '/json.htm?type=command&param=udevice&idx=' + str(printer_device_id) + '&nvalue=0&svalue=' + status
    if (DOMOTICZ_USERNAME and DOMOTICZ_PASSWORD):
        requests.get(request_url, auth=(DOMOTICZ_USERNAME, DOMOTICZ_PASSWORD))
    else:
        requests.get(request_url)

printer_status = obtain_printer_status()
print('Printer status: ' + printer_status)
previous_printer_status = read_status_from_file()
print('Previous printer status: ' + previous_printer_status)

if printer_status != previous_printer_status:
    try:
        save_status_to_file(printer_status)
        send_to_domoticz(printer_status)
    except Exception as e:
        error_message = "Handle printer status app gives an exception: \"" + str(e) + "\"."
        print(error_message)