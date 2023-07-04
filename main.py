import machine
import utime as time
from dht import DHT11
import ubinascii
from umqttsimple import MQTTClient

CLIENT_ID = ubinascii.hexlify(machine.unique_id())
MQTT_BROKER = "io.adafruit.com"
PORT = 1883
ADAFRUIT_USERNAME = "Julval"
ADAFRUIT_PASSWORD = "password"
PUBLISH_TOPIC = b"Julval/f/IOTproject"

pin = machine.Pin(2, machine.Pin.OUT, machine.Pin.PULL_DOWN)
sensor = DHT11(pin)

def reset():
    print("Resetting...")
    time.sleep(5)
    machine.reset()

def get_sensor_reading():
    time.sleep(4)
    try:
        t = sensor.temperature
        return t
    except:
        print("An exception occurred")
        return None

def main():
    print(f"Begin connection with MQTT Broker :: {MQTT_BROKER}")
    mqttClient = MQTTClient(
        CLIENT_ID, MQTT_BROKER, PORT, ADAFRUIT_USERNAME, ADAFRUIT_PASSWORD, keepalive=60
    )

    mqttClient.connect()
    print(f"Connected to MQTT Broker :: {MQTT_BROKER}")
    
    while True:
        temperature = get_sensor_reading()
        if temperature is not None:
            mqttClient.publish(PUBLISH_TOPIC, "{}".format(temperature))
            print("Sent temperature...")
       

if __name__ == "__main__":
    while True:
        try:
            main()
        except OSError as e:
            print("Error: " + str(e))
            reset()