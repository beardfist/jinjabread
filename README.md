# jinjabread

![jinjabread](http://i.imgur.com/HbGvgSj.png)

DEPENDENCIES
=============================

python 2.7

```bash
 pip install flask
 pip install pyyaml
 pip install jinja2
```

ACKNOWLEDGEMENTS
=============================

[Codemirror](https://codemirror.net)

[Bootstrap 3](https://getbootstrap.com)

USAGE
=============================

```bash
~/git/jinjabread$ python __init__.py
```

Browse to `localhost:5000`


DOCKER (linux)
=============================

### BUILD CONTAINER

```bash
~/git$ docker build jinjabread/
```

### TEST CONTAINER

```bash
~/git$ docker run -d -p 80:80 --name jinjabread jinjabread
~/git$ docker ps

    CONTAINER ID   IMAGE        COMMAND                  CREATED          STATUS          PORTS                NAMES
    b31fb065c2db   jinjabread   "/usr/sbin/apache2ctl"   49 minutes ago   Up 49 minutes   0.0.0.0:80->80/tcp   jinjabread

```

Browse to `localhost/`
