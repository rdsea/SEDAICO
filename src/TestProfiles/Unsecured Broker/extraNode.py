import sched, time
import paho.mqtt.client as mqtt
import os


def info(title):
    print(f"\n{title}")
    print('parent process:', os.getppid())
    print('process id:', os.getpid())



def sensor_simulator(topic, broker_url, broker_port, rate):
    info("Spawned a new program")
    s = sched.scheduler(time.time, time.sleep)
    client = mqtt.Client()
    client.connect(broker_url, broker_port, 60)

    # This is the Publisher
    def send_mqtt_requests():
        client.publish(topic, "RANDOM DATA")
        print("publishing random data")
        s.enter(1/int(rate), 1, send_mqtt_requests)

    s.enter(1/int(rate), 1, send_mqtt_requests)
    s.run()

    client.disconnect()
