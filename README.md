## Prerequisite
```
python3 -m pip install bitarray
sudo apt-get install -y python3-tk
```


## OLSR config
```
git clone https://github.com/OLSR/OONF.git
sudo apt-get install -y cmake
sudo apt-get install -y build-essential libnl-3-dev
cd build
cmake ..
make

sudo ./olsrd2_static wlp2s0 lo
```

## Start app
```
sudo python3 ./main.py
```

## Simulate Multi-hop by fix route
### The topology will be like this to test multihop.
** if is interface, please change wlp3s0 with you wireless interface **
M <-> A <-> L
```
M: 192.168.1.9
A: 192.168.1.10
L: 192.168.1.11
```
### PC M (192.168.1.9)
```
telnet 127.0.0.1 2009
route get
route add src-ip 192.168.1.9 gw 192.168.1.10 dst 192.168.1.11 if wlp3s0
route del src-ip 192.168.1.9 dst 192.168.1.11 if wlp3s0
```
### PC L (192.168.1.11)
```
telnet 127.0.0.1 2009
route get
route add src-ip 192.168.1.11 gw 192.168.1.10 dst 192.168.1.9 if wlp3s0
route del src-ip 192.168.1.11 dst 192.168.1.9 if wlp3s0
```

## Step
1. open termainal then run
```
cd /OONF/build
sudo ./olsrd2_static wlp2s0 lo
```
2. open another terminal and change directory to groupify
```
cd /groupify
```
3. copy `adhoc-config.example.sh` to be `adhoc-config.sh`
```
cp adhoc-config.example.sh adhoc-config.sh
```
4. In `adhoc-config.sh`, if you would like to auto assign ip address via olsrd, please comment the last line (to be like the following)
```
# sudo ip addr add 192.168.1.9/24 dev $iface
```
5. run following command to config adhoc and start app
```
sudo bash adhoc-config.sh
sudo python3 main.py
```
6. change to manage mode
```
sudo bash manage-config.sh
```
