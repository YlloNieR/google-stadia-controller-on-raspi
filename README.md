# google-stadia-controller-on-raspi
How to setup a Raspberry Pi 4 Model B to use a Google Stadia Controller as Mouse

How to check bluetooth devices on raspi
```bash
bluetoothctl devices
```

get events on raspi after bt connection
```bash
sudo evtest /dev/input/event5
```