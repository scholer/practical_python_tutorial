from distutils.core import setup


long_description = """

Practitioneer's practical Python tutorial.



"""


# update 'version' and 'download_url', as well as qpaint_analysis.__init__.__version__
setup(
    name='practical-python-tutorial',
    description="Practitioneer's practical Python tutorial.",
    long_description=long_description,
    # long_description=open('README.txt').read(),
    version='0.1.0dev',  # Update for each new version
    packages=['practical_python'],  # List all packages (directories) to include in the source dist.
    url='https://github.com/scholer/practical_python_tutorial',
    download_url='https://github.com/scholer/practical_python_tutorial/archive/master.zip',
    author='Rasmus Scholer Sorensen',
    author_email='rasmusscholer@gmail.com',
    license='GNU General Public License v3 (GPLv3)',
    keywords=[
        "Python", "Tutorial"
    ],

    # scripts or entry points..
    # scripts=['bin/annotate_gel.py'],

    # Automatic script creation using entry points has largely super-seeded the "scripts" keyword.
    # you specify: name-of-executable-script: module[.submodule]:function
    # When the package is installed with pip, a script is automatically created (.exe for Windows).
    # Note: The entry points are stored in ./gelutils.egg-info/entry_points.txt, which is used by pkg_resources.
    entry_points={
        # 'console_scripts': [
        #     # These should all be lower-case, else you may get an error when uninstalling:
        # ],
        # 'gui_scripts': [
        # ]
    },

    install_requires=[
        'pyyaml',
        'requests',
        'pillow',
        'numpy',
        'scipy',
        'matplotlib',
    ],
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        # 'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',

        # 'Topic :: Software Development :: Build Tools',
        'Topic :: Education',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',

        'Operating System :: MacOS',
        'Operating System :: Microsoft',
        'Operating System :: POSIX :: Linux',
    ],

)
