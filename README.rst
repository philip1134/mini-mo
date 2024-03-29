=======
mini-mo
=======

.. image:: https://travis-ci.com/philip1134/mini-mo.svg?branch=master
   :target: https://travis-ci.com/philip1134/mini-mo
   :alt: Build Status

.. image:: https://img.shields.io/pypi/v/minimo.svg?color=orange
   :target: https://pypi.python.org/pypi/minimo
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/minimo.svg
   :target: https://pypi.org/project/minimo/
   :alt: Supported Python versions


``minimo`` is a lightweight automation framework. mainly focuses on
automated test/task. the project name comes from the mini robot M-O in
WALL-E as the following guy:

.. image:: ./artwork/walle-mo.jpg
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
        |- log
        |- templates # case template
        |- vendor # vendor library
        |- .dockerignore
        |- .gitignore
        |- config.yml # global configuration
        |- Dockerfile # dockerfile if you want to run scheduler in docker
        |- README.md
        |- requirements.txt # dependencies here, use ``pip install -r requirements.txt`` to install all dependencies

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

Installation
~~~~~~~~~~~~

.. code:: text

    $ pip install -U minimo

Create project instance
~~~~~~~~~~~~~~~~~~~~~~~

cli
^^^

.. code:: text

    $ mmo init [project-name] [-t template-path] [-o output-path]

the project will be created under ``output-path``, default is the current
working directory if no ``output-path`` specified. minimo will initialize
the project with default template. or you can specify a path which contains
the template.

api
^^^

.. code:: python

    import minimo

    mmo = minimo.Application(
        interface="api",
        root_path="/path/to/project/instance"
    )

    # return True or False for `init` result
    result = mmo.call(
        "init",
        name="helloKitty",
        template="/path/to/my/template",
        output="./myprojects"
    )

Create new cases
~~~~~~~~~~~~~~~~

cli
^^^

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

api
^^^

.. code:: python

    import minimo

    mmo = minimo.Application(
        interface="api",
        root_path="path/to/instance_project"
    )

    # return successfully created cases list
    cases = mmo.call(
        "new",
        cases=["case1", "suite2/case1", "suite2/case2"]
    )

template file is written in mako's syntax, check out
`mako <https://www.makotemplates.org>`_.

List all standard cases
~~~~~~~~~~~~~~~~~~~~~~~

cli
^^^

.. code:: text

    $ mmo ls [pattern...]

"pattern" supports Unix shell-style wildcards, such as \* or ?. if not
specified "pattern", it will list all standard cases' names under
"cases" folder. if specified "pattern", it will search the case name by
"pattern". can give multiple patterns, such as：

.. code:: text

    $ mmo ls foo bar*

api
^^^

.. code:: python

    import minimo

    mmo = minimo.Application(
        interface="api",
        root_path="path/to/instance_project"
    )

    # return sorted valid cases
    sorted_cases = mmo.call("ls")

Run suite
~~~~~~~~~

cli
^^^

.. code:: text

    $ mmo run [case...]

can specify some cases separated by whitespace as:

.. code:: text

    $ mmo run case1 case2 case3

and also can specify some suites (case group under one folder) as:

.. code:: text

    $ mmo run suite1 suite2 suite3

minimo will run all cases under those suites.

api
^^^

.. code:: python

    import minimo

    mmo = minimo.Application(
        interface="api",
        root_path="path/to/instance_project"
    )

    # return output file path or None if all failed
    sorted_cases = mmo.call(
        "run",
        cases=["suite1", "suite2/case1", "suite2/case2"]
    )

Get help
~~~~~~~~

.. code:: text

    $ mmo --help
    $ mmo [command] --help

seems not useful in api mode

Get version
~~~~~~~~~~~

cli
^^^

.. code:: text

    $ mmo version

api
^^^

.. code:: python

    import minimo

    mmo = minimo.Application(
        interface="api",
        root_path="path/to/instance_project"
    )

    # version string
    version = mmo.call("version")

Scheduled jobs
~~~~~~~~~~~~~~~~~~~~~~~

we can run scheduled jobs in minimo project since r0.8, that is based on
APScheduler. just configure your ``scheduler`` item in ``config.yml``, minimo
will execute your scheduled jobs in blocking mode, which means run in
foreground, recommend you to run your project in a docker container. detail
information about scheduler setting please refer to
`APScheduler <https://apscheduler.readthedocs.io/>`_.

cli
^^^

.. code:: text

    $ mmo start

api
^^^

.. code:: python

    import minimo

    mmo = minimo.Application(
        interface="api",
        root_path="path/to/instance_project"
    )

    mmo.call("start")

please note that scheduler configured in case/config.yml will not work.
