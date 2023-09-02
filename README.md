# mongoqtt

this repo contains 3 things. 

- The first is a paho mqtt client that connects to a mongo DB to write out messages on "BASE_TOPIC/log"

- The same process also launches a python webio which launches "apps" defined at the start of the file webio.py

- The last part is a layer on top of the mycropython robust mqtt client which implements a formater for the logging messages and a helper to format / subscribe to the apps on the webio


## mqtt client / webio

define topics and their handlers in pahohandlers.py

define webio apps and register them at the start of webio.py

build the container and define the environment variables in the compose file to connect to the db / mqtt broker.


## mycropython client

copy the file `myumqtt.py`, `myumqtthandler.py` and `mysecrets.py` to the mycropython device. To subscribe to the webio, implement the callbacs in myumqtthandler.py and respond using the clients publish function. The messages have to be json parsable dictionaries and will be expanded with the keys "device" and "c" for counting the packets and discarding duplicates



## environment variables
- `MONGOCON` connection string to the mongo database
- `MQTT_HOST`
- `MQTT_USER`
- `MQTT_PASS`
- `BASE_TOPIC`
- `WEBIO_PASS` password to the webio interface