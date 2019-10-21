#!/bin/bash

echo 'clear datas in ppio.tables'
mysql -uroot -p123456 -Dppio ./ppio.sql
