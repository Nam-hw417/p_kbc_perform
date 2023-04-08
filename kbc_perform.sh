#!/bin/bash

ps gx | grep "kbc_perform.py" | grep -v grep | awk '{cmd=sprintf("kill %s",$1); system(cmd); system("sleep 5");}'

nohup streamlit run --server.port 18887 --server.fileWatcherType none kbc_perform.py > ../Log/PromisingItems.log &
echo "App Start ::: KBC Perform"
