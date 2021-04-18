# Domoticz System Printer

A library written in python that takes the current printer status and sends it to Domoticz and allows you to clear the print queue.

## Requirements

- `Linux` based device (like `Raspberry Pi`) with installed `Python 3`
- Printer connected and installed
- The following python packages installed on device: `requests`
- The script saves the last read printer status in a file to avoid sending redundant requests to Domoticz, so make sure it will have permission to write to that location

## Installation and usage

### Prepare scripts

Install required Python packages:

```bash
pip3 install requests
```

Clone the repository to any directory on your device, e.g. to the home directory.

```bash
cd
git clone https://github.com/paulomac1000/Domoticz-System-Printer
```

Change to the script's directory

```bash
cd Domoticz-System-Printer
```

### Printer status display function

Open the Domoticz panel, expand "Setup", select "Hardware" and add a device with the name of your printer, e.g. "HP Printer", type "Dummy (Does nothing, use for virtual switches only)". Leave the rest of the options unchanged and press the "Add" button.

At the newly created Hardware in the "Type" column, press the "Create Virtual Sensors" button. A modal will appear in which you must enter the name of the sensor "Printer status" and the type "Text".

Now go to the "Utility" tab and click the "Edit" button on the newly created item. At the top of the open modal you have the "Idx" field - write down its value somewhere.

Go back to the console. First, check the name of your printer - use the command below.

```bash
lpstat -p -d
```

Then open the edit script for checking the status of the device.

```bash
nano systemPrinterStatus.py
```

Go to line 6 and replace the printer name with the one you just read.

```python
printer_name = 'your printer name'
```

Go to line 8 (to the code below) and replace this url with your Domoticz url, or leave the default configuration if the script is run on the same machine.

```python
DOMOTICZ_SERVER = "127.0.0.1:8080"
```

Go to line 12 and enter the Idx of the device you added.

```python
printer_device_id = 99
```

Close the file with `ctrl+x` and save changes. To run a script, run it from the command line.

```bash
python3 systemPrinterStatus.py
```

If everything was working fine you can add the script to the `crontab`.

```bash
crontab -e
```

`crontab` doesn't handle calls less than 1 minute, and we'd like to call it every 15 seconds so we don't overlook the status change. To do this, we'll use a workaround - we'll add the script 4 times as executed every minute, but delay each entry by 15 seconds. So add the following entry to the `crontab` file:

```bash
* * * * * sleep 00; timeout 15s python3 /home/pi/Domoticz-System-Printer/systemPrinterStatus.py
* * * * * sleep 15; timeout 15s python3 /home/pi/Domoticz-System-Printer/systemPrinterStatus.py
* * * * * sleep 30; timeout 15s python3 /home/pi/Domoticz-System-Printer/systemPrinterStatus.py
* * * * * sleep 45; timeout 15s python3 /home/pi/Domoticz-System-Printer/systemPrinterStatus.py
```

Close the file with `ctrl+x` and save changes.

### Clear print queue function

Go to the script directory in Domoticz's home directory.

```bash
cd /home/pi/domoticz/scripts
```

Create a script that performs a cleanup request from the print queue by calling systemPrinterClearQueue.py from your home directory.

```bash
nano printer_clearQueue.sh
```

And paste the following content into it.

```bash
#!/bin/bash
python3 /home/pi/Domoticz-System-Printer/systemPrinterClearQueue.py
```

Close the file with `ctrl+x` and save changes.

Open the Domoticz panel, expand "Setup", select "Hardware" and find the previously added hardware with the name of your printer.

In the "Type" column, press the "Create Virtual Sensors" button. A modal will appear in which you must enter the name of the sensor "Clear print queue" and the type "Switch".

Now go to the "Switches" tab and click the "Edit" button on the newly created item. Select switch Type `Push On Button` and enter `script://printer_clearQueue.sh` in the "On Action" field. Save the changes and check if it works.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Show your support

Please star this repository if this project helped you!

## License
[MIT](https://choosealicense.com/licenses/mit/)

## See also
Blog post on [cleverblog.pl](https://cleverblog.pl/?p=208)