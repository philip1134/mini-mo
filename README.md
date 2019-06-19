# mini-mo

[![Build Status](https://travis-ci.org/philip1134/mini-mo.svg?branch=master)](https://travis-ci.org/philip1134/mini-mo)

`minimo` is a lightweight automation framework. mainly focused on automated test/task. the project name comes from the mini robot M-O in WALL-E as the following guy: 

![home page](./images/walle-mo.jpg "M-O")

using minimo, you can create some standardized project instances by 
`mmo init` command. it will generate project with the organized folders like:

> <b>project-root-folder-with-project-name</b><br/>
> |- <b>bin</b>      <i># minimo reserved command, don't touch it</i><br/>
> |- <b>cases</b>    <i># suite and cases here</i><br/>
> |- <b>ext</b>      <i># customized extensions, will be loaded before running commands</i><br/>
> |- <b>lib</b>      <i># customized library, put all your common code here</i><br/>
> &nbsp;&nbsp;&nbsp;&nbsp;|- app.py<br/>
> &nbsp;&nbsp;&nbsp;&nbsp;|- performer.py<br/>
> |- <b>templates</b>     <i># case template</i><br/>
> |- <b>vendor</b>        <i># third-party libraries</i><br/>
> |- config.yml           <i># project configuration</i><br/>
> |- README.md<br/>
> |- requirements.txt     <i># dependencies here, can use `pip install -r requirements.txt` to install all dependencies</i><br/>

after project created, under the project root path you can use minimo commands
to create suite/cases by `mmo new`, or run suite/cases by `mmo run`. 

minimo will create new cases from the case template which is under `templates` folder. you can customize the template. you can also customize template for each suite if you create `templates` folder under the suite root path.

currently minimo can run suite/cases in two types, which are `serial` and `concorrence`, they are easy to understand from their names. and they can be
configured in `config.yml`. the output can be configured too, currently supports `text`, `html` or `xml`.

tip: we can use `mmo` or `minimo` as the main command after v0.4.0, but in older version, it's only `minimo`.

## Usage

we can use minimo by typing command in console, or calling its apis in your own project.

### Install and update using `pip`

	$ pip install -U minimo

### Create project instance

usage in cli mode:

    $ mmo init [project-name] [-t template-name-or-path]

the project will be created under current working directory. if not
specified template, minimo will initialize the project with 'task'
template. currenty template name only supports 'task', or you can
specify a path which contains the template.

----------

usage in api mode:

```
    import minimo

    mmo = minimo.Application(
                interface="api",
                root_path=instance_project_path)

    # return True or False for `init` result
    result = mmo.main(
                    "init",
                    name="helloKitty")
```

### Create new cases

usage in cli mode:

    $ mmo new [cases...] [-a author]

for example:

    $ mmo new suite1/case1 suite2/case2 case3 [-a hellokitty]

minimo will walk through the sub-directory of task suite, if templates
exists in task suite, it initializes the case by the suite specified
templates, otherwise, by the project default templates.

if specified author name, it will be filled in the template file, or minimo
will get the current system user as the author name.

----------

usage in api mode:

```
    import minimo

    mmo = minimo.Application(
                interface="api",
                root_path=instance_project_path)

    # return successfully created cases list
    cases = mmo.main(
                "new",
                cases=["case1", "suite2/case1", "suite2/case2"])
```

template file is written in mako's syntax, check out [mako](https://www.makotemplates.org). 

### List all standard cases

usage in cli mode:

    $ mmo ls [pattern...]

"pattern" supports Unix shell-style wildcards, such as * or ?.
if not specified "pattern", it will list all standard cases' names under
"cases" folder. if specified "pattern", it will search the case name by
"pattern". can give multiple patterns, such as：

    $ mmo ls foo bar*

----------

usage in api mode:

```
    import minimo

    mmo = minimo.Application(
                interface="api",
                root_path=instance_project_path)

    # return sorted valid cases
    sorted_cases = mmo.main("ls")
```

### Run suite

usage in cli mode:

    $ mmo run [case...]

can specify some cases separated by whitespace as:

    $ mmo run case1 case2 case3

and also can specify some suites (case group under one folder) as:

    $ mmo run suite1 suite2 suite3

minimo will run all cases under those suites.

----------

usage in api mode:

```
    import minimo

    mmo = minimo.Application(
                interface="api",
                root_path=instance_project_path)

    # return output file path or None if all failed
    sorted_cases = mmo.main(
                    "run",
                    cases=["suite1", "suite2/case1", suite2/case2])
```

### Get help

	$ mmo --help
	$ mmo [command] --help

seems not useful in api mode

### Get version

usage in cli mode:

    $ mmo version

----------

usage in api mode:

```
    import minimo

    mmo = minimo.Application(
                interface="api",
                root_path=instance_project_path)

    # version string
    version = mmo.main("version")
```
