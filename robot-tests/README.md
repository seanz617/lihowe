## robot 测试框架

## 1. 需求
- 自动化测试用例稳定，完整，易于维护

## 2. 设计
|层级结构|
|--|
|环境变量和配置文件 JSON|
|robot framework|
|测试用例和测试数据 ROBOT|
|参数转换，操作计时，断言，业务功能封装 PYTHON|
|RPC调用 PYTHON|

## 3. 准备环境
1. 安装PYTHON 3
```bash
apt-get install software-properties-common
add-apt-repository ppa:jonathonf/python-3.6
apt-get update
apt-get install python3.6
```

2. 安装PIP
```bash
apt-get install python3-pip
cd /usr/bin
ln -s python3.6m python
ln -s pip3 pip
python -V
pip -V
```

3. 安装robot framework以及依赖包
```bash
pip install robotframework
pip install robotframework-archivelibrary
pip install robotframework-sshlibrary
pip install robotframework-requests
pip install pymysql
pip install kubernetes #可选
pip install SlackClient #可选
python3 -m pip install -U discord.py
robot --version
```

4. 设置环境变量
```bash
export TEST_CONFIG=$curr_dir/config/test_config.json #配置文件路径
export TEST_ENV=R #大环境R多机环境，S单机环境
```

## 4. 配置
1. 配置文件中已经将所有配置扁平化，R环境和S环境的配置不会相互影响，例如：
```bash
mysql : {
    R: {
        IP:192.168.50.231,
        PORT:3306,
    },
    S: {
        IP:127.0.0.1,
        PORT:3306,
    }
}
```
2. 配置文件在test_config这个类被加载时加载
3. test_config类中定义了一个get_config函数，可以根据环境自动获取相应的配置，例如
```bash
TEST_ENV = R
SUB_ENV = A
conf = test_config.get_config("mysql")
#conf 为R环境的mysql配置
```

## 5. 测试用例和测试数据
1. 测试用例和测试数据分离，例如：
```bash
测试用例
*** Settings   ***
Library    controller.test_poss
Variables    data-center/data.py #测试数据文件
*** Test Cases ***
Test poss put get delete
  [Template]    Test poss put get delete ${param}
  ${POSS_PUT_GET_DELETE_1K}  #测试数据引用
  ${POSS_PUT_GET_DELETE_16LESSM}  #测试数据引用
  ${POSS_PUT_GET_DELETE_16LARGERM}  #测试数据引用
  ${POSS_PUT_GET_DELETE_32M_2COPIES}  #测试数据引用
*** Key Words ***
Test poss put get delete ${param}
  put object    ${param}[put]
  get object    ${param}[get]
  delete object    ${param}[delete]
```
```bash
测试数据
#---------- put get delete -----------
tmp = gen_name("1K")
POSS_PUT_GET_DELETE_1K = {
        "put" : {"key":tmp, "body": "1K"},
        "get" : {"key":tmp, "outfile":tmp},
        "delete" : {"key":tmp}
        }
```

## 6. 参数转换，操作计时，断言，业务功能封装
1. 参数转换  
  - 所有人为指定的ROBOT关键字参数以PYTHON DICT的形式给定，例如: chiprice copies expires...
  - 所有人为无法指定，在运行时确定的参数以字符串的形式在关键字之间传递，例如:sharecode, taskid, chunk hash...

2. 操作计时
  - 所有业务函数都被WRAP到以下代码快中：
  ```bash
  wrapper(time_limit)
      start_time = int(time.time())
      status, ret = function call
      used_time = int(time.time()) - start_time
      if used_time > time_limit:
          status = False
          print("operation timeout")
      return status, ret
  ```

3. 断言
  - 关键字参数中可以指定result（True or False）字段，表明此次操作结果是成功还是失败，例如
  ```bash
  def keyword(param):
      expect = param.get("result",True)
      status,ret = something
      assert expect == status
  ```

4. 业务功能封装
```bash
def put_object(params):
    根据CHUNKS和COPIES计算time_limit
    if no bucket:
        create bucket
    status,ret = put object rpc call(time_limit)
    assert expect == status
    if 同步
        等待 object status 变为deal
    else 异步
        直接返回
```
