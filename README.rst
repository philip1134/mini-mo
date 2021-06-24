=======
mini-mo
=======

.. image:: https://travis-ci.org/philip1134/mini-mo.svg?branch=master
   :target: https://travis-ci.org/philip1134/mini-mo
   :alt: Build Status

.. image:: https://img.shields.io/pypi/v/minimo.svg?color=orange
   :target: https://pypi.python.org/pypi/minimo
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/minimo.svg
   :target: https://pypi.org/project/minimo/
   :alt: Supported Python versions


``minimo`` is a lightweight automation framework. mainly focused on
automated test/task. the project name comes from the mini robot M-O in
WALL-E as the following guy:

.. image:: https://github.com/philip1134/mini-mo/blob/master/artwork/walle-mo.jpg?raw=true
   :alt: M-O

using minimo, you can create some standardized project instances by
``mmo init`` command. it will generate project with the organized
folders like:

.. code:: text

    project-root-folder-with-project-name
        |- bin # minimo reserved command, don't touch it
        |- cases # suite and cases here
        |- ext # customized extensions, will be loaded before running commands
        |- lib # customized library, put all your common code here
            |- app.py
            |- performer.py
        |- templates # case template
        |- config.yml # project configuration
        |- README.md
        |- requirements.txt # dependencies here, can use ``pip install -r requirements.txt`` to install all dependencies

after project created, under the project root path you can use minimo
commands to create suite/cases by ``mmo new``, or run suite/cases by
``mmo run``.

minimo will create new cases from the case template which is under
``templates`` folder. you can customize the template. you can also
customize template for each suite if you create ``templates`` folder
under the suite root path.

currently minimo can run suite/cases in two types, which are ``serial``
and ``concorrence``, they are easy to understand from their names. and
they can be configured in ``config.yml``.

in ``concorrence`` mode, suite/cases will be run by multi-thread pool,
thread count can be configured by ``max_thread_count``.

the output can be configured too,
currently supports ``text``, ``html`` or ``xml``.

tip: we can use ``mmo`` or ``minimo`` as the main command after v0.4.0,
but in older version, it's only ``minimo``.

Usage
-----

we can use minimo by typing command in console, or calling its apis in
your own project.

Install and update using ``pip``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: text

    $ pip install -U minimo

Create project instance
~~~~~~~~~~~~~~~~~~~~~~~

usage in cli mode
^^^^^^^^^^^^^^^^^

.. code:: text

    $ mmo init [project-name] [-t template-name-or-path] [-o output-path]

the project will be created under 'output-path', if no 'output-path'
specified, that will be the current working directory. if not specified
template, minimo will initialize the project with 'task' template.
currenty template name only supports 'task', or you can specify a path
which contains the template.

usage in api mode
^^^^^^^^^^^^^^^^^

.. code:: python

    import minimo

    mmo = minimo.Application(
                interface="api",
                root_path="/path/to/project/instance")

    # return True or False for `init` result
    result = mmo.call(
                    "init",
                    name="helloKitty",
                    template="/path/to/my/template",
                    output="./myprojects")

Create new cases
~~~~~~~~~~~~~~~~

usage in cli mode
^^^^^^^^^^^^^^^^^

.. code:: text

    $ mmo new [cases...] [-a author]

for example:

.. code:: text

    $ mmo new suite1/case1 suite2/case2 case3 [-a hellokitty]

minimo will walk through the sub-directory of task suite, if templates
exists in task suite, it initializes the case by the suite specified
templates, otherwise, by the project default templates.

if specified author name, it will be filled in the template file, or
minimo will get the current system user as the author name.

usage in api mode
^^^^^^^^^^^^^^^^^

.. code:: python

    import minimo

    mmo = minimo.Application(
        interface="api",
        root_path="path/to/instance_project")

    # return successfully created cases list
    cases = mmo.call(
        "new",
        cases=["case1", "suite2/case1", "suite2/case2"])

template file is written in mako's syntax, check out
`mako <https://www.makotemplates.org>`__.

List all standard cases
~~~~~~~~~~~~~~~~~~~~~~~

usage in cli mode
^^^^^^^^^^^^^^^^^

.. code:: text

    $ mmo ls [pattern...]

"pattern" supports Unix shell-style wildcards, such as \* or ?. if not
specified "pattern", it will list all standard cases' names under
"cases" folder. if specified "pattern", it will search the case name by
"pattern". can give multiple patterns, such as：

.. code:: text

    $ mmo ls foo bar*

usage in api mode
^^^^^^^^^^^^^^^^^

.. code:: python

    import minimo

    mmo = minimo.Application(
        interface="api",
        root_path="path/to/instance_project")

    # return sorted valid cases
    sorted_cases = mmo.call("ls")

Run suite
~~~~~~~~~

usage in cli mode
^^^^^^^^^^^^^^^^^

.. code:: text

    $ mmo run [case...]

can specify some cases separated by whitespace as:

.. code:: text

    $ mmo run case1 case2 case3

and also can specify some suites (case group under one folder) as:

.. code:: text

    $ mmo run suite1 suite2 suite3

minimo will run all cases under those suites.

usage in api mode
^^^^^^^^^^^^^^^^^

.. code:: python

    import minimo

    mmo = minimo.Application(
        interface="api",
        root_path="path/to/instance_project")

    # return output file path or None if all failed
    sorted_cases = mmo.call(
        "run",
        cases=["suite1", "suite2/case1", "suite2/case2"])

Get help
~~~~~~~~

.. code:: text

    $ mmo --help
    $ mmo [command] --help

seems not useful in api mode

Get version
~~~~~~~~~~~

usage in cli mode
^^^^^^^^^^^^^^^^^

.. code:: text

    $ mmo version

usage in api mode
^^^^^^^^^^^^^^^^^

.. code:: python

    import minimo

    mmo = minimo.Application(
        interface="api",
        root_path="path/to/instance_project")

    # version string
    version = mmo.call("version")

