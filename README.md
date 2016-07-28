# pimpositor
Simple website that pimps your pics!

------------

### Installation

* Clone the repo:

`git clone https://github.com/patillacode/pimpositor.git`

* Move into the repo folder:

`cd pimpositor`

* Create a virtual environment ([mkvirtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/)):

```mkvirtualenv pimpositor```

* Activate the virtualenv:
```workon pimpositor```

* Install requirements:

```pip install -r requirements.txt```

* _You are ready to execute the code!_

------------

### Usage

* Execute `python pimpositor_server.py -h` to see options available

------------

### Notes
* Please double check the global vars in the code (at `app/pompositor.py`)
    * DB_PATH (path to database - there is a db folder)
    * MAX_CONTENT_LENGTH (maximum picture weight - default 16MB)
    * UPLOAD_FOLDER (default is `app/static/usr_src_img`)
    * ALLOWED_EXTENSIONS (a set, default: set(['png', 'jpg', 'jpeg', 'gif']))

* There are missing features that will come in the future, such as:
    * Unittests
    * Automatic upload to imgur
    * Share in social media
   
------------

### Demo
* [Live demo](http://pimpositor.patilla.es/)
