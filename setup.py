from setuptools import setup, find_packages

setup(
    name='pimpositor',
    version='0.1.0',
    description='',
    license='GPLv2',
    include_package_data=True,
    packages=find_packages(),
    author='patillacode',
    author_email='patillacode@gmail.com',
    url='https://github.com/patillacode/pimpositor',
    install_requires=['Flask', 'nodeenv', 'Pillow'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU General Public License v2',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7']
)
