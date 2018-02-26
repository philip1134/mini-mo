# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2018-02-26
#

import os
import time
from string import Template
from .helpers import *

class Generator(object):
    """Generator for initializing mini-mo project and cases."""

    def __init__(self, arg):
        super(Generator, self).__init__()

    def generate_project(self, project_name):
        """initialize project from templates"""

        project_name = project_name.replace("-", "_")
        project_name_camelized = camelize(project_name)
        project_dir_name = underscore(project_name)
        project_dir = os.path.join(os.getcwd(), project_dir_name)
        config = {
            "project_name": project_name_camelized,
        }

        # checking target path
        if os.path.exists(project_dir):
            warning(_("warning.abort_creating_dir_for_existence"), project_dir_name)
        else:
            info(_("info.creating_dir"), project_dir_name)
            os.makedirs(project_dir)

            self._copy_template_dir(project_dir, template_dir, ".tt", config)

    def generate_cases(self, cases, author):
        """generate case from templates. it will walk through the sub-directory of task suite,
        if templates exists in task suite, it initializes the case by the suite specified templates,
        otherwise, by the project default templates."""

        info(_("info.prepare_to_create_case"))

        date = time.strftime("%Y-%m-%d")
        config = {
            "author": author,
            "date": date
        }
        for case in set(cases):
            # checking templates
            dirs = ["cases"] + case.split("/")
            template_dir = None
            while len(dirs) > 0:
                dirs.pop()
                _templatedir = os.path.join(g.app.root_path(), *(dirs + ["templates"]))
                if os.path.exists(_templatedir):
                    template_dir = _templatedir
                    break                    
                
            if template_dir is None:
                warning(_("warning.abort_creating_case_for_no_template"), case)
            else:
                # checking target path
                target = os.path.join(g.app.root_path(), "cases", case)
                if os.path.exists(target):
                    warning(_("warning.abort_creating_case_for_existence"), case)
                    continue
                else:
                    info(_("info.creating_case_dir"), case)
                    os.makedirs(target)

                info(_("info.creating_case_by_template"), \
                    template_dir.replace(self.root_path(), "%s.root"%g.app.project_name()))
                
                # copy files
                config["case_name"] = os.path.basename(case)
                self._copy_template_dir(target, template_dir, ".template", config)
                
                info(_("info.case_created"), g.app.project_name())

    @staticmethod
    def _copy_template_file(dest, src, config = {}):
        """copy template file from src to dest, replace the placeholder in template file
        by the given config keywords."""

        try: 
            with open(src, "r") as src_file:
                content = Template(src_file.read())
               
            content = content.safe_substitute(**config)
            f = open(dest, "w")
            f.write(content)
            f.close()

            info(_("info.create"), os.path.basename(dest))
        except:
            error(_("error.fail_to_create_file"), os.path.basename(dest), format_traceback())

    @staticmethod
    def _copy_template_dir(dest_dir, template_dir, template_file_afterfix, config):
        """copy template directory to dest"""
            info(_("info.creating_dir"), project_dir_name)
            os.makedirs(project_dir)

        for dirpath, dirs, files in os.walk(template_dir):
            dest_subdir = template_dir.replace(dirpath, "")
            if not os.path.exists(dirpath):
                info(_("info.creating_dir"), dest_subdir)
                os.makedirs(dirpath)

            for file in files:
                self._copy_template_file(
                    os.path.join(dest_dir, dest_subdir, file.replace(template_file_afterfix, "")), 
                    os.path.join(dirpath, file), 
                    config)
