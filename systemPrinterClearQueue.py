import subprocess

def clear_printer_queue():
    out = subprocess.Popen(['cancel', '-a', '-x'], 
           stdout=subprocess.PIPE, 
           stderr=subprocess.STDOUT)
    stdout,stderr = out.communicate()

try:
    clear_printer_queue()
except Exception as e:
    error_message = "Clear printer queue app gives an exception: \"" + str(e) + "\"."
    print(error_message)