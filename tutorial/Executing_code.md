


Getting started: Writing and executing your code.
=================================================

Needless to say, being able to execute your Python code is fundamental to doing anything with Python.

Python is a high-level interpreted language, and that gives us a fairly high degree of flexibility in
how Python code is executed.


There are two fundamentally different ways of executing Python code:

* Single-run mode, where you write your code in a file and execute it with ``python <your-file.py>``,
* Interactive mode, where you start a long-running Python interpreter or kernel (REPL),
    and invoke your commands on an ad-hoc basis.

Each mode has its own advantages and disadvantages.

In single-run mode you basically write and execute a complete program, which may be simpler to understand.

Interactive mode, you can execute one statement at a time, see if it works or modify it if it doesn't,
and then execute the next statement.
This is really well-suited for exploring new features or looking at and analyzing data in different ways.
But interactive mode has a few pitfalls that may cause issues as your code become more complex,
or you try to reproduce your analyses or translate your code to an actual program.


Single-run mode:
----------------

All single-run modes work basically the same:
1. Open a text editor, create a new file, write some Python code, and save the file with a ``.py`` file extension.
2. Execute your `.py` file with python, e.g. from the terminal: ``$ python <your-file.py>``.
3. Modify your python file, execute again, repeat.

The main








Interactive mode:
-----------------





These *gotchas*, with old variables still hanging around, is one reason why
I recommend trying to minimize the amount of code write in interactive mode.

There are ways of minimizing issues with old variables.
The best way is to package everything up within functions,
so you don't "clutter" the outer, global namespace with lots of variable names.

A second way to minimize issues with old or conflicing variables
is to add a prefix, e.g. ``my_``, whenever you create a variable in the global namespace, e.g.::

    my_list = [0, 1, 2, 3]


