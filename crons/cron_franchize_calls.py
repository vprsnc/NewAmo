#!/bin/sh

mydate=`date`
cd $HOME/NewAmo
$HOME/NewAmo/venv/bin/python $HOME/NewAmo/etl_franchize_calls.py
if [ $? -eq 0 ]; then
    echo "franchize calls cron successful on $mydate" >> $HOME/newAmo.log; else
    echo "franchize calls cron failed on $mydate" >> $HOME/newAmo.log;
fi
