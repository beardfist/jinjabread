#-*- encoding: utf-8 -*-
import os
import sys
import glob
import json

# Create cache dir in project root
cache = os.sep.join(__file__.split(os.sep)[:-2])+os.sep+"cache"
try:
    os.mkdir(cache)
except:
    pass


def _delete_file(filename):
    ''' delete a file '''
    
    os.remove(cache+os.sep+filename)


def _safe_size(payload, limit):
    ''' if file size limit return false '''
    
    limit = limit * 1024
    size = sys.getsizeof(payload)
    
    if size > limit:
        return False
    return True


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


def get_history(conf):
    ''' returns list of files from history, 
        and removes the oldest if list exceeds cache limit '''

    limit = conf['link_history_size']
    files = glob.glob(cache+os.sep+"*")
    files.sort(key=os.path.getmtime)
    list_of_links = [ f.split(os.sep)[-1] for f in files.__reversed__() ]

    if len(list_of_links) > limit:
        _delete_file(list_of_links[-1])
        list_of_links = list_of_links[:-1]

    return list_of_links


def save_content(payload, conf):
    ''' save content to a file if file does not exceed 
        link_history_file_size '''

    limit = conf['link_history_file_size']
    content = json.dumps(payload, ensure_ascii=False, encoding='utf-8')
    
    if _safe_size(content, limit):
        link = _file_link(content)
        _file_write(content, link)
    else:
        return "size_limit_exceeded!"

    return link


def load_content(link_id):
    ''' get file content, return as dictionary '''
    
    content = _file_load(link_id)

    try:
        #special characters don't work to well here sadly
        payload = json.loads(content, encoding='utf-8') 
    except:
        return False
        
    return payload

# -- testing --
#from render_state import mash

#link = save_content(payload)
#data = load_content(link)
#print mash(data['grains'][0], data['pillar'][0], data['state'][0])[0]