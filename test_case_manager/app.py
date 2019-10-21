import os,sys,time,json,datetime,re
from queue import Queue
from flask import Flask,render_template,request
from flask import Markup
from service_config import service_config
from models import DB

conf = service_config("config.json")
db_handler = DB(conf.config["mysql"])
app = Flask(__name__)

PRIPORITY = {
    "P1":1,
    "P2":2,
    "P3":3
}

AUTOMATION = {
    "Yes":1,
    "No":0
}

SYSTEM_TABLES = ["pathes","cases"]
PATH_TABLE = "pathes"
CASE_TABLE = "cases"

PATH_BASE = 0
CASE_BASE = 100000

@app.route('/getcases', methods=["GET"])
def getcases():
    case_id = int(request.args.get("id",0))
    plan_id = request.args.get("plan_id", "")
    plan_flag = True if len(plan_id) > 0 else False
    plan_pathes = set([])

    cases = []
    untest_cases = set([])
    fail_cases = set([])

    if plan_flag:
        path_queue = set([])

        cmd = "select id,result from {};".format(plan_id)
        result, status = db_handler.handle(cmd)
        for r in result:
            plan_pathes.add(r[0])
            if r[1] == 0:
                untest_cases.add(r[0])
            elif r[1] == 2:
                fail_cases.add(r[0])

        ids_str = ",".join([str(r[0]) for r in result])
        cmd = "select id,parent from cases where id in ({})".format(ids_str)
        result, status = db_handler.handle(cmd)
        for r in result:
            parent = int(r[-1])
            id = int(r[0])
            if parent > 0:
                plan_pathes.add(parent)
                path_queue.add(parent)
            if id in untest_cases:
                untest_cases.add(parent)
            if id in fail_cases:
                fail_cases.add(parent)

        while len(path_queue) > 0:
            ids_str = ",".join([str(i) for i in path_queue])
            path_queue = set([])
            cmd = "select id,parent from pathes where id in ({});".format(ids_str)
            result, status = db_handler.handle(cmd)
            for r in result:
                parent = int(r[-1])
                id = int(r[0])
                if parent > 0:
                    plan_pathes.add(parent)
                    path_queue.add(parent)
                if id in untest_cases:
                    untest_cases.add(parent)
                if id in fail_cases:
                    fail_cases.add(parent)

    if case_id < CASE_BASE:
        cmd = 'select id,name from pathes where parent={} {};'.format(case_id,"" if plan_flag else "and status=1")
        result, status = db_handler.handle(cmd)
        for r in result:
            if plan_flag and r[0] not in plan_pathes:
                continue

            color = None
            if plan_flag:
                color = "/static/images/green.png"
                if r[0] in untest_cases:
                    color = "/static/images/yellow.png"
                if r[0] in fail_cases:
                    color = "/static/images/red.png"

            cases.append({
                "id": str(r[0]),
                "text": r[1],
                "icon": color,
                "state": {"opened": False, "disabled": False},
                "children": True
            })

        cmd = 'select id,title from cases where parent ={} {};'.format(case_id, "" if plan_flag else "and status=1")
        result, status = db_handler.handle(cmd)
        for r in result:
            if plan_flag and r[0] not in plan_pathes:
                continue

            color = None
            if plan_flag:
                color = "/static/images/green.png"
            if r[0] in untest_cases:
                color = "/static/images/yellow.png"
            if r[0] in fail_cases:
                color = "/static/images/red.png"

            cases.append({
                "id": str(r[0]),
                "text": r[1],
                "icon": color,
                "state": {"opened": False, "disabled": False},
                "children": False
            })

    elif CASE_BASE <= case_id:
        plan_info = []

        cmd = 'select * from cases where id ={} {};'.format(case_id, "" if plan_flag else "and status=1")
        case_info, status = db_handler.handle(cmd)

        if status and plan_flag:
            cmd = "select result,remarks,issues from {} where id={};".format(plan_id,case_id)
            plan_info, status = db_handler.handle(cmd)

        if status and len(case_info) > 0:
            cases = {
                "id": case_info[-1][0],
                "title": case_info[-1][1],
                "priority": case_info[-1][2],
                "auto": case_info[-1][3],
                "basic": case_info[-1][4],
                "description": case_info[-1][5],
                "steps": case_info[-1][6],
                "expect": case_info[-1][7],
                "time": case_info[-1][9].strftime("%Y-%m-%d %H:%M:%S"),
                "result": plan_info[-1][0] if len(plan_info) > 0 and plan_info else "",
                "remarks": plan_info[-1][1] if len(plan_info) > 0 and plan_info else "",
                "issues": plan_info[-1][2] if len(plan_info) > 0 and plan_info else "",
            }
    return json.dumps(cases)

