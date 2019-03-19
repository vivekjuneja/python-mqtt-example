# Copyright (c) 2010,2011 Roger Light <roger@atchoo.org>
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
# 3. Neither the name of mosquitto nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import paho.mqtt.client as mqtt
import os, urlparse


class MQTTClient(object): 

	mqttc = None
	cloudmqttUrl=None

	def __init__(self, cloudmqttUrl):
		self.cloudmqttUrl=cloudmqttUrl

	# Define event callbacks
	def on_connect(self, client, userdata, flags, rc):
	    print("rc: " + str(rc))

	def on_message(self, client, obj, msg):
	    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

	def on_publish(self, client, obj, mid):
	    print("mid: " + str(mid))

	def on_subscribe(self, client, obj, mid, granted_qos):
	    print("Subscribed: " + str(mid) + " " + str(granted_qos))

	def on_log(self, client, obj, level, string):
	    print(string)

	def connect(self):
		self.mqttc = mqtt.Client()
		# Assign event callbacks
		self.mqttc.on_message = self.on_message
		self.mqttc.on_connect = self.on_connect
		self.mqttc.on_publish = self.on_publish
		self.mqttc.on_subscribe = self.on_subscribe

		# Uncomment to enable debug messages
		self.mqttc.on_log = self.on_log

		# Parse CLOUDMQTT_URL (or fallback to localhost)
		url_str = os.environ.get('CLOUDMQTT_URL', self.cloudmqttUrl)
		url = urlparse.urlparse(url_str)
		topic = url.path[1:] or 'test'
		print("%s %s %s %s %s" %(url.username, url.password, url.path, url.hostname, url.port))
		# Connect
		self.mqttc.username_pw_set(url.username, url.password)
		self.mqttc.connect(url.hostname, url.port)

	def publishToTopic(self, topic, message):
		self.mqttc.publish(topic, message)


	def subscribeToTopic(self, topic):
		self.mqttc.subscribe(topic, 0)
		# Continue the network loop, exit when an error occurs
		rc = 0
		while rc == 0:
		    rc = self.mqttc.loop()
		print("rc: " + str(rc))




