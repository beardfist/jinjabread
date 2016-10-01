#-*- encoding: utf-8 -*-
import os
import sys
import glob
import uuid
import json
import shutil
import base64

# Create cache dir in project root
cache = os.sep.join(__file__.split(os.sep)[:-2])+os.sep+"cache"
try:
    os.mkdir(cache)
except:
    pass

payload = {"pillar":["""\
secret: 1A2B3C4D5E6F
ns:
  - 12.34.45.1
  - 12.34.45.2
"""], 
"grains":["""\
host: minion
id: minion.domain.net
domain: domain.net
fqdn: minion.domain.net
fqdn_ip4:
  - 192.168.1.3
saltversion: 2016.3.3
os: Debian
os_family: Debian
osarch: amd64
oscodename: jessie
osfinger: Debian-8
osfullname: Debian
osmajorrelease: '8'
osrelease: '8.2'
biosreleasedate: 01/01/2011
biosversion: Bochs
cpuarch: x86_64
ip4_nameservers:
  - 8.8.8.8
  - 8.8.4.4
ip4_interfaces: 
  eth0:
    - 192.168.1.3
kernel: Linux
localhost: minion.domain.net
mem_total: 2010
num_cpus: 2

"""], 
"state":["""\
{% set secret = pillar['secret'] %}
{% set domain = grains['domain'] %}
{% set osfinger = salt['grains.get']('osfinger') %}
{% set nameservers = salt['pillar.get']('ns') %}

{% if domain == 'domain.net' %}
set secret:
  file.managed:
    - name: /etc/secret
    - source: salt://state/secret
    - template: jinja
    - context:
        secret: {{ secret }}
{% endif %}

eth0:
  network.managed:
    - dns:
        {% for ip in nameservers %}
      - {{ ip }}
        {% endfor %}
"""]}


def get_history():
    ''' returns list of files from history '''

    files = glob.glob(cache+os.sep+"*")
    files.sort(key=os.path.getmtime)
    list_of_links = [f.split(os.sep)[-1] for f in files.__reversed__() ]

    return list_of_links

def _safe_size(payload):
    ''' if file size limit exceeds 500 kb return false '''
    if sys.getsizeof(payload) > 512000:
        return False
    return True

def _content_encode(content):
    ''' base64 encode data '''
    return base64.b64encode(content)

def _content_decode(content):
    ''' decode base64 data '''
    return base64.b64decode(content)

def _file_write(json, file_link_hash):
    ''' writes content to file as json '''
    
    with open(cache+os.sep+file_link_hash, 'wb') as fs:
        fs.write(json)

    return True

def _file_load(file_link_hash):
    ''' return content of file as dictionary '''
    
    with open(cache+os.sep+file_link_hash, 'rb') as fs:
        payload = fs.read()

    return payload

def _file_link(json):
    ''' generates hash based on file content '''

    return str(hex(hash( json ).__abs__()).replace('0x', "").upper())

def save_content(payload):
    ''' save content to a file if file does not exceed 500kb '''

    # TODO: if at cache file limit, overwrite oldest file
    content = json.dumps(payload, ensure_ascii=False, encoding='utf-8', indent=4)
    data = _content_encode(content)
    
    if _safe_size(data):
        link = _file_link(content)
        _file_write(data, link)
    else:
        raise Exception("Size of input data exceeds minimum allowance of 500kb")

    return link

def load_content(link_id):
    content = _file_load(link_id)
    data    = _content_decode(content)
    payload = json.loads(data, encoding='utf-8') #special characters don't work to well here sadly

    return payload


#link = save_content(payload)
#get_history()
#data = load_content(link)
#from render_state import mash
#print mash(data['grains'][0], data['pillar'][0], data['state'][0])[0]