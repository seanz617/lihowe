import os,sys,time,json,datetime
from service_config import service_config
from models import DB

conf = service_config("/home/ec2-user/tangsan/monitor/config.json")
db_handler = DB(conf.config["mysql"])
nodes = conf.config["resource"]

def update_report(name):
    cmd = "select * from {} order by id desc limit 1;".format(name)
    node_query_result = db_handler.handle(cmd)

    cmd = "select sum(crash) from {};".format(name)
    crash_count = db_handler.handle(cmd)[-1][0]

    cmd = "select * from report where name=\"{}\";".format(name)
    report_query_result = db_handler.handle(cmd)
    
    if node_query_result and len(node_query_result) > 0 and report_query_result and len(report_query_result) > 0:
        delta = node_query_result[-1][6] - report_query_result[-1][7]
        if delta.total_seconds() > 0:
           cmd = "update report set version=\'{}\', reporter=\'{}\', crash={}, method=\'{}\', data=\'{}\', time=\'{}\', crash={} where name=\'{}\';".format(node_query_result[-1][1], node_query_result[-1][2], node_query_result[-1][3], node_query_result[-1][4], node_query_result[-1][5], node_query_result[-1][6], crash_count, name); 
           db_handler.handle(cmd)

def update_netspeed():
    pass

def update_switch():
    pass

if __name__ == "__main__":
    try:
        #center
        for center in nodes["centers"]["node_list"]:
            update_report(center)

        #bootstrap
        for bootstrap in nodes["bootstraps"]["node_list"]:
            update_report(bootstrap)

        #verifier
        for verifier in nodes["verifiers"]["node_list"]:
            update_report(verifier)

        #verifier
        for indexer in nodes["indexers"]["node_list"]:
            update_report(indexer)

        #miner
        for miner in nodes["miners"]["node_list"]:
            update_report(miner)
    except Exception as err:
        print(err)
