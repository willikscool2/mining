import pathlib, stat, shutil, urllib.request, subprocess, getpass, time, tempfile
import secrets, json, re
import IPython.utils.io
import ipywidgets
import socket
import os
from IPython.display import clear_output



def _download(url, path):
  try:
    with urllib.request.urlopen(url) as response:
      with open(path, 'wb') as outfile:
        shutil.copyfileobj(response, outfile)
  except:
    print("Failed to download ", url)
    raise

  return True

def _setupssh():
  #Inpur Username
  user_name = "ubuntu"
  subprocess.run(["useradd", "-s", "/bin/bash", "-m", user_name])
  subprocess.run(["adduser", user_name, "sudo"], check = True)
  clear_output()

  #Inpur Password
  user_password = "willy123"
  subprocess.run(["chpasswd"], input = f"{user_name}:{user_password}", universal_newlines = True)
  clear_output()

  #Set your ngrok Authtoken.
  ngrok_token = "1tkY8NiSuWBkbta3sQRkHM0EVih_5XM3H9Li7GJ5TXqkkJBNB"

  #Set your ngrok region.
  print("Select your ngrok region :")
  print("us - United States (Ohio)")
  print("eu - Europe (Frankfurt)")
  print("ap - Asia/Pacific (Singapore)")
  print("au - Australia (Sydney)")
  print("sa - South America (Sao Paulo)")
  print("jp - Japan (Tokyo)")
  print("in - India (Mumbai)")
  ngrok_region = "ap"
  clear_output()

  #SSH Dropbear
  os.system("sudo apt-get install -y dropbear")

  #Set Dropbear
  f = open("../etc/default/dropbear", "w")
  f.write("""# the TCP port that Dropbear listens on
DROPBEAR_PORT=443

# any additional arguments for Dropbear
DROPBEAR_EXTRA_ARGS=

# specify an optional banner file containing a message to be
# sent to clients before they connect, such as "/etc/issue.net"
DROPBEAR_BANNER=""

# RSA hostkey file (default: /etc/dropbear/dropbear_rsa_host_key)
#DROPBEAR_RSAKEY="/etc/dropbear/dropbear_rsa_host_key"

# DSS hostkey file (default: /etc/dropbear/dropbear_dss_host_key)
#DROPBEAR_DSSKEY="/etc/dropbear/dropbear_dss_host_key"

# ECDSA hostkey file (default: /etc/dropbear/dropbear_ecdsa_host_key)
#DROPBEAR_ECDSAKEY="/etc/dropbear/dropbear_ecdsa_host_key"

# Receive window size - this is a tradeoff between memory and
# network performance
DROPBEAR_RECEIVE_WINDOW=65536
""")
  f.close()

  #SSH Service Restart
  subprocess.run(["service", "dropbear", "restart"])

  #Root Password
  root_password = user_password
  subprocess.run(["chpasswd"], input = f"root:{root_password}", universal_newlines = True)

  # Ngrok Tunnel
  if not os.path.exists('ngrok.zip'):
    _download("https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip", "ngrok.zip")
    shutil.unpack_archive("ngrok.zip")
    pathlib.Path("ngrok").chmod(stat.S_IXUSR)

  subprocess.run(["./ngrok", "authtoken", ngrok_token])
  ngrok_proc = subprocess.Popen(["./ngrok", "tcp", "-region", ngrok_region, "443"])
  time.sleep(2)

  with urllib.request.urlopen("http://localhost:4040/api/tunnels") as response:
    url = json.load(response)['tunnels'][0]['public_url']
    m = re.match("tcp://(.+):(\d+)", url)

  hostname = m.group(1)
  port = m.group(2)
  
  msg = ""
  msg += "="*48 + "\n"
  msg += "Command to connect to the ssh server:\n"
  msg += f"ssh -p {port} {user_name}@{socket.gethostbyname(hostname)}\n"
  msg += "="*48 + "\n"
  msg += "SSH Login Termux and Git bash:\n"
  msg += f"host          : ssh -p {port} {user_name}@{socket.gethostbyname(hostname)}\n"
  msg += f"Username      : {user_name}\n"
  msg += f"Password      : {user_password}\n"
  msg += f"Subscribe     : https://www.youtube.com/c/BangAndroid10\n"
  msg += "="*48 + "\n"
  return msg
  
  
def startColab():
  msg = _setupssh()
  print(msg)

startColab()
