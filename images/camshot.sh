#!/bin/sh

adb -s HT23DV802031 shell input keyevent 26
adb -s HT23DV802031 shell input swipe 200 900 200 300
adb -s HT23DV802031 shell input tap 450 900
sleep 5
adb -s HT23DV802031 shell input tap 250 800 
sleep 5
adb -s HT23DV802031 shell input keyevent KEYCODE_BACK
adb -s HT23DV802031 shell input keyevent 26
image=`adb -s HT23DV802031 shell 'ls /sdcard/DCIM/Camera | tail -n 1'`
image=`echo $image | tr -d "\r"`
path=/sdcard/DCIM/Camera/
adb -s HT23DV802031 pull /sdcard/DCIM/Camera/
adb -s HT23DV802031 shell rm $path/*
mv $image outside.jpeg
datetime=`date`
hour=`date +"%H"`
minute=`date +"%M"`
day=`date +"%d"`
month=`date +"%m"`
if [ $hour -eq 12 ]
then   
            cp outside.jpeg "/diablo/timelapse/$month-$day-$hour-$minute.jpeg"
fi
temperature=`ssh raspberrypi python tempnow.py`
convert outside.jpeg -resize 640x480 -pointsize 28 -fill white -undercolor '#00000080' -gravity SouthEast -annotate +0+5 "$datetime $temperature°C" outside-timestamp.jpg
scp outside-timestamp.jpg andromeda:/var/www/