def get_auto():
    cmd = 'select id,parent from cases where auto=1'
    result, status = db_handler.handle(cmd)

    case_list = set([])
    path_list = set([])
    path_list.add(0)

    for r in result:
        case_list.add(r[0])
        path_list.add(r[1])

    path_queue = Queue(maxsize=0)
    for p in path_list:
        path_queue.put(p)

    while not path_queue.empty():
        p = path_queue.get()
        cmd = 'select parent from pathes where id={}'.format(p)
        result, status = db_handler.handle(cmd)
        if result[-1][0] not in path_list:
            path_list.add(result[-1][0])
            path_queue.put(result[-1][0])

def get_High():
    pass

def get_Middle():
    pass

def get_Low():
    pass

@app.route('/updatenode', methods=["GET"])
def update_node():
    id = int(request.args.get("id", 0))
    name = request.args.get("name", "")

    ret = "fail"
    if id > 0 and name:
        cmd = "update pathes set name=\'{}\' where id={};".format(name,id)
        result, status = db_handler.handle(cmd)
        ret = "success" if status else "fail"
    return ret

@app.route('/updatecasetitle', methods=["GET"])
def update_case_title():
    id = int(request.args.get("id", 0))
    name = request.args.get("name", "")

    ret = "fail"
    if id > 0 and name:
        cmd = "update cases set title=\'{}\',update_time=NOW() where id={};".format(name,id)
        result, status = db_handler.handle(cmd)
        ret = "success" if status else "fail"
    return ret

