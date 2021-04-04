# pimpositor
Simple website that pimps your pics!

Python 3.8 and beyond.

### Install

```bash
git clone git@github.com:patillacode/pimpositor.git
cd pimpositor
make install
```

### Run
`make serve`

### Use
Just go to: `http://127.0.0.1:5000/` in your browser.

------------

### Notes
* Please double check the global vars in the code (at `app/pompositor.py`)
    * DB_PATH (path to database - there is a db folder)
    * MAX_CONTENT_LENGTH (maximum picture weight - default 16MB)
    * ALLOWED_EXTENSIONS (a set, default: set(['png', 'jpg', 'jpeg', 'gif']))

------------

### Demo
* [Live demo](http://pimpositor.patilla.es/)
