# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 NYU.
#
# Ultraviolet Permssions is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Module tests."""

from flask import Flask
import flask_security
import pytest

from conftest import create_roles, assign_roles, login_user, logout_user, create_proprietary_record
from invenio_accounts.testutils import create_test_user
# from invenio_rdm_records.tests.conftest import minimal_record

import sys
sys.path.append('/Users/kunal/dev/ultraviolet-permissions-module')
import ultraviolet_permissions.ext

def test_version():
    """Test version import."""
    from ultraviolet_permissions import __version__
    assert __version__


def test_init():
    """Test extension initialization."""
    app = Flask('testapp')
    ext = ultraviolet_permissions.ext.UltravioletPermssions(app)
    assert 'ultraviolet-permissions' in app.extensions

    app = Flask('testapp')
    ext = ultraviolet_permissions.ext.UltravioletPermssions()
    assert 'ultraviolet-permissions' not in app.extensions
    ext.init_app(app)
    assert 'ultraviolet-permissions' in app.extensions


def test_view(base_client):
    """Test view."""
    res = base_client.get("/")
    assert res.status_code == 200
    assert 'Welcome to Ultraviolet Permssions' in str(res.data)

def test_user_without_special_role(base_client):
    client = base_client
    user = create_test_user()
    recid = create_proprietary_record(client)
    login_user(client, user)
    url = f"/records/{recid}"

    # Anonymous user can't list files
    response = client.get(url, headers=headers)
    assert 403 == response.status_code

def test_anonymous(base_client):
    client = base_client
    recid = create_proprietary_record(client)
    url = f"/records/{recid}"

    # Anonymous user can't list files
    response = client.get(url, headers=headers)
    assert 403 == response.status_code

def test_user_with_special_role(base_client):
    client = base_client
    user = create_test_user()
    role = create_roles(['nyu'])
    assign_roles(user, [role])
    login_user(client, user)

    recid = create_proprietary_record(client)

    url = f"/records/{recid}"

    # Anonymous user can't list files
    response = client.get(url, headers=headers)
    assert 200 == response.status_code
