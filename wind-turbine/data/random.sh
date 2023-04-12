#!/bin/bash

while true; do

sleep 5; echo 100 > spinny_speed.avi;
sleep 2; echo 0 > spinny_speed.avi;
sleep 5; echo -100 > spinny_speed.avi;
sleep 2; echo 0 > spinny_speed.avi;


done
