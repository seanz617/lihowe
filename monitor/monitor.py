import os,sys,time,json,datetime,math
import requests
from urllib import parse
from flask import Flask
from flask import render_template
from flask import abort, redirect, url_for, request
from flask import make_response
from flask import send_file, send_from_directory
from flask_login import UserMixin
from flask_login import LoginManager
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from flask_login import current_user
from werkzeug.utils import secure_filename

from service_config import service_config
from models import DB
from models import User

conf = service_config("/home/ec2-user/tangsan/monitor/config.json")
users = conf.config["users"]
white_list = conf.config["white_list"]
db_handler = DB(conf.config["mysql"])
nodes = conf.config["resource"]

with open("/home/ec2-user/tangsan/monitor/state_default.json", "r") as json_file:
    miner_state_default = json.loads(json_file.read())

app = Flask(__name__)
app.debug = False 
app.secret_key = os.urandom(24)

BASE_DIR = '/home/ec2-user/tangsan/monitor/upload_logs'
FILE_TYPES = ['log',"tar","gz","jpg","conf"]

def query_user(user_id):
    for user in users:
        if user_id == user['id']:
            return user

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Access denied.'
login_manager.init_app(app)

def get_indexer_verifier_num(data):
    indexer_num = 0
    verifier_num = 0
    datas = data.split("!")
    for line in datas:
        ii = line.find("Indexers:")
        iv = line.find("Verifiers:")
        if ii >= 0:
            indexer_num = int(line.split(":")[1])
        if iv >= 0:
            verifier_num = int(line.split(":")[1])
    return indexer_num, verifier_num

def get_summary():
    config_nodes_num = json.dumps([[nodes["miners"]["node_num"], 0],
                                   [nodes["centers"]["node_num"], 1],
                                   [nodes["indexers"]["node_num"], 2],
                                   [nodes["verifiers"]["node_num"], 3],
                                   [nodes["bootstraps"]["node_num"], 4]])

    online_nodes_num = [[0, 0],
                        [0, 1],
                        [0, 2],
                        [0, 3],
                        [0, 4]]

    info = {
        "centers":[],
        "bootstraps":[],
        "verifiers":[],
        "indexers":[],
        "miners":[]
    }

    cmd = 'select name,data,time,version,crash from report;'
    query_result = db_handler.handle(cmd)
    now = datetime.datetime.now()
    if query_result and len(query_result) > 0:
        for value in query_result:
            status = "offline"
            report_time = value[2]
            delta = now - report_time
            if delta.total_seconds() < 300:
                status = "online" 
            
            data = None 
            try:
                data = json.loads(value[1]) 
            except Exception as err:
                data = value[1]

            tmp = {
                    "name":value[0],
                    "status":status,
                    "version":value[3],
                    "crash":int(value[4]),
                    "data":data if data else miner_state_default
            }

            if value[0].find("miner") >= 0:
                info["miners"].append(tmp)
                if status == "online":
                    online_nodes_num[0][0] = online_nodes_num[0][0] + 1
            elif value[0].find("center") >= 0:
                ci, cv = get_indexer_verifier_num(data)
                online_nodes_num[2][0] = ci
                online_nodes_num[3][0] = cv
                tmp["data"] = {"indexers": ci,"verifiers":cv}
                info["centers"].append(tmp) 
                if status == "online":
                    online_nodes_num[1][0] = online_nodes_num[1][0] + 1
            elif value[0].find("indexer") >= 0:
                indexer_miners = data.split(";")
                indexer_miners_info = dict({})
                if indexer_miners and len(indexer_miners) > 0:
                    for im in indexer_miners:
                        mi = im.split(":")
                        if mi and len(mi) == 3:
                            indexer_miners_info[mi[0]] = {
                                "total_space":int(mi[1]),
                                "left_space":int(mi[2])
                            }
                tmp["data"] = indexer_miners_info
                tmp["miner_count"] = len(indexer_miners_info.keys())
                info["indexers"].append(tmp)
            elif value[0].find("verifier") >= 0:
                info["verifiers"].append(tmp) 
            elif value[0].find("bootstrap") >= 0:
                bi, bv = get_indexer_verifier_num(data)
                if bi < online_nodes_num[2][0]:
                    online_nodes_num[2][0] = bi
                if bv < online_nodes_num[3][0]:
                    online_nodes_num[3][0] = bv
                tmp["data"] = {"indexers": bi,"verifiers":bv}
                info["bootstraps"].append(tmp) 
                if status == "online":
                    online_nodes_num[4][0] = online_nodes_num[4][0] + 1

    for m in info["miners"]:
        m["indexing"] = "unindexed"
        m["total_space"] = 0
        m["left_space"] = 0
        
        for i in info["indexers"]:
            if m["data"].get("account","") in i["data"].keys():
                m["indexing"] = "indexing"
                m["total_space"] = i["data"][m["data"]["account"]]["total_space"]
                m["left_space"] = i["data"][m["data"]["account"]]["left_space"]
                break
        if m["indexing"] != "indexing":
            m["indexing"] = "unindexed"
            m["total_space"] = 0
            m["left_space"] = 0
    
    return config_nodes_num, online_nodes_num, info 

