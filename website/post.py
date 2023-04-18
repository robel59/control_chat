import socket
import os
import shutil
import subprocess
import threading
import yaml

def get_free_port():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind(('', 0))
    _, port = tcp.getsockname()
    tcp.close()
    return port 

def setupserver(fname):
    newpath = r'/home/robel/Desktop/WebSiteproject/adminsite/project-enviroments/django-dashboard-volt-1.0.4/media/deployedlist/'+fname
    tpath = str(newpath)+'/web'
    runa = r'/home/robel/Desktop/WebSiteproject/adminsite/project-enviroments/django-dashboard-volt-1.0.4/media/deployedlist/run.sh'
    runba = str(newpath)+'/run.sh'
    
    docetloc = str(newpath)+'/docker-compose.yaml'
    port = get_free_port()
    valu = {"version": "3.9","services":{"apache":{"image": "httpd:latest","container_name": fname,"ports":[str(port)+":80"],"restart":"always","volumes":["./web:/usr/local/apache2/htdocs"]}}}
    with open(docetloc, 'x') as f:
        yaml.dump(valu, f)

    with open(runba, 'x') as f:
        data = "#!/bin/bash\ncd "+newpath+"\ndocker-compose up -d "
        f.write(data)

    subprocess.run(["sudo", "chmod", "-R", "777", newpath], text=True, input="23wesdxc")
    password = '23wesdxc'
    step1 = subprocess.Popen(['sudo',runba],stdin=subprocess.PIPE)
    step1.communicate(password.encode())
    subprocess.Popen.wait(step1)
    print("DONE")
    return port


def restart(fname):
    newpath = r'/home/robel/Desktop/WebSiteproject/adminsite/project-enviroments/django-dashboard-volt-1.0.4/media/deployedlist/'+fname
    runba = str(newpath)+'/run.sh'
    password = '23wesdxc'
    step1 = subprocess.Popen(['sudo',runba],stdin=subprocess.PIPE)
    step1.communicate(password.encode())
    subprocess.Popen.wait(step1)



'''
import docker


def server_setup(project_name):
    client = docker.from_env()
    project_dir = r'/home/robel/Desktop/WebSiteproject/adminsite/project-enviroments/django-dashboard-volt-1.0.4/media/deployedlist/'+project_name

    compose_file = str(project_dir)+'/docker-compose.yaml'
    port = get_free_port()
    valu = {"version": "3.9","services":{"apache":{"image": "httpd:latest","container_name": project_name,"ports":[str(port)+":80"],"restart":"always","volumes":["./web:/usr/local/apache2/htdocs"]}}}
    with open(compose_file, 'x') as f:
        yaml.dump(valu, f)

    project = client.containers.run(
            'docker/compose:latest',
            command=f'up -d',
            volumes={
                '/var/run/docker.sock': {'bind': '/var/run/docker.sock', 'mode': 'rw'},
                f'{compose_file}': {'bind': '/app/docker-compose.yml', 'mode': 'rw'}
            },
            environment={'COMPOSE_PROJECT_NAME': project_name},
            detach=True
        )
    return port

def remove_server_setup(project_name):
    client = docker.from_env()
    project_dir = r'/home/robel/Desktop/WebSiteproject/adminsite/project-enviroments/django-dashboard-volt-1.0.4/media/deployedlist/'+project_name
    
    cmd = f'docker-compose -p {project_name} -f {project_dir}/docker-compose.yml down'

    # run the command in a container
    container = client.containers.run(
        'docker/compose:latest',
        command=cmd,
        remove=True,
        volumes={
            '/var/run/docker.sock': {'bind': '/var/run/docker.sock', 'mode': 'rw'},
            f'{project_dir}': {'bind': '/app', 'mode': 'rw'}
        },
        detach=True
    )

    return True
'''

