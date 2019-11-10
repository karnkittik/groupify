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
4. In `adhoc-config.sh`, change the interface from `wlp4s0` to your wireless interface.
5. run following command to config adhoc and start app
```
sudo bash adhoc-config.sh
sudo python3 main.py
```
6. change to manage mode
```
sudo bash manage-config.sh
```