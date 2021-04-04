import os

import shelve
import traceback
from uuid import uuid4
from datetime import datetime

from PIL import Image


from flask import (
    Blueprint,
    current_app,
    render_template,
    request,
)

bp = Blueprint('pimpositor', __name__)


def open_db():
    return shelve.open(str(current_app.config.get('DB_PATH')))


def allowed_file(filename):
    current_app.logger.info('Checking if file is allowed...')
    return '.' in filename and filename.rsplit('.', 1)[1] in current_app.config.get(
        'ALLOWED_EXTENSIONS'
    )


def generate_and_save_uuid_to_db():
    uuid = str(uuid4())
    db = open_db()
    current_app.logger.info('Generating UUID...')
    if uuid in db:
        current_app.logger.info('UUID already exists, generating another one...')
        return generate_and_save_uuid_to_db()

    db[uuid] = {'uploaded': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    db.close()
    return uuid


def save_img(request):
    current_app.logger.info('Getting picture from POST')

    if request.files and 'picture' in request.files:

        image = request.files['picture']

        if image and allowed_file(image.filename):
            filename = image.filename
            extension = filename.split('.')[-1]
            uuid = generate_and_save_uuid_to_db()

            current_app.logger.info(
                'Saving image to disk at {0}/{1}.{2}'.format(
                    current_app.config['UPLOAD_FOLDER'], uuid, extension
                )
            )
            path = os.path.join(
                current_app.config['UPLOAD_FOLDER'], '{0}.{1}'.format(uuid, extension)
            )
            try:
                image.save(path)
            except Exception as err:
                current_app.logger.error(f'There was a problem saving the image: {err}')
                current_app.logger.error(traceback.format_exc())
                return {'status': False}

            try:
                image_size = Image.open(path).size
                width = image_size[0]
                height = image_size[1]
            except Exception as err:
                current_app.logger.error(f'There was a problem opening the image: {err}')
                current_app.logger.error(traceback.format_exc())
                return {'status': False}

            return {
                'status': True,
                'uuid': uuid,
                'extension': extension,
                'width': width,
                'height': height,
            }
        else:
            current_app.logger.info('Data does not meet requirements. Check the size.')
            return {'status': False}
    else:
        current_app.logger.info('No data was uploaded.')
        return {'status': False}


@bp.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        current_app.logger.info('Received POST')
        save_dict = save_img(request)
        saved = save_dict['status']
        if saved:
            img_url = 'static/usr_src_img/{0}.{1}'.format(
                save_dict['uuid'], save_dict['extension']
            )

            current_app.logger.info('Rendering pimpositor...')

            return render_template(
                'pimpositor.html',
                img_url=img_url,
                width=save_dict['width'],
                height=save_dict['height'],
            )
        else:
            return render_template('problem.html', request=request)
    else:
        current_app.logger.info('Serving index page...')
        return render_template('index.html')
