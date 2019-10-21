#!/bin/bash

#install netp
yum -y install ntp ntpdate
#sync net time (a li time server)
ntpdate -d 182.92.12.11
#write hardware time
hwclock --systohc
#write CMOS
hwclock -w
