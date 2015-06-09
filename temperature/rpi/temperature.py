import os
import time
import collections

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

temp_sensor = '/sys/bus/w1/devices/28-0000050577cc/w1_slave'

temps = collections.deque(maxlen=96)

jsfile = 'temps.js'

def temp_raw():
    f = open(temp_sensor, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = temp_raw()
    temp_output = lines[1].find('t=')
    if temp_output != -1:
        temp_string = lines[1].strip()[temp_output+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

def createjs():
    x_axis = []
    y_axis = []

    for reading in temps:
        x_axis.append(reading[0])
        y_axis.append(reading[1])

    f = open(jsfile ,'w')

    f.write("""$(function () {
            $('#container').highcharts({
                    title: {
                                    text: 'Temperature at Window Sill',
                                                x: -20 //center
                                                        },
            xAxis: {
                categories: [""")
    for timestamp in x_axis[:-1]:
        f.write("'"+ timestamp + "',")
    f.write("'" +  x_axis[-1] + "']")
    f.write("""},
        yAxis: {
            title: {
                text: 'Temperature'
            },
            min: 0,
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
                }]
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
        series: [{
            name: 'Temperature',
            data: [""")
    for reading in y_axis[:-1]:
	f.write(str(reading) + ",")
    f.write(str(y_axis[-1]) + "]")
    f.write("""}]
    });
});""")
    f.close()



while True:
    this_temp = [time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()), read_temp()]
    temps.append(this_temp)
    createjs()
    os.system('scp -q /home/pi/' + jsfile + ' jamies@diablo:/var/www/html/temps/')
    time.sleep(900)
