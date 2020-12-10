#!/bin/sh
while true
do 
	inotifywait run.py
	clear
	./run.py </dev/null
done
