#!/usr/bin/python3
import time
import pylcddc.client as client
import pylcddc.widgets as widget
import pylcddc.screen as screen
import pylcddc.exceptions as lcdexcept
import paho.mqtt.client as mqtt


# initialise lcd
lcd_host = 'localhost'
lcd_port = '13666'
# compose screen layout
# ##################
# #13:24  Ti=-**.*C#
# #>***%  To=-**.*C#
# ##################

clock = widget.String('clock', 1, 1, time.strftime("%H:%M", time.localtime()))
ti = widget.String('ti', 8, 1, 'Ti=')
ti_v = widget.String('ti_v', 10, 1, '**.*C')
to = widget.String('to', 8, 2, 'Tb=')
to_v = widget.String('to_v', 10, 2, '**.*C')
flame = widget.Icon('flame', 1, 2, widget.Icon.IconType.FF)
flame_v = widget.String('flame_v', 2, 2, '***%')

scr = screen.Screen('Temperature',
                    (clock, ti, ti_v, to, to_v, flame, flame_v),
                    heartbeat=screen.ScreenAttributeValues.Heartbeat.OFF)
c = client.Client(lcd_host, lcd_port)
width, height = (c.server_information_response.lcd_width,
                 c.server_information_response.lcd_height)
c.add_screen(scr)


# initialise mqtt
broker = "broker.hivemq.com"  # replace with rpi3.local
topic_ti = "house/wetterstation/temp"  # inside temp topic
# topic_to =
topic_flame = "house/wetterstation/luftfeuchtigkeit"  # burner % topic
topics = [(topic_ti, 0), (topic_flame, 0), ]  # junkers topics goes here


# define mqtt on_connect callback
def on_connect(client, userdata, flags, rc):
    print("Connected to broker")
    client.connected_flag = True
    client.subscribe(topics)


# define mqtt on_message callback
def on_message(client, userdata, message):
    value = (message.payload.decode("utf-8"))
    if message.topic == topic_flame:
        flame_v.text = value + '%'
    elif message.topic == topic_ti:
        ti_v.text = value + 'C'
    else:
        print("invalid topic")
    c.update_screens([scr])

# TODO define on_disconnect callback


# create mqtt client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connected_flag = False
client.message = 'Waiting for value'
client.connect(broker)
client.loop_start()

# TODO define disconnect


# wait for connection with broker
while not client.connected_flag:
    print("Connecting to broker")
    time.sleep(.1)

# main loop
try:
    while True:
        time.sleep(.1)
except lcdexcept.RequestError as e:
    print('LCDd refused our request', e)
except lcdexcept.FatalError as e:
    print('pylcddc fatal internal error', e)
except KeyboardInterrupt:
    print('exitting')
# TODO add mqtt except
