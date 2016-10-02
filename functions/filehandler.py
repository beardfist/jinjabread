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


def _delete_file(filename):
    ''' delete a file '''
    
    os.remove(cache+os.sep+filename)


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


def _file_write(base64_string, file_link_hash):
    ''' writes content to file as base64_string '''
    
    with open(cache+os.sep+file_link_hash, 'wb') as fs:
        fs.write(base64_string)

    return True


def _file_load(file_link_hash):
    ''' return content of file as dictionary '''
    
    try:
        with open(cache+os.sep+file_link_hash, 'rb') as fs:
            payload = fs.read()
    except IOError:
        return False
    
    return payload


def _file_link(json):
    ''' generates hash based on file content '''

    return str(hex(hash( json ).__abs__()).replace('0x', "").upper())


def get_history(cache_limit):
    ''' returns list of files from history, and removes the oldest if list exceeds cache limit '''

    files = glob.glob(cache+os.sep+"*")
    files.sort(key=os.path.getmtime)
    list_of_links = [ f.split(os.sep)[-1] for f in files.__reversed__() ]

    if len(list_of_links) > cache_limit:
        _delete_file(list_of_links[-1])
        list_of_links = list_of_links[:-1]

    return list_of_links


def save_content(payload):
    ''' save content to a file if file does not exceed 500kb '''

    content = json.dumps(payload, ensure_ascii=False, encoding='utf-8', indent=4)
    data = _content_encode(content)
    
    if _safe_size(data):
        link = _file_link(content)
        _file_write(data, link)
    else:
        raise Exception("Size of input data exceeds minimum allowance of 500kb")

    return link


def load_content(link_id):
    ''' get file content, return as dictionary '''
    
    content = _file_load(link_id)
    if content:
        data = _content_decode(content)
        payload = json.loads(data, encoding='utf-8') #special characters don't work to well here sadly
    else:
        return False
        
    return payload


#link = save_content(payload)
#get_history(0)
#data = load_content(link)
#from render_state import mash
#print mash(data['grains'][0], data['pillar'][0], data['state'][0])[0]