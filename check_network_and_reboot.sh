#!/bin/bash
ping -c4 8.8.8.8  # Try pinging Google's website 4 times
if [ "$?" -ne "0" ]; then  # If ping fails (returns a non-zero exit code)
    systemctl stop vncTkinter
    printf "AT\r\n" > /dev/ttyUSB2
    sleep 1
    printf "AT+CFUN=0\r\n" > /dev/ttyUSB2
    sleep 10
    printf "AT+QPOWD\r\n" > /dev/ttyUSB2
    # echo "power off"
    sleep 20
    printf "AT+CFUN=1,1\r\n" > /dev/ttyUSB2
    sleep 40
    # echo "reset cgatt"
    printf "AT+CGATT=1\r\n" > /dev/ttyUSB2
    sleep 3
    /usr/sbin/reboot # Schedule reboot in 5 minutes with a message
fi
# */5 * * * * if [ $(echo $(vcgencmd measure_volts ain1| grep -oE '[0-9\.]+')"<0.85356"|bc) -eq 1 ]; then sudo 
# timeout 1 sh -c 'echo "AT+QPOWD\r\n" > /dev/ttyUSB2 ; cat /dev/ttyUSB2 > /home/dty717/shutdownByVol>
# ByVoltage.txt' & sudo /sbin/shutdown -h now;fi


# chmod +x check_network_and_reboot.sh
# 30 1 * * * path/check_network_and_reboot.sh