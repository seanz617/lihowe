## ENFI UI自动化DEMO

## 1. 需求
-  主要目的是PCDN发版前通过ENFI测试PCDN
-  ENFI BASIC用例自动化
-  PCDN-ENFI兼容性测试

## 2. 设计
- 测试输出:
   - HTML测试报告
   - 【PCDN，ENFI，测试脚本】日志
   - 每个测试用例【完成，失败】后的截图(PNG)
- 测试框架: mocha
- 测试驱动: spectron封装[chromedriver,webdriverIO,electron]
   - [spectron文档](https://github.com/electron-userland/spectron)
   - [webio文档](https://webdriver.io/) 和 [webio文档](https://webdriver.io/docs/selectors.html)
- 测试报告: mochawesome
- 编程语言: javascript
- 编码IDE: vscode or webstorm

## 3. 环境搭建
- 下载安装nodejs，下载地址:https://nodejs.org/en/download/
   - npm -v
   - node -v
- 全局安装electron: ENFI用electron版本为3.0.13
   - npm -g install electron@3.0.13
   - npm ls electron
- 全局安装spectron: spectron版本必须和electron对应
   - npm -g install --save-dev spectron@5.0.0
   - npm ls spectron
- 全局安装mocha:
   - npm -g install mocha
   - npm ls mocha
- 全局安装mocha:
   - npm -g install mochawesome
   - npm ls mochawesome
- 全局安装chai:
   - pm -g install chai
   - npm ls chai
- 全局安装chai-as-promised:
   - npm -g install chai-as-promised
   - npm ls chai-as-promised
- 全局安装assert:
   - npm -g install assert
   - npm ls assert

## 4. ENFI UI自动化用例流程
- WGET下载PCDN，更新ENFI中的PCDN
- BT下载
  - 创建BT下载任务
  - 等待下载进度大于1%后，暂停，恢复下载任务
  - 每隔20秒检查一次下载任务的状态和速度
    - 下载速度长时间为零，则用力失败
    - 下载任务状态不在运行中，则用力失败
- HTTP下载
  - 创建离线下载任务
  - 等待下载进度大于1%后，暂停，恢复下载任务
  - 每隔20秒检查一次下载任务的状态和速度
    - 下载速度长时间为零，则用力失败
    - 下载任务状态不在运行中，则用力失败
- 手机日志，生成报告

## 5. ENFI UI自动化初步实践经验
- nodejs编程特性：单线程，异步IO，事件循环，编码时要考虑代码执行顺序
- 尽量使用spectron操作元素，javascript或selenium操作元素坑比较多
- ENFI页面上不是单一的程序窗口，定位元素时需要在各个窗口间切换
- ENFI页面上相同TEXT的控件较多，定位元素不要用TEXT定位
- [DEMO源码](https://github.com/PPIO/ppio-tests/blob/master/docs/enfi_automation_demo/demo.js)
- 启动测试命令：mocha demo --reporter mochawesome --reporter-options reportFilename=r.html,overwrite=true
