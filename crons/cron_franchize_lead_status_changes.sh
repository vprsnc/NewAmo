#!/bin/sh

mydate=`date`
cd $HOME/NewAmo
$HOME/NewAmo/venv/bin/python $HOME/NewAmo/etl_franchize_lead_status_changes.py
if [ $? -eq 0 ]; then
    echo "leads status changes cron successful on $mydate" >> $HOME/newAmo.log; else
    echo "leads status change scron failed on $mydate" >> $HOME/newAmo.log;
fi
