# mini-mo

[![Build Status](https://travis-ci.org/philip1134/mini-mo.svg?branch=master)](https://travis-ci.org/philip1134/mini-mo)

minimo 是一款轻量级的研发效率支持框架，主要功能包括支持标准化开发的脚手架、测试/任务自动化框架等。
项目名称来源于 《机器人总动员》 中的角色小 _M-O_ 机器人，就是下图那货。

![home page](./images/walle-mo.jpg "M-O")

## 用法 Usage

使用 `setup.py` 安装:

	$ pip install minimo

**创建项目:**

	$ minimo init my-project -t TEMPLATE -s ABBREVIATION

`TEMPLATE` 指定项目模板。 如果 `TEMPLATE` 为模板名称，则会在 `minimo` 的模板目录查找对应的项目模板；
如果为目录地址，则根据该地址提供的项目模板创建项目。
目前支持的模板有：
    flask - 以 python flask 框架为基础的 web 应用项目
    task - 以 minimo 原生任务功能库为基础的项目，一般应用于自动化测试等任务执行类项目

**获取帮助:**

	$ minimo help

在不同的 minimo 项目实例中，help命令还会显示该项目实例专用的帮助信息。

**版本信息:**

	$ minimo version

### flask 脚手架

**创建数据库迁移脚本:**

	$ minimo migration migration_script_name

在 `flask` 项目的 `migrations` 目录下通过 `alembic` 创建 `[timestamp]_migration_script_name.py`

**创建 model:**

	$ minimo model ModelName -a AuthorName

在 `flask` 项目的 `app/models` 目录下创建 `model_name.py`，并在 `migrations` 下通过 `alembic` 创建 `[timestamp]_create_model_name.py` 数据库迁移文件。
如果使用了 `--without-migration` 选项，则不会创建数据库迁移文件。

### 测试/任务自动化

**创建任务用例:**

	$ minimo new TASK_SUITE/TASK_CASE -a AUTHOR

根据项目用例模板初始化用例代码，代码被创建在 `project.root/cases/TASK_SUITE/TASK_CASE`
如果 `TASK_SUITE` 目录下有用例模板，则优先使用该模板创建。
自定义的模板文件请在文件名末尾添加 `.template` 。

`-a AUTHOR` 指定作者名，必填。

**run task case:**

	$ minimo run TASK_SUITE/TASK_CASE

指定task的格式可以是 '用例集' 或者 '用例集/用例名称'。 例如: `my_tasksuite` 或 `my_tasksuite/my_taskcase`，如果指定任务集名称，则执行该项目下的所有任务用例。
如果指定用例名称，则执行指定的任务用例。

这两种方式可以一起使用，例如：

	$ minimo run my-task-suite1 my-task-suite2/case1 my-task-suite3/case3"

## 功能拓展 Extensions

在 minimo 的项目实例中，可以自定义 `sub-commands` 来实现功能的拓展。

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

