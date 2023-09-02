#!/bin/bash
#the script must be executed in the scripts folder -- run in sudo mode
chmod +x ./init.sh
./init.sh

if [ $? -eq 0 ]
        then
          /etc/poetry/bin/poetry run python ../app.py
fi
