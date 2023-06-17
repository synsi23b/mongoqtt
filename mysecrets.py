from dotenv import load_dotenv
import os

# load dotenv and mimic the secrets file on ESP IOT device
load_dotenv()

SSID="noneed"
WIFIKEY="noneed"
MQTTHOST=os.getenv("MQTT_HOST")
MQTTUSER=os.getenv("MQTT_USER")
MQTTPASS=os.getenv("MQTT_PASS")
MQTTBASE=os.getenv("BASE_TOPIC")
MQTTCLIENT="localtest"