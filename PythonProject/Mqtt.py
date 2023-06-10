import paho.mqtt.client as mqtt

# MQTT broker details
broker_address = "localhost"
broker_port = 1883
topic = "relay1"

# Callback function for when a new message is received
def on_message(client, userdata, msg):
    print("Received message: " + str(msg.payload.decode()))

# Create an MQTT client instance
client = mqtt.Client()

# Set the callback function for message reception
client.on_message = on_message

# Connect to the MQTT broker
client.connect(broker_address, broker_port)

# Subscribe to the topic
client.subscribe(topic)

# Start the MQTT client loop to continuously check for new messages
client.loop_start()

# Keep the script running until interrupted
try:
    while True:
        pass
except KeyboardInterrupt:
    pass

# Disconnect from the MQTT broker
client.disconnect()