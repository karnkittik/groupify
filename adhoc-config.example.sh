#! /bin/bash

iface=`ip -br link | grep -v LOOPBACK | awk '{print $1}'`

sudo service network-manager stop
sleep 1s

sudo ip link set $iface down
sleep 1s

sudo iwconfig $iface mode Ad-Hoc
sudo iwconfig $iface channel 1
sudo iwconfig $iface essid 'CUWIRELESS'

sudo ip link set $iface up
sleep 1s

sudo ip addr add 192.168.1.9/24 dev $iface