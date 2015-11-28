#!/usr/bin/env python
# title           :pimpositor_server.py
# description     :Backend server for pimpositor.
# author          :PatilaCode
# date            :20151128
# version         :0.4
# usage           :python pimpositor_server.py --host host --port port
# notes           :
# python_version  :2.7.10
# =============================================================================

# Import the modules needed to run the script.
import os
import sys
import shelve
import argparse
import logging
import traceback
from datetime import datetime
from uuid import uuid4
from flask import Flask, render_template, request
from werkzeug import secure_filename
from PIL import Image
# , url_for
# , redirect, url_for

logging.basicConfig(filename='log/pimpositor.log',
                    level=logging.DEBUG,
                    format='%(asctime)s %(message)s')

DB_PATH = 'db/pimpositor'

# template_dir = os.path.abspath('../html/')
# app = Flask(__name__, template_folder=template_dir)

# Images configuration
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
UPLOAD_FOLDER = 'static/usr_src_img/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# App config
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
# CORS(app)


def open_db():
    return shelve.open(DB_PATH)


def allowed_file(filename):
    """
    Check if the file meets minimum requirements
        * Has '.' in the name
        * Has accepted extension
    """
    logging.info("Checking if file is allowed...")
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def generate_unique_uuid():
    """
    Generate a unique UUID and create a blank database entry for it.
    """
    uuid = str(uuid4())
    db = open_db()
    logging.info("Generating UUID...")
    if uuid in db:
        logging.info("UUID already exists, generating another one...")
        return generate_unique_uuid()

    db[uuid] = {"uploaded": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    db.close()
    return uuid


def save_usr_img(request):
    """
    Save image to local disk with a unique name.
    Also save uuid to database with uploaded datetime
    """
    try:
        logging.info("Getting picture from POST")
        file = request.files['picture']
        if file.content_length:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                extension = filename.split('.')[-1]
                uuid = generate_unique_uuid()

                logging.info(
                    "Saving image to disk at {0}/{1}.{2}".format(
                        app.config['UPLOAD_FOLDER'],
                        uuid,
                        extension))
                path = os.path.join(app.config['UPLOAD_FOLDER'],
                                    "{0}.{1}".format(uuid, extension))
                file.save(path)

                image_size = Image.open(path).size
                width = image_size[0]
                height = image_size[1]
                return {'status': True,
                        "uuid": uuid,
                        "extension": extension,
                        "width": width,
                        "height": height}
        else:
            raise
    except:
        logging.error(traceback.format_exc())
        return {"status": False}


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    """
    Main method.
        * Returns index page and also returns 'pimped' image
          dependending on request method
    """
    if request.method == 'POST':
        logging.info("Received POST")
        save_dict = save_usr_img(request)
        saved = save_dict['status']
        if saved:
            # pimp!
            img_url = "http://{0}/static/usr_src_img/{1}.{2}".format(
                request.host,
                save_dict["uuid"],
                save_dict["extension"])

            logging.info("Rendering pimpositor...")

            return render_template('pimpositor.html',
                                   img_url=img_url,
                                   width=save_dict["width"],
                                   height=save_dict["height"])
        else:
            return render_template('problem.html')
    else:
        logging.info("Serving index page...")
        return render_template('index.html')


class PimpParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


if __name__ == '__main__':
    try:
        parser = PimpParser()
        parser.add_argument("--host",
                            default="127.0.0.1",
                            help="IP to run on [default: 127.0.0.1]")
        parser.add_argument("--port",
                            default=8080,
                            type=int,
                            help="port to listen to [default: 8080")
        parser.add_argument("--debug",
                            default=False,
                            help="to set debug mode on [default: False]")
        args = parser.parse_args()

        app.run(host=args.host, port=args.port, debug=args.debug)

    except:
        logging.error(traceback.format_exc())
