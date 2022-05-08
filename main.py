import time
import network
from dht import DHT11
from machine import Pin
from umqtt.simple import MQTTClient
dht = DHT11(Pin(15))
tempMeasured = 0
humidityMeasured = 0


#connecting to wifi
SSID = "WAR_5G"
PASSWORD = "az671005"
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.disconnect()
wlan.scan()
wlan.config('mac')

if not wlan.isconnected():
  print('connecting to network...')
  wlan.connect(SSID, PASSWORD)
  while not wlan.isconnected():
    print('network config:', wlan.ifconfig())

server = "mqtt.favoriot.com"
client = MQTTClient("umqtt_client", server, user="E9lYZoHNsmF84UCHQMJoONZPOQFqA9fj", password="E9lYZoHNsmF84UCHQMJoONZPOQFqA9fj")
while wlan.isconnected():
  dht.measure()
  tempMeasured = dht.temperature()
  humidityMeasured = dht.humidity()
  print("measuring...")
  print(tempMeasured, humidityMeasured)
  topic = "E9lYZoHNsmF84UCHQMJoONZPOQFqA9fj/v2/streams"
  client.connect()
  print("ok")
  data = '{"temperature":"'+str(tempMeasured)+'", "humidity":"'+str(humidityMeasured)+'" }}'
  client.publish(topic, '{"device_developer_id": "ESP32@irash10", "data":' + data)
  client.disconnect()
  time.sleep(5)