# Manual script to set up a Raspberry Pi from host
read -p "This step will manually guide you through the setup process. Press Enter after you have completed each step, or enter data if it prompts you."
read -p "1. Download these files:
    * balenaEtcher: https://www.balena.io/etcher/
    * Raspbian OS: https://downloads.raspberrypi.org/raspios_full_armhf_latest
    * VNC viewer: https://www.realvnc.com/en/connect/download/viewer/
    * Fing App: https://www.fing.com/products/fing-app
    * (Windows only) PuTTY: https://www.putty.org/
"
read -p "2. Unzip Raspbian
"
read -p "3. Open balenaEtcher and flash Raspbian OS onto the SD card
"
read -p "4. Open a command line in a separate shell and enter the SD card directory (should be named 'boot')
"
read -p "5. Run:
    touch ssh
    touch wpa_supplicant.conf
"
read -p "6. Enter WiFi name: " wifiname
read -p "7. Enter WiFi password: " wifipassword
read -p "8. 2-letter country code (see https://en.wikipedia.org/wiki/ISO_3166-1#Current_codes): " countrycode
read -p "9. Copy the following text into wpa_supplicant.conf:

ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=${countrycode}

network={
 ssid=\"${wifiname}\"
 psk=\"${wifipassword}\"
}
"
read -p "10. Safely eject the SD card
"
read -p "11. Open the Fing app while connected to your WiFi network. Press 'Scan for devices' and take a screenshot to see which devices are connected already.
"
read -p "12. Put the SD card into the Raspberry Pi and plug it in. Wait a minute for the Pi to boot.
"
read -p "13. In the Fing app, scan for devices again. A new device should appear.
"
read -p "14. What is the IP of the new device? IP = " ip
read -p "15. Depending on your OS:
    * Windows: Open PuTTY, enter ${ip} into the hostname field and click Open
    * Other: Run: ssh ${ip}
You should get a login prompt.
"
read -p "16. Log in with the default credentials (username: pi, password: raspberry)"
read -p "17. Once you have a shell, change the password:
    passwd pi
You should get a CLI to update the password. Change it to something secure.
"
read -p "18. Configure the Pi to use the camera etc.
    sudo raspi-config
You should get a GUI.
"
read -p "19. Go to 'Interfacing Options' and enable everything (just in case). You should at least enable camera and VNC.
"
read -p "20. Press 'Finish' and say yes to reboot. Wait a minute for the Pi to reboot.
"
read -p "21. Open VNC viewer and enter ${ip}.
"
read -p "22. Go to Preferences -> Raspberry Pi configuration and change the resolution to e.g. 1280x720
"
read -p "23. Open a command line in the RPi and run:
    raspistill -o ~/test.jpg
"
read -p "24. Open test.jpg and see that it's a picture.
"
read -p "25. That's all!
"
