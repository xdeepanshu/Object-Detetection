import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import time
from nameko.standalone.rpc import ClusterRpcProxy
import json


UPLOAD_FOLDER = os.getcwd() + '/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


CONFIG = {'AMQP_URI': "amqp://zqtfjfbn:tH8aOU7bVgzi0TDhIA0xAYd4lUyZ5pa2@mustang.rmq.cloudamqp.com/zqtfjfbn"}
API_KEY = 'aril9uRBwIvx97EYdIfb7X0frsK0i4E83veo238HO2QD'



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_extension(filename):
    if '.' in filename and '\\' :
    	return filename.rsplit('.', 1)[1].lower()


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
        	#for security purpose
            filename = time.strftime("%Y%m%d-%H%M%S") + '.' + get_file_extension(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/detect', methods=['GET','POST'])
def detect():
    if request.method == 'POST':
        image_url = request.form['link']
        with ClusterRpcProxy(CONFIG) as rpc:
            result1 = rpc.detect.compute(image_url, API_KEY)
            #print(result1)
            return json.dumps(result1)
    else:
        return '''
        <!doctype html>
        <title>Enter the link of the file</title>
        <h1>Link of the file</h1>
        <form method=post enctype=multipart/form-data>
          <input type=text name=link>
          <input type=submit value=Upload>
        </form>
        '''


if __name__ == "__main__":
	app.run(debug=True)
