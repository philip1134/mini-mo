# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2018-02-26
#


import os
import time
import subprocess
from ..helpers import *
from ..globals import g, MINIMO_ROOT
from ..route import register
from generator import copy_template_file, copy_template_folder


@register("migration", "help.flask.migration", True, "flask")
def flask_generate_migration(args = {}):
    """generate migration script file from template"""

    if g.app.root_path is None:
        error(_("error.invalid_minimo_project_directory"))
        return

    # check migration folder for alembic
    if os.path.exists(os.path.join(os.getcwd(), "migrations")):
        for _migration in set(args["args"]):
            # create migration
            m = _migration.lower()
            info(_("info.flask.file_create"), "migration", m)
            stdout, stderr = subprocess.Popen(
                ["alembic", "revision", "-m", m],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
            ).communicate()
            info(" "*4 + stdout)
    else:
        error(_("error.invalid_alembic_env"))


@register("model", "help.flask.model", True, "flask")
def flask_generate_model(args = {}):
    """generate model file from template. it will create the related migration
    script if '--without-migration' is not set."""

    if g.app.root_path is None:
        error(_("error.invalid_minimo_project_directory"))
        return

    if not validate_keys(args, {"a": _("error.author_name_required")}):
        return

    config = {
        "author": args["a"],
        "date": time.strftime("%Y-%m-%d"),
    }

    migrations = []
    for _model in set(args["args"]):
        # create model
        _model = underscore(_model)
        config["model_name"] = camelize(_model)

        model_template_path = os.path.join(MINIMO_ROOT,
            "templates", "flask", "files", "model.py.mot")
        model_file_name = "{}.py".format(_model)
        model_dir = os.path.join(g.app.root_path, "app", "models")

        if _create_file(
            "model",
            model_dir,
            model_file_name,
            model_template_path,
            config
        ):
            migrations.append("create {}".format(_model))

    if "without-migration" not in args:
        # create migration script
        flask_generate_migration({"args": migrations})


def _create_file(
    file_type,
    target_dir,
    target_file_name,
    template_path,
    config
):
    """create file by the specified template."""
    result = False
    if os.path.exists(template_path):
        # checking target dir path
        if not os.path.exists(target_dir):
            info(_("info.flask.creating_dir"), os.path.basename(target_dir))
            os.makedirs(target_dir)

        # copy files
        info(_("info.flask.file_create"), file_type, target_file_name)
        result = copy_template_file(
            os.path.join(target_dir, target_file_name),
            template_path, config)
    else:
        warning(_("warning.flask.no_template"))

    return result


# end
