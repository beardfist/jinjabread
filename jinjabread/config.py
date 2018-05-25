import yaml

def config():
    user_conf = ""
    raw_conf = ""
    defaults = {
        'link_history_enabled':False,
        'link_history_size':500,
        'link_history_file_size':10
    }

    #Read config file
    try:
        with open('config.yml') as c:
            raw_conf = c.read()
    except IOError:
        print("could not find config.conf, using defaults")
        print(defaults)
        pass

    # Overwrite defaults with user-defined configs, if any
    if raw_conf:
        conf = yaml.safe_load(raw_conf)

        user_conf = defaults.copy()
        user_conf.update(conf)

        user_conf
    else:
        user_conf = defaults
    return user_conf
