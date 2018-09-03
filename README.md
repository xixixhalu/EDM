# EDMToolkit

## Setup

`pip install -r requirements.txt`

* Should pull in most of the dependencies. Had to change host from
'localhost' to '0.0.0.0' to connect to app running in the VM. I
added a host only adapter in VBox so host/guest are in a LAN.

* Updating the packages might have broken some things. When registering,
 the server was complaining about taking timestamp difference.
 [StackOverflow fix](https://stackoverflow.com/questions/796008/cant-subtract-offset-naive-and-offset-aware-datetimes)
