var enfi_cloud = require('./enfi_cloud');
const chai = require('chai');
const chaiAsPromised = require('chai-as-promised');

describe('ENFI Compatibility Test', function () {
    this.timeout(3600000);

    before(async function () {
        await enfi_cloud.update_pcdn('https://pcdn-release.oss-cn-shanghai.aliyuncs.com/cmd_pcdn_windows_v0.5.19.exe');
        return await enfi_cloud.run();
    });

    after(async function () {
        //await enfi_cloud.snap_shot("end.png");
        return await enfi_cloud.quit();
    });

    beforeEach(async function(){
        await console.log("---------- "+this.currentTest.title+" begin ----------")
    });

    afterEach(async function () {
        //await enfi_cloud.snap_shot(this.currentTest.title+".png");
        await console.log("---------- "+this.currentTest.title+" end ----------")
    });

    it('setup_main_window', async function(){
        await enfi_cloud.setup_main_window();
        return await enfi_cloud.close_notification();
    });

    it('test_bt_download', async function(){
        return await enfi_cloud.bt_download();
    });

    it('test_offline_download', async function () {
        return await enfi_cloud.offline_download();
    });
});