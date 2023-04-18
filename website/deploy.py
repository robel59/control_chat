import socket
import os
import shutil
import subprocess
import threading

def get_free_port():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind(('', 0))
    _, port = tcp.getsockname()
    tcp.close()
    return port 
                    
                    
#create project folder
def builedproject(fname):
	newpath = r'/home/robel/Desktop/WebSiteproject/adminsite/project-enviroments/django-dashboard-volt-1.0.4/media/'+fname
	docetloc = str(newpath)+'/Dockerfile'
	runba = str(newpath)+'/run.sh'
	runba1 = str(newpath)+'/start.sh'

	
	try:
		with open(docetloc, 'x') as f:
			data = "FROM httpd:2.4\nCOPY ./web/ /usr/local/apache2/htdocs/"
			f.write(data)

		port = get_free_port()
		with open(runba, 'x') as f:
			data = "#!/bin/bash\ncd "+newpath+"\ndocker build -t "+fname+" ."
			f.write(data)

		with open(runba1, 'x') as f:
			data = "#!/bin/bash\ncd "+newpath+"\ndocker run -d --restart unless-stopped --name "+fname+" -p "+str(port)+":80 "+fname
			f.write(data)

		subprocess.run(["sudo", "chmod", "-R", "777", newpath], text=True, input="23wesdxc")
		password = '23wesdxc'
		step1 = subprocess.Popen(['sudo',runba],stdin=subprocess.PIPE)
		step1.communicate(password.encode())
		subprocess.Popen.wait(step1)
		step2 = subprocess.Popen(['sudo',runba1],stdin=subprocess.PIPE)
		step2.communicate(password.encode())

		return port
	except FileNotFoundError:
		return "The 'docs' directory does not exist"

#builedproject('fnamle73')


def stopproject(fname):
	subprocess.run(["sudo", "docker", "stop", fname], text=True, input="23wesdxc")


def restart(fname):
	subprocess.run(["sudo", "docker", "start", fname], text=True, input="23wesdxc")
		

def reload(fname):
	newpath = r'/home/robel/Desktop/WebSiteproject/adminsite/project-enviroments/django-dashboard-volt-1.0.4/media/deployedlist/'+fname
	runba1 = str(newpath)+'/start.sh'
	password = '23wesdxc'
	step2 = subprocess.Popen(['sudo',runba1],stdin=subprocess.PIPE)
	step2.communicate(password.encode())
		
#restart('fnamle87')
#sudo chmod -R 777  fnamle7
#stopproject('fnamle87')