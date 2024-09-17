# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 NYU.
#
# Ultraviolet Permssions is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio module that is used to define user permissions for NYUltraviolet ( NYU InvenioRDM instance)"""

from flask_babel import gettext as _

from . import config


class UltravioletPermssions(object):
    """Ultraviolet Permssions extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        # TODO: This is an example of translation string with comment. Please
        # remove it.
        # NOTE: This is a note to a translator.
        _('A translation string')
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        app.extensions['ultraviolet-permissions'] = self

    def init_config(self, app):
        """Initialize configuration."""
        # Use theme's base template if theme is installed
        for k in dir(config):
            if k.startswith('ULTRAVIOLET_PERMSSIONS_'):
                app.config.setdefault(k, getattr(config, k))
