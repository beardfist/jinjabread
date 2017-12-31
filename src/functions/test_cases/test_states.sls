{# ====== TEST: Get grains and pillar ====== #}
{% set secret = pillar['secret'] %}
{% set domain = grains['domain'] %}
{% set osfinger = salt["grains.get"]('osfinger') %}
{% set number = salt["pillar.get"]('number') %}
test1: {{ secret }}
test2: {{ domain }}
test3: {{ osfinger }}
test4: {{ number }}
{# ====== END ====== #}

{# ====== TEST: Loop over list ====== #}
{% set nameservers = pillar['ns'] %}
test:
{% for ip in nameservers %}
  - {{ ip }}
{% endfor %}
{# ====== END ====== #}

{# ====== TEST: Get nested pillar ====== #}
{% set eggs = pillar['nest']['bird'] %}
omelette:
{% for egg in eggs %}
  - {{ egg }}
{% endfor %}
{# ====== END ====== #}

{# ====== TEST: Loop over split string ====== #}
list:
{% for thing in "a/b/c/d".split('/') %}
  - {{ thing }}
{% endfor %}
{# ====== END ====== #}

{# ====== TEST: FAIL_ON_PURPOSE Conflicting ID ====== #}
{% set nameservers = pillar['ns'] %}
{% for ip in nameservers %}
test:
  - {{ ip }}
{% endfor %}
{# ====== END ====== #}

{# ====== TEST: FAIL_ON_PURPOSE could not find expected ':' ====== #}
stuff:
  and a thing

test
morestuff: sdfsdf
{# ====== END ====== #}
