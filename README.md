# TD_IoT


##Start linux


open putty : https://the.earth.li/~sgtatham/putty/latest/w64/putty.exe or teraterm or any SSH terminal

connect to 192.168.7.2
login : debian
pass : temppwd


###Connect to the WiFi

root@BeagleBone:~# wpa_cli -i wlan0
wpa_cli v2.9
Copyright (c) 2004-2019, Jouni Malinen <j@w1.fi> and contributors

This software may be distributed under the terms of the BSD license.
See README for more details.

Interactive mode

> scan
OK
<3>CTRL-EVENT-SCAN-STARTED 
<3>CTRL-EVENT-SCAN-RESULTS 
<3>CTRL-EVENT-NETWORK-NOT-FOUND 
> scan_results
bssid / frequency / signal level / flags / ssid
b4:fb:e4:f5:7b:d2	5180	-86	[WPA2-PSK-CCMP][ESS]	XYZA
be:fb:e4:f5:7b:d2	5180	-87	[WPA2-PSK-CCMP][ESS]	BeagleBone
ba:fb:e4:f5:7b:d2	5180	-87	[WPA2-PSK-CCMP][ESS]	XYZB
c2:fb:e4:f5:7b:d2	5180	-87	[WPA2-PSK-CCMP][ESS]	XYZC
> 
> add_network
1
> set_network 1 ssid "BeagleBone"
OK
> set_network 1 psk "BeagleBone"
OK
> enable_network 1
OK
<3>CTRL-EVENT-SCAN-STARTED 
<3>CTRL-EVENT-SCAN-RESULTS 
<3>SME: Trying to authenticate with be:fb:e4:f5:7b:d2 (SSID='BeagleBone' freq=5180 MHz)
<3>Trying to associate with be:fb:e4:f5:7b:d2 (SSID='BeagleBone' freq=5180 MHz)
<3>Associated with be:fb:e4:f5:7b:d2
<3>CTRL-EVENT-SUBNET-STATUS-UPDATE status=0
<3>WPA: Key negotiation completed with be:fb:e4:f5:7b:d2 [PTK=CCMP GTK=CCMP]
<3>CTRL-EVENT-CONNECTED - Connection to be:fb:e4:f5:7b:d2 completed [id=1 id_str=]


###Test Internet connection 

ping google.com

expected results : 
PING google.com(par10s49-in-x0e.1e100.net (2a00:1450:4007:80c::200e)) 56 data bytes
64 bytes from par10s49-in-x0e.1e100.net (2a00:1450:4007:80c::200e): icmp_seq=1 ttl=115 time=50.8 ms
64 bytes from par21s11-in-x0e.1e100.net (2a00:1450:4007:80c::200e): icmp_seq=2 ttl=115 time=16.6 ms
64 bytes from par21s11-in-x0e.1e100.net (2a00:1450:4007:80c::200e): icmp_seq=3 ttl=115 time=17.3 ms
64 bytes from par21s11-in-x0e.1e100.net (2a00:1450:4007:80c::200e): icmp_seq=4 ttl=115 time=15.2 ms

stop : ctrl+c




##Clone Python Script

git clone https://github.com/tgaberan/TD_IoT.git


###install paho mqtt

pip3 install paho-mqtt


### run python script

python IoT_TD_sub.py

open the nodered url : http://213.32.88.153:1880/dashboard/


###install temp lib
cd ~
git clone https://github.com/adafruit/Adafruit_Python_MCP9808.git
cd Adafruit_Python_MCP9808/
sudo python setup.py  install


