# -*- coding: utf-8 -*-
"""WSGI middleware initialization for the mdemos.server application."""

from mdemos.server.config.app_cfg import base_config
from mdemos.server.config.environment import load_environment

from moksha.wsgi.middleware import make_moksha_middleware


__all__ = ['make_app']

# Use base_config to setup the necessary PasteDeploy application factory.
# make_base_app will wrap the TG2 app with all the middleware it needs.
make_base_app = base_config.setup_tg_wsgi_app(load_environment)


def make_app(global_conf, full_stack=True, **app_conf):
    """
    Set mdemos.server up with the settings found in the PasteDeploy
    configuration file used.

    :param global_conf: The global settings for mdemos.server (those
        defined under the ``[DEFAULT]`` section).
    :type global_conf: dict
    :param full_stack: Should the whole TG2 stack be set up?
    :type full_stack: str or bool
    :return: The mdemos.server application with all the relevant middleware
        loaded.

    This is the PasteDeploy factory for the mdemos.server application.

    ``app_conf`` contains all the application-specific settings (those defined
    under ``[app:main]``.


    """
    wrap_app = lambda app: make_moksha_middleware(app, app_conf)
    app = make_base_app(global_conf, full_stack=True,
                        wrap_app=wrap_app, **app_conf)

    # Wrap your base TurboGears 2 application with custom middleware here

    return app
