#!/bin/sh

mydate=`date`
cd $HOME/NewAmo
$HOME/NewAmo/venv/bin/python $HOME/NewAmo/franchize_status_changes_etl.py
if [ $? -eq 0 ]; then
    echo "leads cron successful on $mydate" >> $HOME/newAmo.log; else
    echo "leads cron faield on $mydate" >> $HOME/newAmo.log;
fi