@app.route('/addnode', methods=["GET"])
def add_node():
    name = request.args.get("name", "")
    parent = int(request.args.get("parent", 0))
    if name != "" and parent:
        cmd = "select name from pathes where parent={} and status=1;".format(parent)
        result, status = db_handler.handle(cmd)
        if name not in [r[-1] for r in result]:
            cmd = "insert into pathes(name,parent,create_time,update_time) values(\'{}\',{},NOW(),NOW());".format(name,parent)
            result, status = db_handler.handle(cmd)

            cmd = "select max(id) from cases;"
            result, status = db_handler.handle(cmd)

            return json.dumps({"case_id": result[-1][-1],"time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) if status else "fail"
    return "fail"

@app.route('/deletenode', methods=["GET"])
def delete_node():
    id = int(request.args.get("id", 0))
    cmd = "update pathes set status=0 where id={};".format(id) if id < 100000 else "update cases set status=0 where id={};".format(id)
    result, status = db_handler.handle(cmd)
    ret = "success" if status else "fail"
    return ret

@app.route('/movenode', methods=["GET"])
def move_node():
    id = int(request.args.get("id", 0))
    parent = request.args.get("parent", "#")
    parent = 0 if parent == "#" else int(parent)
    if id == parent or id <= 0 or parent < 0:
        return "fail"

    cmd = "update pathes set parent={} where id={};".format(parent,id,id) if id < CASE_BASE else "update cases set parent={} where id={};".format(parent,id,id)
    result, status = db_handler.handle(cmd)
    ret = "success" if status else "fail"
    return ret

@app.route('/createplan')
def create_plan():
    status = False

    plan_id = request.args.get("planid", None)
    case_list = request.args.get("caselist", None)

    real_case_list = set([])
    pathes = [i for i in case_list.split(",")][:-1]
    path_queue = Queue(maxsize=0)
    for p in range(len(pathes)):
        tmp = [int(i) for i in pathes[p].split("-")]
        if tmp[-1] > CASE_BASE:
            real_case_list.add(tmp[-1])
        else:
            path_queue.put(tmp)

    while not path_queue.empty():
        path = path_queue.get()
        if path[-1] > CASE_BASE:
            real_case_list.add(tmp[-1])
        else:
            cmd = "select id from pathes where parent={};".format(path[-1])
            result, status = db_handler.handle(cmd)
            if len(result) == 0:
                cmd = "select id from cases where parent={}".format(path[-1])
                result, status = db_handler.handle(cmd)
                for r in result:
                    real_case_list.add(r[-1])
            else:
                for r in result:
                    path_tmp = list(path)
                    path_tmp.append(r[-1])
                    path_queue.put(path_tmp)

    if plan_id and real_case_list:
        plan_id = plan_id.replace(".","_")
        cmd = "create table {}(id int, result int default 0, remarks text, issues text);".format(plan_id)
        result, status = db_handler.handle(cmd)

        tmp_str = ",".join(["(" + str(i) + ")" for i in real_case_list if int(i) >= CASE_BASE])
        cmd = "insert into {}(id) values {};".format(plan_id, tmp_str)
        result, status = db_handler.handle(cmd)

    return plan_id if status else "fail"

@app.route('/addcase')
def add_case():
    parent = request.args.get("parent", None)
    parent = 0 if not parent else int(parent)

    title = request.args.get("title", "")
    priority = request.args.get("priority", 0)
    auto = request.args.get("auto", 0)
    description = request.args.get("description", "")
    steps = request.args.get("steps", "")
    expect = request.args.get("expect", "")

    cmd = "insert into cases(title,priority,auto,description,steps,expect,parent,create_time,update_time) values(\'{}\',{},{},\'{}\',\'{}\',\'{}\',{},NOW(),NOW())".format(title, priority, auto, description, steps, expect,parent)
    result, status = db_handler.handle(cmd)
    if status:
        cmd = "select max(id) from cases;"
        result, status = db_handler.handle(cmd)
        if status and result:
            return json.dumps({"case_id": result[-1][-1],"time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) if status else "fail"
    return "fail"

@app.route('/updatecase')
def update_case():
    case_id = request.args.get("case_id", None)
    plan_id = request.args.get("plan_id", None)

    title = request.args.get("title", None)
    priority = request.args.get("priority", None)
    auto = request.args.get("auto", None)
    description = request.args.get("description", None)

    steps = request.args.get("steps", None)
    expect = request.args.get("expect", None)

    result = request.args.get("result", "")
    remarks = request.args.get("remarks", "")
    issues = request.args.get("issues", "")

    status = False
    if case_id and plan_id:
        cmd = "update {} set result={}, remarks=\'{}\', issues=\'{}\' where id={}".format(plan_id,result,remarks,issues,case_id)
        result, status = db_handler.handle(cmd)
    elif case_id:
        cmd = "update cases set title=\'{}\', priority={}, auto={}, description=\'{}\', steps=\'{}\', expect=\'{}\', update_time=NOW() where id={};".format(title,priority,auto,description,steps,expect,case_id)
        result, status = db_handler.handle(cmd)
    return json.dumps({"case_id": case_id, "time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) if status else "fail"

@app.route('/updateplancase')
def update_plan_case():
    case_id = request.args.get("case_id", None)
    plan_id = request.args.get("plan_id", None)

    result = request.args.get("result", "")
    remarks = request.args.get("remarks", "")
    issues = request.args.get("issues", "")

    status = False
    if case_id and plan_id:
        cmd = "update {} set result={}, remarks=\'{}\', issues=\'{}\' where id={}".format(plan_id, result, remarks, issues, case_id)
        result, status = db_handler.handle(cmd)

    return json.dumps({"case_id": case_id, "time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) if status else "fail"

@app.route('/')
def index():
    return render_template("CaseManager.html")

@app.route('/CaseManager')
def case_manager():
    return render_template("CaseManager.html")

@app.route('/PlanManager')
def plan_manager():
    cmd = "show tables;"
    result, status = db_handler.handle(cmd)
    plans = []
    for r in result:
        if r[0] not in SYSTEM_TABLES:
            plans.append(r[0])
    return render_template("PlanManager.html",plans=plans)

@app.route('/ShowPlan/<plan_id>')
def show_plan(plan_id):
    cmd = 'select create_time from information_schema.tables where table_name = \'{}\''.format(plan_id)
    plan_create_time, status = db_handler.handle(cmd)

    cmd = "SELECT result, count(*) FROM plan14 GROUP BY result"
    counts, status = db_handler.handle(cmd)

    untest_count = 0
    ok_count = 0
    fail_count = 0

    for c in counts:
        if c[0] == 0:
            untest_count = c[1]
        elif c[0] == 1:
            ok_count = c[1]
        elif c[0] == 2:
            fail_count = c[1]

    return render_template("ShowPlan.html",
        plan_id=plan_id,
        plan_create_time=plan_create_time[-1][0],
        ok_count=ok_count,
        fail_count=fail_count,
        untest_count=untest_count)

@app.route('/Report')
def report_manager():
    cmd = 'select date_format(create_time, "%%Y-%%m-%%d") as time, count(*) as total from cases group by date_format(create_time, "%%Y-%%m-%%d") order by time asc'
    result_cases, status = db_handler.handle(cmd)

    cmd = 'select date_format(create_time, "%%Y-%%m-%%d") as time, count(*) as total from cases where auto=1 group by date_format(create_time, "%%Y-%%m-%%d") order by time asc'
    result_auto, status = db_handler.handle(cmd)

    date = []
    cases = []
    auto = []

    count = 0
    cur_case_num = 0
    for r in result_cases:
        cur_case_num = cur_case_num + r[1]
        date.append([count,r[0]])
        cases.append([count,cur_case_num])
        count = count + 1

    count = 0
    cur_auto_num = 0
    for r in result_auto:
        cur_auto_num = cur_auto_num + r[1]
        auto.append([count, cur_auto_num])
        count = count + 1

    date = Markup(json.dumps(date))
    cases = json.dumps(cases)
    auto = json.dumps(auto)

    return render_template("report.html",case_date=date,case_num=cases,case_auto=auto)

if __name__ == '__main__':
    app.run(port=8088,debug = True)