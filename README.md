# mini-mo

[![Build Status](https://travis-ci.org/philip1134/mini-mo.svg?branch=master)](https://travis-ci.org/philip1134/mini-mo)

minimo 是一款轻量级的自动化框架，主要支持测试自动化，但并不限于测试。 
项目名称来源于 《机器人总动员》 中的角色小 _M-O_ 机器人，就是下图那货。

minimo is a lightweight automation framework. mainly focused on automated test, but not limited to test.
the project name comes from the mini robot _M-O_ in _WALL-E_ as the following guy:

![home page](./images/walle-mo.jpg "M-O")

## 用法 Usage
install using setup.py:

	# download the package
	$ python setup.py install

**create project instance:**

	$ minimo init my-project -t TEMPLATE

`TEMPLATE` 指定项目模板，可选。 可以是 minimo 的模板名称，目前只有 `default`。
也可以是一个存放自定义模板的目录，minimo 将按照该目录的样纸创建项目。 

`TEMPLATE` specify the project template, it's optional.
it can be a template name, minimo will search the name under minimo/templates and create project as it, currently only `default`.
or, it can be a directory path, minimo will check out that path and create project as it.

**create task case:**

	$ minimo new TASK_SUITE/TASK_CASE -a AUTHOR

根据项目用例模板初始化用例代码，代码被创建在 `project.root/cases/TASK_SUITE/TASK_CASE` 
如果 `TASK_SUITE` 目录下有用例模板，则优先使用该模板创建。
自定义的模板文件请在文件名末尾添加 `.template` 。

`-a AUTHOR` 指定作者名，必填。

create new task case by project case-template, case code will be placed under `project.root/cases/TASK_SUITE/TASK_CASE`
if there's suite specified case-template under `TASK_SUITE` helpdirectory，minimo will prefer to use it to create case.

`-a AUTHOR` specify the author name, it's required.

**run task case:**

	$ minimo run TASK_SUITE/TASK_CASE

指定task的格式可以是 '用例集' 或者 '用例集/用例名称'。 例如: `my_tasksuite` 或 `my_tasksuite/my_taskcase`，如果指定任务集名称，则执行该项目下的所有任务用例。
如果指定用例名称，则执行指定的任务用例。

这两种方式可以一起使用，例如：

	$ minimo run my-task-suite1 my-task-suite2/case1 my-task-suite3/case3"

we can perform the whole task-suite or a single task-case (or some task-cases). such as: `my_tasksuite` or `my_tasksuite/my_taskcase`. 
if task suite is specified, all the cases under that suite will be performed.

the two types can be mixed, such as:

	$ minimo run my-task-suite1 my-task-suite2/case1 my-task-suite3/case3"

**get help:**

	$ minimo 

## 功能拓展 Extensions
在 minimo 的项目实例中，可以自定义 sub-commands 来实现功能的拓展。

将拓展的功能代码放置在 `ext` 目录下，例如 `hellokitty.py`，并在该 package 的 `__init__.py` 文件中 `import`，如下：

	# in hellokitty.py
	from minimo import register

	@register("sub-cmd-name", "help string")
	def my_cmd_handler(args = {}):
		# ...

	# in __init__.py
	from .hellokitty import xxx

这样就可以使用 `minimo sub-cmd-name ...` 的方式调用这个功能。 同时，在 `minimo help` 显示的帮助信息中，将会加入你为该子命令添加的 `help string`

## 标准化 Standardization
项目标准化是 minimo 希望辅助的一个方向，标准化的目的，不是为了扼杀个性，而是为了保持队型，降低项目的学习和维护成本。
minimo 对标准化的支持目前主要表现在基于模板创建项目实例，和基于模板创建用例。 在这一方面 minimo 还有很多的工作需要做。

the purpose of standardization is not "kill personality", but for "one team one style".