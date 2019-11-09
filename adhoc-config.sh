#! /bin/bash

sudo service network-manager stop
sudo ip link set wlp2s0 down
sudo iwconfig wlp2s0 mode Ad-Hoc
sudo iwconfig wlp2s0 channel 4
sudo iwconfig wlp2s0 essid 'CUWIRELESS'

sudo ip link set wlp2s0 up