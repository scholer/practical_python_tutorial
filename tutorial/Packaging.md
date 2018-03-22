



Packaging, installing and executing your modules and functions
==============================================================

This chapter was originally intended for Part 3: Beyond the basics - Features used by professional Python programmers.

However, packaging your code as a proper Python package has some advantages
that even a beginner may find useful in his day-to-day work.

If you are just starting out with Python, I would recommend skipping this chapter for now,
and return to it once you've completed the basics and maybe one or two of the Practical examples.


What are the benefits of properly packaging your Python project?
----------------------------------------------------------------

1. You can re-use your code - from anywhere.
This means that you can re-use code that you have previously written without copy/pasting it.
And generally we always want to avoid copy/pasting code as much as possible.
2. You can execute your files from anywhere.
3. You can create real programs that you can execute from anywhere.

As you may notice, "use from anywhere" is the major theme here.
Instead of creating a *script* that resides in some random folder on your computer
and is only used for one particular purpose,
you write *reusable modules* that are installed and available from anywhere,
without having to remember where the file is located on your computer.

It turns out that this makes it much more convenient when you want to use your Python code and programs.

For instance, let's say that you have a python script, `make_image_thumbnails.py`
that creates a small "thumbnail" image of all images in the current folder.
You place this script in a random folder on your computer, e.g. ``/Users/<your username>/Python-scripts/``
and when you need to make thumbnails, you execute the script with::

    $ python "/Users/<your username>/Python-scripts/make_image_thumbnails.py"

This works, but it has some disadvantages:
* You have to remember and write the full path to your script every time you need it.
This can be partially mitigated by manually adding the folder containing the script
to your ``PATH`` environment variable, but that is not sustainable in the long run,
and is almost as much work as creating a proper Python package.
* You cannot re-use the code in your script from another script.

If you create a proper Python package (e.g. ``my_code``) and install it, you could execute it as a module::

    $ python -m my_code.make_image_thumbnails

or as a proper program::

    $ make_image_thumbnails

And you can import code from your module from within another python script or module with::

    from my_code.make_image_thumbnails import resize_image  # import a function


What is needed to create a properly packaged Python project?
------------------------------------------------------------

The only thing you need is to create a file named `setup.py` in the folder where you keep your python files.
I would recommend that you then organize your python files into sub-folders, e.g.::

    /Users/<your username>/My-Python-Project/
    /Users/<your username>/My-Python-Project/setup.py
    /Users/<your username>/My-Python-Project/my_code/
    /Users/<your username>/My-Python-Project/my_code/__init__.py
    /Users/<your username>/My-Python-Project/my_code/make_image_thumbnails.py

Where lines ending with ``/`` indicates a folder. Note that ``/Users/<your username>/My-Python-Project/``
can be anything; it doesn't matter much what you call it. From now on we will just refer to this as

Blue box: Packaging nomenclature.
* We usually say that by packaging your code you are creating a proper python *package*.
* Strictly speaking, the folder containing ``setup.py`` including all files and subfolders
    are collectively called a ``distribution package``. However, this is generally only used in the context
    of distributing a distinct version (release) of your project.
* This is to distinguish this "outer" folder from the ``.../my_code/`` folder containing
    the ``__init__.py`` file, since this is also called a package (or, if distinction is needed: an *import package*).
* **Project** is thus the most appropriate nomenclature to describe the folder with the
    ``setup.py`` and all files and sub-folders, which is the reason I'm using the rather clunky
    form "properly packaged Python project" instead of simply "a Python package".
* Just be aware that "package" can be used to describe two different things,
    either the project, containing the ``setup.py`` file,
    or the sub-folder containing the ``__init__.py`` file.



Creating your ``setup.py`` file
-------------------------------

A minimal ``setup.py`` file for your project might look as follows::

    from distutils.core import setup
    setup(
        name='my-python-project',
        description="All my personal Python codes, packaged as a proper Python project.",
        long_description="",
        version='0.1.0dev',  # Update for each new version
        packages=['my_code'],  # List all packages (directories) to include in the source dist.
        author='<your name here>',
        author_email='<your email here>',
        # An executable script or .exe is automatically created for each entry point when installed:
        entry_points={
            'console_scripts': [
                # console scripts should be lower-case, else you may get an error when uninstalling:
                'make_image_thumbnails=my_code.make_image_thumbnails:main',
            ],
        },
        # List all non-standard distribution packages used in your project:
        install_requires=[
            'pyyaml',
            'requests',
            'numpy',
        ]
    )

As you can see, the


A final note for developing packaged modules in interactive mode (remember to `reload`)
---------------------------------------------------------------------------------------

If you like to work in interactive mode, e.g. using IPython or Jupyter Notebooks,
you may find yourself doing the following::

    >>> from my_code import make_image_thumbnails  # import module
    >>> make_image_thumbnails.resize_image(image)  # test if the resize_image() function works.
    # There was an error when executing resize_image(image).
    # You open make_image_thumbnails.py in your editor and fix the mistake, then execute the function again:
    >>> make_image_thumbnails.resize_image(image)
    # You get the same error as before! But you just fixed it?
    # NOTE: Modules are NOT automatically re-loaded after they have been imported.
    # Importing the make_image_thumbnails module again doesn't actually re-load it:
    >>> from my_code import make_image_thumbnails  # doesn't work, still the old version.
    # In order to actually get the updated module, you have to use the ``reload()`` function:
    from importlib import reload
    reload(make_image_thumbnails)

Note that if you have imported anything from the make_image_thumbnails module,
e.g. if you are using `resize_image()` directly, you will have to import these things again
*after* reloading the module.

It is important to note that even though you reload a module,
there may still be left-overs of the old module imported from other modules or packages.
As you create more and more modules and dependencies, you find it hard to completely reload everything,
when working in interactive mode.
As always, if you are working in interactive mode and you experience unexpected behavior,
this may easily be caused by unexpected variables still hanging around.
Whenever this happens, the best course is to simply restart the interpreter,
rather than try to debug the issue.






