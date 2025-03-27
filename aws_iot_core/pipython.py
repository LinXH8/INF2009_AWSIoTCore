# Import required libraries
import time  # For adding delays between message publications
import paho.mqtt.client as mqtt  # MQTT client library for IoT communication
import ssl  # For secure TLS/SSL connections
import json  # For handling JSON data formatting
import _thread as thread  # For creating a separate thread for publishing messages
import psutil  # For accessing system information (CPU usage, etc.)
import json  # Note: json is imported twice (unnecessary duplication)

# Define the callback function that will be triggered when the connection to the MQTT broker is established
def on_connect(client, userdata, flags, rc):
    # Print a message showing the connection result code
    # rc=0 means successful connection, other values indicate errors
    print("Connected with result code "+str(rc))

# Create a new MQTT client instance
client = mqtt.Client()

# Assign the on_connect callback function to the client
client.on_connect = on_connect

# Configure TLS/SSL security for the MQTT connection
# This is essential for secure communication with AWS IoT Core
client.tls_set(
    ca_certs='./rootCA.pem',  # Root CA certificate from AWS
    certfile='./aws-certificate.pem.crt',  # Device certificate
    keyfile='./aws-private.pem.key',  # Device private key
    tls_version=ssl.PROTOCOL_SSLv23  # TLS protocol version
)

# Allow insecure TLS connections (not recommended for production)
# This bypasses hostname verification which can be useful during development
client.tls_insecure_set(True)

# Connect to the AWS IoT Core endpoint with the following parameters:
# - AWS IoT endpoint (unique to each AWS account)
# - Port 8883 (standard port for secure MQTT)
# - Keepalive interval of 60 seconds
client.connect("xxxxxxxx-ats.iot.ap-southeast-1.amazonaws.com", 8883, 60) #Copy endpoint from your AWS IoT Core Console

# Define the function that will run in a separate thread to publish messages
def justADummyFunction(Dummy):
    # Infinite loop to continuously publish messages
    while (1):
        # This commented section explains where you would put real sensor data processing code
        # You could replace the dummy message with actual sensor readings or analytics results
        
        # Create a simple message string
        message = "Hello from INF2009 RaspberryPi Device#1"
        
        # Print the message to the console for debugging
        print(message)
        
        # Publish the message to the "device/data" topic on AWS IoT Core with:
        # - QoS (Quality of Service) level 0 (at most once delivery)
        # - retain flag set to False (message won't be stored by the broker)
        client.publish("device/data", payload=message, qos=0, retain=False)
        
        # Wait for 5 seconds before sending the next message
        # This controls the frequency of message publication
        time.sleep(5)

# Start the message publishing function in a separate thread
# This allows the MQTT client loop to run concurrently with the publishing code
# The second parameter is a tuple containing arguments for the function (here just a string)
thread.start_new_thread(justADummyFunction, ("Create Thread",))

# Start the MQTT client's network loop
# This is a blocking call that processes network traffic and callback functions
# It will run forever until the program is terminated
client.loop_forever()
