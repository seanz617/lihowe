import os,sys,time
import threading
from kubernetes import client, config, utils
from kubernetes.stream import stream

class node_factory:

    def __init__(self):
        self.kube_config_file = './kubeconfig.yml' 
        config.kube_config.load_kube_config(config_file=self.kube_config_file)
        self.api_v1 = client.CoreV1Api()

    def get_pod(self, name, namespace='default'):
        ret = []
        pods = None
        try:
            pods = self.api_v1.list_namespaced_pod(namespace=namespace, watch=False)
        except Exception as err:
            logger.info(err,html=True,also_console=True)
            pods = None
        for pod in pods.items:
            if pod.metadata.name == name:
                ret.append(pod)
            if pod.metadata.owner_references != None:
                for name_iter in pod.metadata.owner_references:
                    if name_iter.name == name:
                        ret.append(pod)
        return ret

    def pod_exec(self, name, namespace='default'):
        ret = True 
        pod_stream = None
        pod_list = self.get_pod(name) 
        if len(pod_list) <= 0:
            print(name + ": node not found\n")
            return
        else:
            name = pod_list[0].metadata.name
            print("node name: %s\n",name)

        try:
            pod_stream = stream(self.api_v1.connect_get_namespaced_pod_exec,
				name,
                                namespace,
                                command="/bin/sh",
				stderr=True,
                                stdin=True,
                                stdout=True,
				tty=True,
                                _preload_content=False)

            while pod_stream.is_open():
                '''
                if pod_stream.peek_stdout():
                    print(pod_stream.read_stdout())

                if pod_stream.peek_stderr():
                    print(pod_stream.read_stderr())
                '''
                cmd_item = input("#") 
                if cmd_item == 'leave':
                    break
                pod_stream.write_stdin(cmd_item + "\n")
                pod_stream.update(timeout=1)
                if pod_stream.peek_stdout():
                    print(pod_stream.read_stdout())

                if pod_stream.peek_stderr():
                    print(pod_stream.read_stderr())
        except Exception as err:
            print(err)
        finally:
            if(pod_stream != None):
                pod_stream.close()
        return ret

if __name__ == "__main__":
    kf = node_factory()
    kf.pod_exec(sys.argv[1])
