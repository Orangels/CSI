# -*- coding: utf-8 -*-# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))


def on_message(client, userdata, msg):
    # print(msg.topic + " " + str(msg.payload))
    print(msg.topic + " " + msg.payload.decode('utf-8'))


#   订阅回调
def on_subscribe(client, userdata, mid, granted_qos):
    print("On Subscribed: qos = %d" % granted_qos)
    pass


#   取消订阅回调
def on_unsubscribe(client, userdata, mid):
    print("On unSubscribed: qos = %d" % mid)
    pass


#   发布消息回调
def on_publish(client, userdata, mid):
    print("On onPublish: qos = %d" % mid)
    pass


#   断开链接回调
def on_disconnect(client, userdata, rc):
    print("Unexpected disconnection rc = " + str(rc))
    pass


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.on_disconnect = on_disconnect
client.on_unsubscribe = on_unsubscribe
client.on_subscribe = on_subscribe
client.connect('172.24.220.54', 1883, 600)  # 600为keepalive的时间间隔
client.subscribe('mqtt11', qos=0)
client.loop_forever()  # 保持连接