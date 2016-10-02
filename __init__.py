#-*- encoding: utf-8 -*-
try:
    from flask import Flask
    from flask import request
    from flask import render_template

except ImportError:
    print "warning, flask not installed"
    print "pip install flask"
    exit(1)


from functions import render_state
from functions import filehandler
from config import config
conf = config()

app = Flask(__name__)

@app.route('/',         methods=['GET', 'POST'])
@app.route('/<linkid>', methods=['GET', 'POST'])
def index(linkid=""):

    output = ""

    if request.method == 'POST':
        linkid=""
        form_data = dict(request.form)

        output = render_state.mash(
                        form_data['grains'][0], 
                        form_data['pillar'][0], 
                        form_data['state'][0])

        if 'save' in form_data.keys():
            filehandler.save_content(form_data)

    else: 
        form_data = render_state.dummydata

    if linkid and request.method != "POST":
        form_data = filehandler.load_content(linkid)

        if not form_data:
            linkid = ""
    
    history = filehandler.get_history(conf['link_history_size'])

    if history:
        current_link = history[0]
    else: 
        current_link = ""

    return render_template(
                'index.html', 
                formdata  = form_data, 
                output    = output,
                shareable = conf['enable_shareable_links'],
                history   = history,
                current_link = current_link 
                )


if __name__ == '__main__':
    app.run()

