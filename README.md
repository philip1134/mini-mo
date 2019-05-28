# mini-mo

[![Build Status](https://travis-ci.org/philip1134/mini-mo.svg?branch=master)](https://travis-ci.org/philip1134/mini-mo)

`minimo` is a lightweight automation framework. mainly focused on automated test/task. the project name comes from the mini robot M-O in WALL-E as the following guy: 

![home page](./images/walle-mo.jpg "M-O")

## Usage

**Install and update using `pip`**

	$ pip install -U minimo

**Create Project instance**

	$ mmo init my-project -t TEMPLATE

`TEMPLATE` specify project template, optional, default is 'task'. If it's a path, will look for template under this path.

**Get help**

	$ mmo --help
	$ mmo [command] --help

**Get version**

	$ mmo version

