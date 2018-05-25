#-*- encoding: utf-8 -*-

from flask import Flask
from flask import request
from flask import render_template
from jinjabread.functions import render_state
from jinjabread.functions import filehandler
from jinjabread.config import config


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
            filehandler.save_content(form_data, conf)

    else:
        form_data = render_state.dummydata

    if linkid and request.method != "POST":
        form_data = filehandler.load_content(linkid)

        if not form_data:
            linkid = ""

    history = filehandler.get_history(conf)

    if history:
        current_link = history[0]
    else:
        current_link = ""

    return render_template(
                'index.html',
                formdata     = form_data,
                output       = output,
                shareable    = conf['link_history_enabled'],
                history      = history,
                current_link = current_link
                )


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
