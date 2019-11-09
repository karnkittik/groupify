#! /bin/bash

sudo service network-manager stop
sudo ip link set wlp4s0 down
sudo iwconfig wlp4s0 mode Ad-Hoc
sudo iwconfig wlp4s0 channel 4
sudo iwconfig wlp4s0 essid 'CUWIRELESS'

sudo ip link set wlp4s0 up