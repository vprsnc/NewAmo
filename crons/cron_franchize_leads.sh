#!/bin/sh

mydate=`date`
cd $HOME/NewAmo
$HOME/NewAmo/venv/bin/python $HOME/NewAmo/etl_franchize_leads.py
if [ $? -eq 0 ]; then
    echo "franchize leads cron successful on $mydate" >> $HOME/newAmo.log; else
    echo "franchize leads cron failed on $mydate" >> $HOME/newAmo.log;
fi
