## remove -y program

```sh
sudo apt-get remove -y geany
sudo apt-get remove -y thonny
sudo apt-get purge -y firefox
sudo apt-get purge -y vlc*
sudo apt-get remove -y rpi-imager
sudo apt-get purge -y rpi-connect
sudo apt-get remove -y rpi-firefox-mods
sudo apt-get remove -y agnostics
sudo apt-get remove -y piclone
sudo apt-get remove -y galculator
sudo apt-get remove -y gnome-calculator
sudo apt-get remove -y eom
sudo apt-get remove -y galculator
sudo apt-get remove -y rp-bookshelf
sudo apt-get remove -y evince
sudo apt-get remove -y xarchiver
sudo apt-get remove -y mousepad
sudo apt-get remove -y system-config-printer
sudo apt-get purge -y cups
sudo apt-get purge -y cups-browsed
sudo apt-get purge -y blueman bluez-utils bluez bluetooth pulseaudio-module-bluetooth
sudo apt-get remove -y firmware-atheros
sudo apt-get remove -y firmware-libertas
sudo apt-get remove -y firmware-brcm80211
sudo apt-get remove -y gcc-12
sudo apt-get remove -y g++-12
sudo apt-get remove -y libstdc++-12-dev
sudo apt-get remove -y libllvm15
sudo apt-get remove -y rpinters
sudo apt-get remove -y rp-prefapps

sudo apt-get autoremove -y
sudo apt-get autoclean -y
```
# remove -y file
```sh
sudo rm Bookshelf/BeginnersGuide-5thEd-Eng_v3.pdf

```
## remove -y journalctl and set limit
```sh
sudo journalctl --vacuum-time=1h
sudo journalctl --disk-usage
sudo nano /etc/systemd/journald.conf
# SystemMaxUse=30M
systemd-analyze cat-config systemd/journald.conf
sudo systemctl restart systemd-journald.service
sudo journalctl --disk-usage
```

## remove -y bluetooth module
```sh
sudo rmmod hci_uart
sudo rmmod btbcm
sudo rmmod bnep
sudo rmmod bluetooth
```