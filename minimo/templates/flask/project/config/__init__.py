# -*- coding:utf-8 -*-


from .initializer import app, db, logger, config
from .routes import register_routes

register_routes(app)
