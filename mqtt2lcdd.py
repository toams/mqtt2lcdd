#!/usr/bin/python3
import time
import pylcddc.client as client
import pylcddc.widgets as widget
import pylcddc.screen as screen
import pylcddc.exceptions as lcdexcept
import paho.mqtt.subscribe as subscribe
import schedule


# initialise lcd
lcd_host = 'localhost'
lcd_port = '13666'
# compose screen layout
# ##################
# #13:24  Ti=-**.*C#
# #>***%  To=-**.*C#
# ##################

clock = widget.String('clock', 1, 1, 'HH:MM')
ti = widget.String('ti', 8, 1, 'Ti=')
ti_v = widget.String('ti_v', 11, 1, '**.*C')
to = widget.String('to', 8, 2, 'Tb=')
to_v = widget.String('to_v', 11, 2, '**.*C')
flame = widget.Icon('flame', 1, 2, widget.Icon.IconType.FF)
flame_v = widget.String('flame_v', 2, 2, '***%')

scr = screen.Screen('Temperature',
                    (clock, ti, ti_v, to, to_v, flame, flame_v),
                    heartbeat=screen.ScreenAttributeValues.Heartbeat.OFF)
c = client.Client(lcd_host, lcd_port)
c.add_screen(scr)


# initialise mqtt
broker = "rpi3.local"  # broker address
topic_ti = "rpi3/hometop/ht/hc1_Tmeasured"  # inside temp topic
topic_to = "rpi3/hometop/ht/ch_Toutside"
topic_flame = "rpi3/hometop/ht/ch_burner_power"  # burner % topic
topics = [(topic_ti, 0), (topic_flame, 0), (topic_to,0)]
value = ['', '', '']  # values received from broker will be stored here


def update_screen():
    for i in range(len(topics)):
        msg = subscribe.simple(topics[i], hostname=broker)
        value[i] = (msg.payload.decode("utf-8"))
    ti_v.text = f'{value[0]:>5}C'
    flame_v.text = f'{value[1]:>3}%'
    to_v.text = f'{value[2]:>5}C'
    clock.text = time.strftime("%H:%M", time.localtime())
    c.update_screens([scr])


update_screen()
schedule.every().minute.at(":00").do(update_screen)
# main loop
try:
    while True:
        schedule.run_pending()
        time.sleep(1)

except lcdexcept.RequestError as e:
    print('LCDd refused our request', e)
except lcdexcept.FatalError as e:
    print('pylcddc fatal internal error', e)
except KeyboardInterrupt:
    print('exiting')
# TODO add mqtt except
