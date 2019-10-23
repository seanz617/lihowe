var electronPath = require("electron");
var Application = require('spectron').Application;
var execSync = require('child_process').execSync;
var assert = require('assert');
const chai = require('chai');
const chaiAsPromised = require('chai-as-promised');

chai.should();
chai.use(chaiAsPromised);

var exepath = 'D:\\enfi-cloud-desktop\\ENFI下载器.exe';

var enfi_cloud = {

    sleep: async function (ms = 0) {
        return new Promise(r => setTimeout(r, ms));
    },

    find_win_index_by_name: async function (title) {
        var count = await this.app.client.getWindowCount().then(function(c){
            return c
        });

        var index = -1;

        for (var i = 0;i<count;i++){
            var win_title = await this.app.client.windowByIndex(i).getTitle().then(function(t){
                return t;
            });

            if(win_title == title){
                index = i;
                break;
            }
        }
        return index
    },

    switch_to_window: async function (title) {
        var index = await this.find_win_index_by_name(title);
        if(index < 0){
            console.log("error:can't find window with title["+title+"]");
        } else {
            console.log("switch to window ["+title+"]");
            await this.app.client.windowByIndex(index);
        }
        await this.sleep(3000);
        return index;
    },

    snap_shot: async function(file_name) {
        await this.app.client.saveScreenshot(file_name);
        await this.sleep(1000);
    },

    update_pcdn: async function(url) {
        //execSync('del \'D:\\Program Files\\enfi-cloud-desktop\\resources\\extraResources\\pcdn_win.exe\'' +
        execSync('del D:\\enfi-cloud-desktop\\resources\\extraResources\\pcdn_win.exe' +
            function (error, stdout, stderr) {
                if (error !== null) {
                    console.log('exec error: ' + error+stdout+stderr);
                }
            });
        //  && copy pcdn_win.exe ',
        //execSync('wget '+url+'-O \'D:\\Program Files\\enfi-cloud-desktop\\resources\\extraResources\\pcdn_win.exe\'',
        execSync('wget '+url+' -O D:\\enfi-cloud-desktop\\resources\\extraResources\\pcdn_win.exe',
            function (error, stdout, stderr) {
                if (error !== null) {
                    console.log('exec error: ' + error);
                }
            });
    },

    run: function() {
        this.app = new Application({
            path:exepath,
            waitTimeout:30000
        });
        return this.app.start()
    },

    quit: function() {
        if (this.app && this.app.isRunning()) {
            return this.app.stop()
        }
    },

    check_download_speed: async function(timeout) {
        var speed_zero_count = 0;
        var pause_flag = false;
        var total_time = parseInt(timeout / 20000);
        for (i = 0; i < total_time; i++) {
            await this.sleep(6000);

            var progress = 0.0;
            progress = await this.app.client.getText('/html/body/div[1]/div/div/div[2]/div/div[1]/div[1]/div[2]/div[1]/div/div[2]/div/div/ul/li/div/div[1]/div[3]/span[2]').then(function(value){
                console.log('progress:'+value);
                var jindu = parseFloat(value);
                if(isNaN(jindu)){
                    jindu = 0.0;
                }
                return jindu;
            });

            console.log('progress:'+progress)

            if(progress > 1 && pause_flag == false){
                pause_flag = true;

                await this.sleep(3000);

                await this.app.client.click('/html/body/div[1]/div/div/div[2]/div/div[1]/div[1]/div[2]/div[1]/div/div[2]/div/div/ul/li/div/div[2]/button[1]').then(function(){
                    console.log('click pause');
                });

                await this.sleep(3000);

                await this.app.client.click('/html/body/div[1]/div/div/div[2]/div/div[1]/div[1]/div[2]/div[1]/div/div[2]/div/div/ul/li/div/div[2]/button[1]').then(function(){
                    console.log('click resume');
                });
            }

            await this.sleep(10000);

            var exist_flag = await this.app.client.isExisting('/html/body/div[1]/div/div/div[2]/div/div[1]/div[1]/div[2]/div[1]/div/div[2]/div/div/ul/li[1]/div/div[1]/div[1]/div/span');
            if(exist_flag){
                var text_ret = await this.app.client.getText('/html/body/div[1]/div/div/div[2]/div/div[1]/div[1]/div[2]/div[1]/div/div[2]/div/div/ul/li[1]/div/div[1]/div[1]/div/span').then(function (text) {
                    console.log(text);
                    if(text == '正在开始 ...' || text == '下载失败' || text=='已暂停'){
                        console.log('download fail');
                        return false;
                    }
                    var speed0 = parseFloat(text[0]);
                    var speed1 = parseFloat(text[1]);
                    if (isNaN(speed1)) {
                        speed1 = 0.0
                    }
                    console.log(speed0);
                    console.log(speed1);
                    total_speed = speed0 + speed1;
                    console.log('total speed '+total_speed)
                    if (total_speed <= 0.1) {
                        speed_zero_count += 1;
                    }else{
                        speed_zero_count = 0;
                    }
                    return true;
                });
                if(!text_ret){
                    console.log("download fail");
                    return false;
                }
                if(speed_zero_count > 10){
                    console.log('download no speed');
                    return false;
                }
            }else{
                console.log('download finished')
                return true;
            }
        }
    },

    setup_main_window: async function() {
        await this.sleep(10000);
        await this.app.webContents.isLoading().then(function (loading) {
            console.log('window is loading? ' + loading)
        });
        await this.app.client.waitUntilWindowLoaded(30000).then(function (){
            console.log('window loaded')
        });
        await this.app.browserWindow.isVisible().then(function (visible) {
            console.log('window is visible? ' + visible)
        });
        await this.app.browserWindow.isFocused() .then(function (focused) {
            console.log('window is focused? ' + focused)
        });
        await this.app.browserWindow.getTitle().then(function (title) {
            console.log('window title is ' + title)
        });
        //await this.app.client.getWindowCount().should.eventually.have.at.least(1);
    },

    close_notification: async function() {
        await this.sleep(3000);
        var notification = await this.switch_to_window("ENFI cloud desktop notification");
        if(notification >= 0){
            await this.app.client.click('//*[@id="app"]/div[3]/button[2]').then(function(){
                console.log('click confirm close notification')
            });
        }
        this.sleep(3000);
        console.log("===========")
    },

    offline_download: async function() {
        await this.switch_to_window('ENFI-cloud');

        await this.app.client.click('/html/body/div[1]/div/div/div[2]/div/div[1]/div[1]/div[1]/div/div/div/div/div[3]').then(function () {
            console.log("click 离线空间");
        });

        await this.app.client.click('/html/body/div[1]/div/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/div/div[1]/span[4]/span').then(function () {
            console.log('click 刷新')
        });

        await this.sleep(3000);

        var dead_text = await this.app.client.getText("/html/body/div[1]/div/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div/div/div[1]/div[1]/div/span").then(function (text) {
            return text;
        });

        if (dead_text == '已过期') {
            await this.app.client.click("/html/body/div[1]/div/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div/div/div[2]/button[1]")
            await this.sleep(3000);
            await this.app.client.click('/html/body/div[29]/div[2]/div/div/div/div/div[3]/button[2]');
            await this.sleep(3000);
        }

        await this.app.client.waitUntilTextExists('html', '离线完成', 300000).then(function () {
            console.log('离线完成')
        });

        await this.app.client.click('/html/body/div[1]/div/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div/div[1]/div[2]/button[1]').then(function () {
            console.log('click 提取')
        });

        await this.sleep(3000);

        await this.app.client.click('//*[@id="offline-download-modal-container"]/div[2]/button/span').then(function(){
            console.log('click 确认提取')
        });

        await this.sleep(3000);

        await this.app.client.click('span*=正在下载').then(function(){
            console.log('click 正在下载')
        });

        var ret = this.check_download_speed(1800000);
        if(!ret){
            await this.app.client.click('/html/body/div[1]/div/div/div[2]/div/div[1]/div[1]/div[2]/div[1]/div/div[2]/div/div/ul/li/div/div[2]/button[2]').then(function(){
                console.log('click delete');
            });
            await this.sleep(3000);

            await this.app.client.click('/html/body/div[4]/div[2]/div/div/div[2]/div/div[2]/button/span').then(function(){
                console.log('click confirm delete');
            });
            await this.sleep(3000);
        }

        await this.sleep(3000);

        await this.app.client.click('/html/body/div[1]/div/div/div[2]/div/div[1]/div[1]/div[2]/div[1]/div/div[2]/div/div/ul/li/div/div[2]/button[2]').then(function(){
            console.log('click delete');
        });

        await this.sleep(3000);

        await this.app.client.click('/html/body/div[4]/div[2]/div/div/div[2]/div/div[2]/button/span').then(function(){
            console.log('click confirm delete');
        });

        await this.sleep(3000);
    },

    bt_download: async function() {
        await this.switch_to_window('ENFI-cloud');

        await this.app.client.click('span*=正在下载').then(function(){
            console.log('click 正在下载')
        });

        await this.sleep(3000);

        await this.app.client.click('/html/body/div[1]/div/div/div[2]/div/div[1]/div[1]/div[2]/div[1]/div/div[1]/button[1]').then(function(){
            console.log('click 添加任务')
        });

        await this.sleep(3000);
        await this.switch_to_window('新建 ENFI 下载');
        await this.app.client.click('//*[@id="app"]/div/textarea');
        await this.sleep(30000);
        await this.app.client.setValue('//*[@id="app"]/div/textarea','magnet:?xt=urn:btih:DBF21FC9A28D7C292B5CD9462683A1E150D4E0E3&dn=John.Wick.3.2019.HDRip.XviD.AC3-EVO&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.internetwarriors.net%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.pirateparty.gr%3A6969%2Fannounce&tr=udp%3A%2F%2Fopen.demonii.si%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.iamhansen.xyz%3A2000%2Fannounce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80%2Fannounce&tr=udp%3A%2F%2F9.rarbg.to%3A2710%2Fannounce&tr=udp%3A%2F%2Fdenis.stalker.upeer.me%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=udp%3A%2F%2Fipv4.tracker.harry.lu%3A80%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Fexodus.desync.com%3A6969%2Fannounce&tr=udp%3A%2F%2Fexplodie.org%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.zer0day.to%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969%2Fannounce&tr=udp%3A%2F%2Fcoppersurfer.tk%3A6969%2Fannounce');
        await this.sleep(10000);
        await this.switch_to_window('ENFI-cloud');
        await this.app.client.click('button*=开始下载');
        await this.sleep(10000);
        await this.app.client.click('button*=极速下载');
        await this.sleep(10000);

        var ret = await this.check_download_speed(30000);

        if(!ret){
            await this.app.client.click('/html/body/div[1]/div/div/div[2]/div/div[1]/div[1]/div[2]/div[1]/div/div[2]/div/div/ul/li/div/div[2]/button[2]').then(function(){
                console.log('click delete');
            });
            await this.sleep(3000);

            await this.app.client.click('/html/body/div[4]/div[2]/div/div/div[2]/div/div[2]/button/span').then(function(){
                console.log('click confirm delete');
            });
            await this.sleep(3000);
        }
    },
};

module.exports = enfi_cloud;