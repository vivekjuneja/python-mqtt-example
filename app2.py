
import app

client = app.MQTTClient("mqtt://bszhbvxe:c98S4q4Bpifl@m24.cloudmqtt.com:19448")
client.connect()
client.subscribeToTopic("temp")

