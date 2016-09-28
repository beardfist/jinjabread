#-*- encoding: utf-8 -*-
from salt import saltyaml

import yaml
from jinja2 import Template
import re
import traceback

def lookup(d, key):
    ''' recursive dictionary lookup until value for a key is found '''
    stack = d.items()
    while stack:
        k, v = stack.pop()
        if isinstance(v, dict):
            stack.extend(v.iteritems())
        else:
            try:
                if k == key:
                    return v
            except:
                pass

def pre_render_test(state):
    pre_state_format = []

    # avoid pre-render errors by commenting out jinja code, but still retaining codeplacement for debug messages.
    for line in state.splitlines():
        if "{%" in line or "{#" in line or "#}" in line:
            line = "#"+line
        if "{{" in line and "}}" in line:
            line = line.replace("{{", "'{{").replace("}}", "}}'")
        pre_state_format.append(line)
        #print line
    
    pre_state = '\n'.join(pre_state_format)
    pre_test_render = saltyaml.render(pre_state)
    return pre_state

def post_render_test(rendered_template):
    filtered_template = "\n".join([ll.rstrip() for ll in rendered_template.splitlines() if ll.strip()])
    prettify = []

    for line in filtered_template.splitlines():
        if not line.startswith(' '):
            line = "\n"+line
        prettify.append(line)
    
    filtered_template = '\n'.join(prettify)
    test_render = saltyaml.render(rendered_template)
    return [filtered_template, test_render]

def mash(grains, pillar, state):
    ''' Takes yaml and jinja templates, and render them as yaml'''
    try:
        yamlpillar = yaml.safe_load(pillar)
        yamlgrain = yaml.safe_load(grains)


        def pillarget(item):
            if ":" in item:
                item = item.split(':')
                return lookup(yamlpillar, item[-1]) # this is bad. It disregards nested keys thus every key needing to be unique to avoid errors

            return yamlpillar[item]


        def grainsget(item):
            if ":" in item:
                item = item.split(':')
                value = lookup(yamlgrain, item[-1])
                return value                

            return yamlgrain[item]

        salt = {'pillar.get':pillarget, 'grains.get':grainsget}
        
        # check yaml syntax before rendering
        pre_render_test(state)
        
        # render state
        template = Template(state)
        rendered_template = template.render({'pillar':yamlpillar, 'grains':yamlgrain, 'salt':salt})

        # check yaml syntax after rendering
        completed_render = post_render_test(rendered_template)

        return completed_render

    except Exception as e:
        return [str(e).replace("could not found","could not find"), "fail"]


dummydata = {"pillar":["""\
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
asd
eth0:
  network.managed:
    - dns:
        {% for ip in nameservers %}
      - {{ ip }}
        {% endfor %}
"""]}

#print mash(dummydata['grains'][0], dummydata['pillar'][0], dummydata['state'][0])[0]