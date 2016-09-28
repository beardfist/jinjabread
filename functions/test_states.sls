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
test1:
{% for ip in nameservers %}
  - {{ ip }}
{% endfor %}
{# ====== END ====== #}

{# ====== TEST:FAIL_ON_PURPOSE Conflicting ID ====== #}
{% set nameservers = pillar['ns'] %}
{% for ip in nameservers %}
test1:
  - {{ ip }}
{% endfor %}
{# ====== END ====== #}