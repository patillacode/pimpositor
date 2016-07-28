#!/usr/bin/env python
#
# This file is part of Pimpositor.  Pimpositor is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright Patilla Code
#
# title           :pimpositor_server.py
# description     :Backend server for pimpositor.
# author          :PatilaCode
# date            :20151128
# version         :0.4
# usage           :python pimpositor_server.py --host host --port port
# notes           :
# python_version  :2.7.10
# =============================================================================

import os
import sys
import shelve
import argparse
import logging
import traceback

from uuid import uuid4
from datetime import datetime

from PIL import Image
from werkzeug import secure_filename
from flask import Flask, render_template, request

logging.basicConfig(stream=sys.stdout,
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    handlers=[logging.StreamHandler()])

# logging.basicConfig(filename='log/pimpositor.log',
#                     level=logging.DEBUG,
#                     format='%(asctime)s %(message)s')

DB_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    ('db/pimpositor'))

# Images configuration
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    ('static/usr_src_img'))
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# App config
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH


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


def generate_and_save_uuid_to_db():
    """
    Generate a unique UUID and create a record in db with datetime for it
    """
    uuid = str(uuid4())
    db = open_db()
    logging.info("Generating UUID...")
    if uuid in db:
        logging.info("UUID already exists, generating another one...")
        return generate_and_save_uuid_to_db()

    db[uuid] = {"uploaded": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    db.close()
    return uuid


def save_img(request):
    """
    Save image to local disk with a unique name.
    Also save image's uuid to database with uploaded datetime
    """
    logging.info("Getting picture from POST")

    if request.files and 'picture' in request.files:

        image = request.files['picture']

        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            extension = filename.split('.')[-1]
            uuid = generate_and_save_uuid_to_db()

            logging.info(
                "Saving image to disk at {0}/{1}.{2}".format(
                    app.config['UPLOAD_FOLDER'],
                    uuid,
                    extension))
            path = os.path.join(app.config['UPLOAD_FOLDER'],
                                "{0}.{1}".format(uuid, extension))
            try:
                image.save(path)
            except:
                logging.error("There was a problem saving the image.")
                logging.error(traceback.format_exc())
                return {"status": False}

            try:
                image_size = Image.open(path).size
                width = image_size[0]
                height = image_size[1]
            except:
                logging.error("There was a problem opening the image.")
                logging.error(traceback.format_exc())
                return {"status": False}

            return {'status': True,
                    "uuid": uuid,
                    "extension": extension,
                    "width": width,
                    "height": height}
        else:
            logging.info(
                "Data does not meet requirements. Check the size.")
            return {"status": False}
    else:
        logging.info("No data was uploaded.")
        return {"status": False}


# Used for testing
@app.route('/problem', methods=['GET'])
def problem():
    return render_template('problem.html', request=request)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    """
    Main method.
        * Returns index page and also returns 'pimped' image
          dependending on request method
    """
    if request.method == 'POST':
        logging.info("Received POST")
        save_dict = save_img(request)
        saved = save_dict['status']
        if saved:
            # pimp!
            img_url = "static/usr_src_img/{0}.{1}".format(
                save_dict["uuid"],
                save_dict["extension"])

            logging.info("Rendering pimpositor...")

            return render_template('pimpositor.html',
                                   img_url=img_url,
                                   width=save_dict["width"],
                                   height=save_dict["height"])
        else:
            return render_template('problem.html', request=request)
    else:
        logging.info("Serving index page...")
        return render_template('index.html')


class PimpParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


if __name__ == '__main__':
        parser = PimpParser()
        parser.add_argument("--host",
                            default="127.0.0.1",
                            help="IP to run on [default: 127.0.0.1]")
        parser.add_argument("--port",
                            default=7070,
                            type=int,
                            help="port to listen to [default: 7070")
        parser.add_argument("--debug",
                            default=False,
                            help="to set debug mode on [default: False]")
        args = parser.parse_args()

        print "Running on {0}:{1} ...".format(args.host, args.port)
        app.run(host=args.host, port=args.port, debug=args.debug)
