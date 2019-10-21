#author: Hongwei Liu
#date: 2018-12-11
#describe: sync log from remote nodes

import commands
import json

skip_node = {
	"redis":True,
	"kibana":True,
	"logstash":True,
	"elasticsearch":True,
	"mysql":True,
	"gppio":True,
	"jenkins-slave-for-master":True,
}

if __name__ == "__main__":
  ret,output = commands.getstatusoutput("kubectl get pods -o json")
  ret = json.loads(output)
  for node in ret["items"]:
	containers = node["status"]["containerStatuses"]
	for contrainer in containers:
		name = contrainer["name"]
		host = node["status"]["hostIP"]
		if skip_node.get(name, None) == None:
			commands.getstatusoutput("mkdir "+name)
			r,o = commands.getstatusoutput("scp root@" + host +":/home/regnet-config/master/" + name + "/*.log ./" + name + "/" )
			print o
