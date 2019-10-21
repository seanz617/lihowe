//加载模块
var Application = require('spectron').Application;
var assert = require('assert');
var electronPath = require("electron");
const chai = require('chai');
const chaiAsPromised = require('chai-as-promised');

chai.should();
chai.use(chaiAsPromised);

describe('application launch', function () {

    //设置所有用例执行完成的超时时间
    this.timeout(600000);

    //执行所有用例前的HOOK
    before(function () {
        this.app = new Application({
            path: 'D:\\Program Files\\enfi-cloud-desktop\\ENFI下载器.exe',
            waitTimeout: 30000
        });
        return this.app.start()
    });

    //所有用例执行完的HOOK
    after(function () {
        if (this.app && this.app.isRunning()) {
            console.log("finished");
            return this.app.stop()
        }
    });

    //每个用例执行前的HOOK
    beforeEach(function () {
    });

    //每个用例执行后的HOOK
    afterEach(function () {
    });

    //等待函数
    async function sleep(ms = 0) {
        return new Promise(r => setTimeout(r, ms));
    }

    //根据ENFI窗口TITLE查找窗口INDEX
    async function find_win_index_by_name(client,title) {
        var count = await client.getWindowCount().then(function(c){
            return c
        });

        var index = -1;

        for (var i = 0;i<count;i++){
            var win_title = await client.windowByIndex(i).getTitle().then(function(t){
                return t;
            });

            if(win_title == title){
                index = i;
                break;
            }
        }

        return index
    }

    //切换focus到指定title的ENFI窗口
    async function switch_to_window(client, title) {
        var index = await find_win_index_by_name(client,title);
        if(index < 0){
            console.log("error:can't find window with title["+title+"]");
        } else {
            console.log("switch to window ["+title+"]");
            await client.windowByIndex(index);
        }
        return index;
    }

    //启动ENFI
    it('shows initial enfi window', async function () {
        //等待ENFI启动
        await sleep(10000);

        await console.log("testing...");

        await this.app.client.waitUntilWindowLoaded();

        //输出ENFI窗口状态
        await this.app.webContents.isLoading().then(function (loading) {
            console.log('window is loading? ' + loading)
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

        /*
        //保存HTML文件
        await this.app.webContents.savePage('page4.html', 'HTMLComplete')
            .then(function () {
                console.log('page saved')
            }).catch(function (error) {
                console.error('saving page failed', error.message)
        });
        */

        /*
        //执行javascript脚本
        await this.app.client.windowByIndex(1).execute(() => {
            var t = document.getElementsByTagName("textarea");
            var tt = 'magnet:?xt=urn:btih:3a508bb3e5e7b4ba72adc85d3bb4c9cbc19152f0&dn=%E6%98%86%E6%B1%A0%E5%B2%A9.GONJIAM.Haunted.Asylum.2017.1080p.FHDRip.H264.AAC.CHS-BTBT4K';
            t[0].innerHTML = tt
        });
        */

        //获取当前ENFI窗口数量
        await this.app.client.getWindowCount().then(function (count) {
            console.log(count);
            assert.equal(count, 6)
        });

        await sleep(3000);
    });

    it('close notification', async function () {
        //切换到ENFI cloud desktop notification串口
        var notification = await switch_to_window(this.app.client,"ENFI cloud desktop notification");
        if(notification >= 0){
            //关闭窗口
            await this.app.client.click('//*[@id="app"]/div[3]/button[2]').then(function(){
                console.log('click confirm notification')
            });
        }
        await sleep(3000);
    });

    it('start offline download', async function () {
        //切换到ENFI-cloud窗口
        await switch_to_window(this.app.client,'ENFI-cloud');

        //进入离线下载列表页面
        await this.app.client.click('/html/body/div[1]/div/div/div[2]/div/div[1]/div[1]/div[1]/div/div/div/div/div[3]').then(function(){
            console.log("click 离线空间");
        });

        //刷新离线下载列表
        await this.app.client.click('/html/body/div[1]/div/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/div/div[1]/span[4]/span').then(function(){
            console.log('click 刷新')
        });

        //检查离线完成
        await this.app.client.waitUntilTextExists('html', '离线完成',3000);

        //下载离线完成的文件
        await this.app.client.click('/html/body/div[1]/div/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div/div[1]/div[2]/button[1]').then(function(){
            console.log('click 提取')
        });

        await sleep(3000);

        await this.app.client.click('//*[@id="offline-download-modal-container"]/div[2]/button/span').then(function(){
            console.log('click 确认提取')
        });

        await sleep(3000);
    });

    it('wait offline download finish', async function () {
        //切换到ENFI-cloud窗口
        await switch_to_window(this.app.client,'ENFI-cloud');

        //进入正在下载列表页面
        await this.app.client.click('span*=正在下载').then(function(){
            console.log('click 正在下载')
        });

        await sleep(3000);

        //获取下载进度
        await this.app.client.getText('/html/body/div[1]/div/div/div[2]/div/div[1]/div[1]/div[2]/div[1]/div/div[2]/div/div/ul/li/div/div[1]/div[3]/span[2]').then(function(value){
            console.log("progress: "+value)
        });

        //暂停下载任务
        await this.app.client.click('/html/body/div[1]/div/div/div[2]/div/div[1]/div[1]/div[2]/div[1]/div/div[2]/div/div/ul/li/div/div[2]/button[1]').then(function(){
            console.log('click pause');
        });

        await sleep(3000);

        //修复下载任务
        await this.app.client.click('/html/body/div[1]/div/div/div[2]/div/div[1]/div[1]/div[2]/div[1]/div/div[2]/div/div/ul/li/div/div[2]/button[1]').then(function(){
            console.log('click resume');
        });

        await sleep(3000);

        //获取下载进度
        await this.app.client.getText('/html/body/div[1]/div/div/div[2]/div/div[1]/div[1]/div[2]/div[1]/div/div[2]/div/div/ul/li/div/div[1]/div[3]/span[2]').then(function(value){
            console.log("progress: "+value)
        });

        await sleep(3000);

        //删除下载任务
        await this.app.client.click('/html/body/div[1]/div/div/div[2]/div/div[1]/div[1]/div[2]/div[1]/div/div[2]/div/div/ul/li/div/div[2]/button[2]').then(function(){
            console.log('click delete');
        });

        await sleep(3000);

        await this.app.client.click('/html/body/div[4]/div[2]/div/div/div[2]/div/div[2]/button/span').then(function(){
            console.log('click confirm delete');
        });

        await sleep(3000);
    });

    it('screen shot', async function () {
        await this.app.client.saveScreenshot('screenshot.png');
        await sleep(3000);
    })

});

// UI测试触发条件：定时任务
// 启动测试命令：mocha demo --reporter mochawesome --reporter-options reportFilename=r.html,overwrite=true
// 测试输出：日志（PCDN,ENFI），截图，HTML测试报告