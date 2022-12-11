#!/bin/sh

mydate=`date`
cd $HOME/NewAmo
$HOME/NewAmo/venv/bin/python $HOME/NewAmo/etl_franchize_lead_status_changes.py
if [ $? -eq 0 ]; then
    echo "franchize leads status changes cron successful on $mydate" >> $HOME/newAmo.log; else
    echo "franchize leads status changes cron failed on $mydate" >> $HOME/newAmo.log;
fi
