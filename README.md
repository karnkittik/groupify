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

## Config AdHoc
```
sudo service network-manager stop
sudo ip link set wlp2s0 down
sudo iwconfig wlp2s0 mode ad-hoc
sudo iwconfig wlp2s0 channel 4
sudo iwconfig wlp2s0 essid 'CUWIRELESS'

sudo ip link set wlp2s0 up
```