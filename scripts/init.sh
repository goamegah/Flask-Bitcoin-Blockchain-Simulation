#!/bin/bash
#the script must be executed in the scripts folder
sudo apt update
sudo apt install build-essential #install C compiler

#installation of specific version of python
wget https://www.python.org/ftp/python/3.10.7/Python-3.10.7.tgz
tar -xf Python-3.10.7.tgz Python-3.10.7
mv Python-3.10.7 ../
rm Python-3.10.7.tgz
cd ../Python-3.10.7
./configure
make
cd ../scripts

poetry_install=$(curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3 -)

if [ $? -eq 0 ]
        then
          echo "Successfully installed poetry"
          echo "Load python packages for the app"
          cd ../
          /etc/poetry/bin/poetry env use ./Python-3.10.7/python
          /etc/poetry/bin/poetry install
fi
