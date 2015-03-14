#!/usr/bin/python3

import urllib.request, re, os.path, sys

def get_ip():
  url="http://checkip.dyndns.org"
  response=urllib.request.urlopen(url)
  html=response.readall().decode('utf-8')
  if re.search('Current IP Address:',html):
    ip_pat=re.search("(\d+.\d+.\d+.\d+)",html)
    ip=ip_pat.group(0)

  if ip: return ip

################################################################################

def log_ip(ip):
  log = open('/var/log/dnsexit_update.log', 'w')

  log.write(current_ip)

  log.close()

################################################################################

def log_err(err):
  logerr = open('/var/log/dnsexit_update.err', 'w')

  logerr.write(err)

  logerr.close()

################################################################################

def update_ip(ip):
  url="http://update.dnsexit.com/RemoteUpdate.sv?login=macastillo&password=n0@cc3$$&host=macastillo.publicvm.com&myip=" + ip
  response=urllib.request.urlopen(url)
  html=response.readall().decode('utf-8')
  if re.search('Success',html):
    return True
  else:
    log_err('Unable to update ip')

################################################################################

if os.path.isfile('/var/log/dnsexit_update.log'):
  for line in open('/var/log/dnsexit_update.log','r'):
    current_ip=get_ip()

    if current_ip!=line:
      if update_ip(current_ip): log_ip(current_ip)
else:
  current_ip=get_ip()

  logip(current_ip)
