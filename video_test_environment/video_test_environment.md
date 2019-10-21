## 视频测试环境

## 1. 需求
- flv 点播，直播
- hls 点播，直播
- mp4 点播
- dash 暂时不需要

## 2. 设计
|推流|视频服务器|拉流/播放|
|--|--|--|
|OBS|nginx|browser|
|ffmpeg|nginx-http_flv_module|vlc|
||nginx_mod_h264_streaming|flv.js|

## 3. 推流
1. 安装ffmpeg
```bash
yum install -y epel-release
rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-7
yum repolist
rpm --import http://li.nux.ro/download/nux/RPM-GPG-KEY-nux.ro
rpm -Uvh http://li.nux.ro/download/nux/dextop/el7/x86_64/nux-dextop-release-0-1.el7.nux.noarch.rpm
yum repolist
yum update -y
yum install -y ffmpeg
ffmpeg -version
```
2. 使用ffmpeg推流
```bash
基本命令
ffmpeg -re -y -i test.mp4 -c:v copy -c:a copy -flags +loop -f flv "rtmp://服务器IP:rmtp服务端口/rmtp app名称/流秘钥（任意字符）"
推送hls直播流
ffmpeg -re -y -i test.mp4 -c:v copy -c:a copy -flags +loop -f flv "rtmp://192.168.50.208:1935/hlslive/myhlsstream"
推送flv直播流
ffmpeg -re -y -i test.mp4 -c:v copy -c:a copy -flags +loop -f flv "rtmp://192.168.50.208:1935/flvlive/myflvstream"
```

3. OBS推流
  - 进入 OBS->设置->流
  - 服务器：rtmp://服务器IP:rmtp服务端口/rmtp app名称/
  - 流密钥：任意(字符串)

## 4. 视频服务器
1. 安装ZLIB
```bash
wget http://www.zlib.net/zlib-1.2.11.tar.gz
tar xf zlib-1.2.11.tar.gz
cd zlib-1.2.11
./configure
make && make install
```
2. 安装openssl
```bash
wget https://www.openssl.org/source/openssl-1.0.2l.tar.gz
tar xf openssl-1.0.2l.tar.gz
cd openssl-1.0.2l
./config
make && make install
```
3. 安装pcre
```bash
wget ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-8.38.tar.bz2
tar xf pcre-8.38.tar.bz2
cd pcre-8.38
./configure
make && make install
```
4. 安装nginx插件
```bash
git clone https://github.com/arut/nginx-rtmp-module.git  
git clone https://github.com/winshining/nginx-http-flv-module.git
wget http://h264.code-shop.com/download/nginx_mod_h264_streaming-2.2.7.tar.gz
tar -zxvf nginx_mod_h264_streaming-2.2.7.tar.gz
wget -O ngx_cache_purge.zip https://github.com/FRiCKLE/ngx_cache_purge/archive/master.zip
unzip ngx_cache_purge.zip
```
5. 安装nginx
```bash
wget http://nginx.org/download/nginx-1.12.2.tar.gz
tar -zxvf nginx-1.12.2.tar.gz
cd nginx-1.12.2
 ./configure --prefix=/usr/local/nginx --add-module=../ngx_cache_purge-master --add-module=../nginx_mod_h264_streaming-2.2.7 --with-http_ssl_module  --with-http_stub_status_module --with-pcre=../pcre-8.38 --with-openssl=../openssl-1.0.2l --with-zlib=../zlib-1.2.11 --with-http_flv_module --with-http_gzip_static_module --with-http_sub_module --with-http_stub_status_module --add-module=../nginx-http-flv-module
 make && make install
```
6. 配置nginx
```bash
修改nginx配置文件
cd /usr/loca/nginx/conf
vi nginx.conf
rtmp app的相关配置（推流时使用）
http 服务server的配置，主要是URL路由配置和HLS FLV直播配置
```
[具体nginx.conf内容](https://github.com/PPIO/ppio-tests/blob/master/docs/video_test_environment/nginx.conf)
```bash
创建目录结构
cd /usr/loca/nginx/html
mkdir hls #存hls点播用的TS和M3U8文件
mkdir flv #存点播FLV文件
mkdir mp4 #存点播MP4文件
mkdir video  #存储原视频用
mkdir hlslive #BUFFER直播TS和M3U8临时文件
mkdir flvlive #BUFFER直播FLV临时文件
```

7. 启动nginx
```bash
启动nginx
cd /usr/local/nginx
sbin/nginx
停止nginx
sbin/nginx -s stop
更新配置
sbin/nginx -s reload
```

## 5. 准备视频点播数据
1. 从网上下载一个MP4文件
2. 将MP4文件切片成TS和M3U8格式的文件
```bash
cp test.mp4 /usr/local/nginx/html/mp4/
cd /usr/local/nginx/html/hls
ffmpeg -i ../mp4/test.mp4 -c:v libx264 -c:a aac -strict -2 -f hls -hls_time 10 -hls_list_size 0 ./test.m3u8
```
3. 将mp4文件转码为flv文件
```bash
cd /usr/local/nginx/html/flv
ffmpeg -i ../mp4/test.mp4 -c:v libx264 -crf 24 ./test.flv
```

## 6. 拉流
|/|hls|flv|mp4|
|--|--|--|--|
|点播|http://192.168.50.208/hls/test.m3u8|http://192.168.50.208/test.flv|http://192.168.50.208/test.mp4|
|http直播|http://192.168.50.208/hlslive/myhlslivestream.m3u8|http://192.168.50.208/flvlive?port=1935&app=flvlive&stream=myflvstream|--|
|rtmp直播|rtmp://192.168.50.208:1935/hlslive/myhlsstream|rtmp://192.168.50.208:1935/flvlive/myflvstream|--|


<font color='red'>注：如果要拉直播流，请将下方myhlslivestream和或myflvlivestream换成推流时设置的（【OBS流秘钥】
或【ffmpeg推流时设置的字符串】）</font>

## 7. 播放
1. 浏览器播放FLV
```bash
yum install -y nodejs
git clone https://github.com/bilibili/flv.js.git
cd flv.js
npm install
npm install -g gulp
gulp release
cp dist/flv.min.js /usr/local/nginx/html/
cd /usr/local/nginx/html
vi index.html
```
[具体index.html内容](https://github.com/PPIO/ppio-tests/blob/master/docs/video_test_environment/index.html)

2. 浏览器播放HLS  
chrome 需要安装native NLS playback插件

## 8. 参考：
