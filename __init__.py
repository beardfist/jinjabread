try:
    from flask import Flask
    from flask import request
    from flask import render_template

except ImportError:
    print "warning, flask not installed"
    print "pip install flask"
    exit(1)

from functions import render_state

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    output = ""
    if request.method == 'POST':
        form_data=dict(request.form)

        output = render_state.mash(form_data['grains'][0], form_data['pillar'][0], form_data['state'][0])
    else: 
        form_data=render_state.dummydata

    return render_template('index.html', formdata=form_data, output=output)


if __name__ == '__main__':
    app.run()



