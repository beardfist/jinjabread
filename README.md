# jinjabread version 2018.05

>**Disclaimer**: It's a prototype full of unexpected behavior like throwing nondescript errors when using single quotes when it expects double quotes. I fully intend to rip out the prototype code and replace it with proper salt template rendering code. Just have to find the time to dig into it.

![jinjabread](http://i.imgur.com/HbGvgSj.png)

![resizable](http://i.imgur.com/LYyvrSj.gif)

**Jinjabread** is a very simple jinja syntax checking tool for creating [SaltStack](https://www.saltstack.com) states.

It's divided into 4 windows, *Grains*, *Pillar*, *State* and *Output*, assuming you're familiar with SaltStack this does not require much explanation. If none of that makes sense, SaltStack is a *Remote Execution Framework* with *Configuration Management* capabilities. If you're a sysadmin/devops/ITguy supporting IT infrastructure of any size, SaltStack is great and you should check it out.

**Essentially**, you type in the *grains* and *pillar* data you want, write your *state* template with your *jinja2*, press `ctrl+b` or click the render button.

If things go well, it produces the *state* in the *output* to make sure it rendered correctly. If an error has occured it should tell you with relative accuracy where it went wrong.

***But, why?***

Figuring out where and why your state broke can be an arduous task,
especially if you are just starting out with SaltStack for the first time.
This tool aims to help either getting started writing *states*,
or just debugging that one state you just can't seem to fix.

I hope you enjoy it

[Try a demo at www.jinjabread.com](http://www.jinjabread.com/)

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

#### Known issues

- Does not work in *Internet Explorer*

Dependencies
=============================

python 3.5+
pipenv 2018+

Usage
=============================

```bash
git clone https://github.com/Inveracity/jinjabread.git
cd jinjabread
pip install pipenv
pipenv sync
pipenv run start
```

Browse to `localhost:5000`


Docker
=============================

#### Build container

```bash
pipenv run build
```

#### Test container

```bash
docker run -d -p 80:80 --name jinjabread jinjabread:latest
```

Browse to `localhost/`

Acknowledgements
=============================

[SaltStack](https://www.saltstack.com) - Extensive use of their code from github

[Codemirror](https://codemirror.net) - Code highlighting in textarea

[Bootstrap3](https://getbootstrap.com) - general styling

[jqueryUI](https://jqueryui.com/) - Resizable divs

[PersistState](https://github.com/togakangaroo/persistState) - persist jqueryUI through refresh