@login_manager.user_loader
def load_user(user_id):
    if query_user(user_id) is not None:
        curr_user = User()
        curr_user.id = user_id
        return curr_user

@app.route('/callback/oauth2')
def login_oauth2():
    return '''  <script type="text/javascript">
                var token = window.location.href.split("#")[1]; 
                window.location = "/callback/oauth2/verifier?" + token;
           </script> '''

@app.route('/callback/oauth2/verifier')
def login_auth2():
    access_token = request.args.get("access_token")
    id_token = request.args.get("id_token")
    token_type = request.args.get("token_type")
    expires_in = request.args.get("expires_in")
    user_info = ""
    access_token = parse.quote(access_token)  
    if access_token:
        url = " https://auth.internal.pplabs.org/oauth2/userInfo"
        headers = {"Authorization":"{} {}".format(token_type,access_token)}
        response = requests.get(url=url,headers=headers)
        if(response.status_code == 200):
            ui = json.loads(response.text)
            curr_user = User()
            curr_user.id = ui["email"] 
            login_user(curr_user)
            return redirect(url_for('frontpage'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('login.html')

@app.route("/")
@login_required
def frontpage():
    result = get_summary()
    return render_template("frontpage.html",
                           c_n_n=result[0],
                           o_n_n=result[1],
                           n_i_s=result[2])

@app.route("/storage")
@login_required
def storage():
    result = get_summary()
    return render_template("frontpage.html",
                           c_n_n = result[0],
                           o_n_n = result[1],
                           n_i_s = result[2])

@app.route("/pcdn")
@login_required
def pcdn():
    return render_template("pcdn.html")

@app.route("/net")
@login_required
def net():
    local_time = time.strftime("%Y-%m-%d", time.localtime())
    cmd = "select ssid,download_speed,upload_speed,time,count from netspeed_summary;"
    history = db_handler.handle(cmd)
    
    history_data = {}
    if history and len(history) > 0:
        for h in history:
            if not history_data.get(h[0],None):
                history_data[h[0]] = {
                    "download":[],
                    "upload":[]
                }
            ds = int(h[1]/h[4] if h[4] != 0 else h[1])
            us = int(h[2]/h[4] if h[4] != 0 else h[2])
            ts = int(time.mktime(h[3].timetuple())) * 1000
            history_data[h[0]]["download"].append([ts,ds])
            history_data[h[0]]["upload"].append([ts,us])
   
    n_s_h = []
    for hd in history_data.keys():
        ssid = hd.replace(".","_")
        tmp = {
            "ssid":ssid,
            "data":history_data[hd]
        }
        n_s_h.append(tmp)

    cmd = "select ssid,download_speed,upload_speed,time from netspeed where time like \'{}%\';".format(local_time)
    today = db_handler.handle(cmd)
    print(today)

    today_data = {}
    if today and len(today) > 0:
        for t in today:
            if not today_data.get(t[0],None):
                today_data[t[0]] = []
            today_data[t[0]].append([t[3],t[1],t[2]])

    n_s_t = []
    for td in today_data.keys():
        tmp = {
            "ssid":td,
            "data":today_data[td]
        }
        n_s_t.append(tmp)

    s_h = []
    cmd = "select time,stop,count from switch_summary;"
    switch_history = db_handler.handle(cmd)
    if switch_history and len(switch_history) > 0:
        for sh in switch_history:
            s_h.append([sh[0],sh[1],sh[2],round(sh[1]/sh[2])])

    s_t = []
    cmd = "select time,stop,old,new from switch where time like \'{}%\';".format(local_time)
    switch_today = db_handler.handle(cmd)
    if switch_today and len(switch_today) > 0:
        for st in switch_today:
            s_t.append([st[0],st[1],st[2],st[3]])

    return render_template("net.html", n_s_h = n_s_h,
        n_s_t = n_s_t,
        s_h = s_h,
        s_t = s_t)

@app.route('/login', methods=['GET', 'POST'])
def login():
    return redirect("https://auth.internal.pplabs.org/oauth2/authorize?redirect_uri=https://ppio-monitor.internal.pplabs.org/callback/oauth2&response_type=token&client_id=130pc2187nrbhrr7b6t5m8r7fm&stat=STATE&identity_provider=Google")
    '''
    ret = "fail"
    try:
        if request.method == 'POST':
            ret = "fail"
            user_id = request.form.get('username')
            user = query_user(user_id)
            if user is not None and request.form['password'] == user['password']:
                curr_user = User()
                curr_user.id = user_id
                login_user(curr_user)
                ret = "success"
        elif request.method == 'GET':
            ret = render_template('login.html')
    except Exception as err:
        print(err)
        ret = "fail"
    finally:
        return ret
    '''

@app.route("/report", methods=['POST'])
def report():
    ret = "fail"
    try:
        reporter = request.remote_addr
        #if reporter in white_list:
        data_ = request.get_data()
        data_ = data_.decode()
        data = data_
        try:
            data = data_.replace("\n","!")
            data = json.loads(data)
        except Exception as err: 
            data = json.loads(data_)
        #data = json.loads(data.decode("utf-8"))
        name = data["name"]
        method_data = data.get("data","")
        src_method_data = data.get("data","")
            
        if type(method_data) == dict:
            if name == "indexer":
                tmp = method_data.get("result",[])
                method_data_str = ""
                for m in tmp:
                    s = "{}:{}:{};".format(m["MinerID"],m["TotalSpace"],m["LeftSpace"])
                    method_data_str = method_data_str + s
                method_data = method_data_str 
            method_data = json.dumps(method_data)

        cmd = ""
        local_time = time.strftime("%Y-%m-%d", time.localtime())
        if name == "netspeed": 
            method_name = data.get("method",None)
            if method_name:
                method_datas = method_data.split(",")
                if len(method_datas) == 4:
                    ds = method_datas[0].split(" ")
                    download_speed = 0
                    upload_speed = 0
                    if len(ds[1]) > 0 and ds[1][0] == "M":
                        download_speed = int(float(ds[0]) * 1024)
                    else:
                        download_speed = round(float(ds[0]))
                    us = method_datas[1].split(" ")
                    if len(us[1]) > 0 and us[1][0] == "M":
                        upload_speed = int(float(us[0]) * 1024)
                    else:
                        upload_speed = round(float(us[0]))

                    cmd = "insert into netspeed(ssid,download_speed,upload_speed,ip,report_time,time) values(\'{}\',{},{},\'{}\',\'{}\',NOW())".format(method_name,
                        download_speed,
                        upload_speed,
                        method_datas[3],
                        method_datas[2])
                    db_handler.handle(cmd)
                    
                    cmd = "select download_speed,upload_speed,count from netspeed_summary where time=\'{}\' and ssid=\'{}\';".format(local_time,method_name)
                    summary = db_handler.handle(cmd)
                    print(summary)
                    if summary and len(summary) > 0:
                        download_speed += summary[-1][0]
                        upload_speed += summary[-1][1]
                        count = summary[-1][2] + 1
                        cmd = "update netspeed_summary set download_speed={},upload_speed={},count={} where time=\'{}\' and ssid=\'{}\';".format(download_speed,upload_speed,count,local_time,method_name)
                        print(cmd)
                        db_handler.handle(cmd) 
                    else:
                        cmd = "insert into netspeed_summary(ssid,download_speed,upload_speed,ip,report_time,time) values(\'{}\',{},{},\'{}\',NULL,\'{}\');".format(method_name,
                        download_speed,
                        upload_speed,
                        local_time)
                        print(cmd)
                        db_handler.handle(cmd)

        elif name == "switch":
            method_datas = method_data.split(",")
            if len(method_datas) == 4:
                stop_time = int(method_datas[2]) if method_datas[2].isdigit() else 10
                cmd = "insert into switch(old,new,stop,report_time,time) values(\'{}\',\'{}\',{},\'{}\',NOW())".format(
                        method_datas[0],
                        method_datas[1],
                        stop_time,
                        method_datas[3])
                db_handler.handle(cmd)
                
                cmd = "select old,new,stop,time,count from switch_summary where time=\'{}\';".format(local_time)
                summary = db_handler.handle(cmd)
                if summary and len(summary) > 0:
                    stop_time = int(summary[-1][2]) + stop_time 
                    count = int(summary[-1][4]) + 1
                    cmd = "update switch_summary set old=\'{}\',new=\'{}\',stop=\'{}\',report_time=\'{}\',count={} where time=\'{}\';".format(
                        method_datas[0],
                        method_datas[1],
                        stop_time,
                        method_datas[3],
                        count,
                        local_time)
                    db_handler.handle(cmd)
                else:
                    cmd = "insert into switch_summary(old,new,stop,report_time,time) values(\'{}\',\'{}\',{},\'{}\',\'{}\')".format(method_datas[0],method_datas[1],stop_time,method_datas[3],local_time)
                    db_handler.handle(cmd)
        else:
            cmd = "insert into {}(version,reporter,crash,method,data,time) values(\'{}\',\'{}\',{},\'{}\',\'{}\',NOW());".format(
                name,
                data.get("version","---"),
                reporter,
                int(data.get("crash","0")),
                data.get("method",""),
                method_data)
            db_handler.handle(cmd)
        ret = "success"
    except Exception as err:
        print(err)
        ret = ret + str(err)
    finally:
        return ret

@app.route('/checkaccount/<account>', methods=['GET'])
def check_account(account):
    ret = ""
    cmd = "select status from log where account=\'{}\'".format(account)
    query_result = db_handler.handle(cmd)
    if query_result:
        if query_result[-1][0] == 0:
            ret = json.dumps({"code":20000,"message":""}) 
        else:
            ret = json.dumps({"code":20001,"message":"account log exists"}) 
    else:
        ret = json.dumps({"code":20002,"message":"no this account"}) 
    print(account,ret)
    return ret

@app.route('/addaccounts', methods=['GET'])
def add_account():
    ret = "success" 

    accounts = request.args.get("accounts").split("\n")
    for account in accounts:
        if account and len(account) > 0 and len(account) < 128:  
            r = None
            cmd = "select status from log where account=\'{}\'".format(account)
            query_result = db_handler.handle(cmd)

            if query_result:
                cmd = "update log set status=0, filename=\'\', add_time=NOW() where account=\'{}\'".format(account)
                r = db_handler.handle(cmd)
            else:
                cmd = "insert into log(account,add_time) values(\'{}\',NOW())".format(account)
                r = db_handler.handle(cmd)
            if r:
                ret = "fail"
    return ret 

@app.route('/upload', methods=['POST'], strict_slashes=False)
def upload_file():
    if request.method == 'POST':
        try:
            account = request.headers.get("Account")

            cmd = "select status from log where account=\'{}\'".format(account)
            query_result = db_handler.handle(cmd)
            
            if query_result:
                f = request.files.get('file')
                fname = secure_filename(f.filename)
                fpath = '{}/{}.{}'.format(BASE_DIR, fname,time.time())
                if fname.split('.')[-1] in FILE_TYPES:
                    f.save(fpath)
                    cmd = "update log set status=1, filename=\'{}\', upload_time=NOW() where account=\'{}\'".format(fpath, account)
                    db_handler.handle(cmd)
                    return json.dumps({'code':20000, "filename":fname})
                else:
                    return json.dumps({'code':20001, "error":"file type illegal"})
            else:
                return json.dumps({'error':'file format error','code':20002})
        except Exception as err:
            return json.dumps({'code':20003,'error':str(err)})
    else:
        return json.dumps({'code':20004,'error':'request must post'})

@app.route('/logmanager', methods=["GET"])
@login_required
def log_manager():
    log_list=[]

    cmd = "select account,filename,status,add_time,upload_time from log"
    query_result = db_handler.handle(cmd)

    if query_result:
        for item in query_result: 
            tmp = dict({})
            tmp["account"] = item[0]
            tmp["add_time"] = item[3].strftime("%Y-%m-%d %H:%M:%S") 
            if item[2] == 1:
                tmp["linkname"] = "download"
                tmp["url"] = "http://34.220.81.147:61111/download/{}".format(item[1].split("/")[-1])
                tmp["upload_time"] = item[4].strftime("%Y-%m-%d %H:%M:%S") 
            else:
                tmp["linkname"] = ""
                tmp["url"] = ""
                tmp["upload_time"] = ""
            log_list.append(tmp)
         
    return render_template('log_manager.html',log_list=log_list)

@app.route('/download/<filename>', methods=["GET",'POST'], strict_slashes=False)
def download_file(filename):
    fname = secure_filename(filename)
    return send_from_directory(BASE_DIR, fname, as_attachment=True)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=61111, threaded=True)
