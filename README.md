# jinjabread

![jinjabread](http://i.imgur.com/HbGvgSj.png)

**Jinjabread** is a very simple jinja syntax checking tool for creating [SaltStack](https://www.saltstack.com) states.

It's divided into 4 windows, *Grains*, *Pillar*, *State* and *Output*, assuming you're familiar with SaltStack this does not require much explanation. If none of that makes sense, SaltStack is a *Remote Execution Framework* with *Configuration Management* capabilities. If you're a sysadmin/devops/ITguy supporting IT infrastructure of any size, SaltStack is great and you should check it out. 

Essentially, you type in the *grains* and *pillar* data you want, write your *state* template with your *jinja2*, press `ctrl+b` or click the render button.

If things go well, it produces the *state* in the *output* to make sure it rendered correctly. If an error has occured it should tell you with relative accuracy where it went wrong.

***But, why?***

Figuring out where and why your state broke can be an arduous task, 
especially if you are just starting out with SaltStack for the first time.
This tool aims to help either getting started writing *states*,
or just debugging that one state you just can't seem to fix.

I hope you enjoy it

----------------------------------------------------------------------

Features
=============================

#### Current
- Renders Jinja2 and YAML

#### Future

- Shareable links *to share with others for help*
- Proper salt integration, to use salt modules

#### Improvements

- Support for multiline comments `{# multiline comment #}` *throws some confusing `yaml` syntax errors*

Dependencies
=============================

python 2.7

```bash
 pip install flask
 pip install pyyaml
 pip install jinja2
```

Usage
=============================

```bash
~/git$ git clone https://github.com/Inveracity/jinjabread.git
~/git/jinjabread$ python __init__.py
```

Browse to `localhost:5000`


Docker (linux)
=============================

#### Build container

```bash
~/git$ docker build jinjabread/
```

#### Test container

```bash
~/git$ docker run -d -p 80:80 --name jinjabread jinjabread
~/git$ docker ps

    CONTAINER ID   IMAGE        COMMAND                  CREATED          STATUS          PORTS                NAMES
    b31fb065c2db   jinjabread   "/usr/sbin/apache2ctl"   49 minutes ago   Up 49 minutes   0.0.0.0:80->80/tcp   jinjabread

```

Browse to `localhost/`

Acknowledgements
=============================

[Codemirror](https://codemirror.net) - Code highlighting in textarea

[Bootstrap3](https://getbootstrap.com) - general styling

[jqueryUI](https://jqueryui.com/) - Resizable divs

[PersistState](https://github.com/togakangaroo/persistState) - persist jqueryUI through refresh

