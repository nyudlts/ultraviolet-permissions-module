# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
# Copyright (C) 2021 CERN.
# Copyright (C) 2021 TU Wien.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.
#
#

"""UltraViolet Permissions Generators."""
from elasticsearch_dsl import Q
from invenio_access.permissions import authenticated_user, superuser_access, any_user
from invenio_access.models import  RoleNeed
from invenio_records_permissions.generators import Generator


def get_roles(record, user_role):
    roles = []
    additional_descriptions = record.get("metadata").get("additional_descriptions", [])
    for index, description in enumerate(additional_descriptions, start = 0):
        if description.get("type").get("id") == "technical-info":
            role = description.get("description")
            if "<p>" in role:
                    role = role.replace("<p>", "")

            if "</p>" in role:
                role = role.replace("</p>", "")
            if role.lower() == user_role:
                roles.append(role)
    return roles 


class ProprietaryRecordPermissions(Generator):
    """ProprietaryRecordPermissions

    Allows users who were granted  a specific role to view additional records
    Main use case are records which should be only available to NYU community
    Another use case are records that only can be accessed by users who met special conditions.
    In second case record curators check the condition outside Ultraviolet and then assign the
    user to a special role.
    InvenioRDM data model does not allow to add role to the access section of the record ( See https://inveniordm.docs.cern.ch/reference/metadata/)
    As a proof of concept solution we use additional_descriptions field where value will be equal to "role" and type will be equal
    to "Technical Info". Hopefully InvenioRDM will modify their data model and we won't have to use this model in production
    We expect that even users who do not have access to the records will be able to see them in the search so query filter is set to any_user
    """

    def needs(self, record=None, **kwargs):
        """Enabling Needs."""
        if record is None:
            # 'record is None' means that this must be a 'create'
            # this should be allowed for any authenticated user
            return [authenticated_user]

        additional_descriptions = record.get("metadata").get("additional_descriptions", [])
        for index, description in enumerate(additional_descriptions, start = 0):
            if description.get("type") == "technical-info":
                role = description.get("description")
                if "<p>" in role:
                    role = role.replace("<p>", "")

                if "</p>" in role:
                    role = role.replace("</p>", "")
                return [RoleNeed(role.name)]
        return []

    def query_filter(self, **kwargs):
        """Match all in search."""
        return Q('can_all')


class AdminSuperUser(Generator):
    """Allows admin superusers"""

    def __init__(self):
        """Constructor."""
        super(AdminSuperUser, self).__init__()

    def needs(self, **kwargs):
        """Enabling Needs."""
        return [superuser_access]

    def query_filter(self, identity=None, **kwargs):
        """Filters for current identity as super user."""
        if superuser_access in identity.provides:
            return Q('match_all')
        else:
            return []


class Depositor(Generator):
    """Allow NYU Depositors"""

    def __init__(self):
        """Constructor."""
        super(Depositor, self).__init__()

    def needs(self, record=None, **kwargs):
        """Enabling Needs."""
        roles = get_roles(record, "depositor")
        if len(roles) == 0:
            return []
        return [RoleNeed(role) for role in roles]


class Viewer(Generator):
    """Allow NYU Viewers for files restricted to NYU"""

    def __init__(self):
        """Constructor."""
        super(Viewer, self).__init__()

    def needs(self, record=None, **kwargs):
        """Enabling Needs."""
        roles = get_roles(record, "viewer")
        if len(roles) == 0:
            return []
        return [RoleNeed(role) for role in roles]


class RestrictedDataUser(Generator):
    """Allow user who has agreed to terms of data use"""

    def __init__(self):
        """Constructor."""
        super(RestrictedDataUser, self).__init__()

    def needs(self, record=None, **kwargs):
        """Enabling Needs."""
        roles = get_roles(record, "restricted_data_user")
        if len(roles) == 0:
            return []
        return [RoleNeed(role) for role in roles]


class PublicViewer(Generator):
    """Allow Public Viewer for any files that are open"""

    def __init__(self):
        """Constructor."""
        super(PublicViewer, self).__init__()

    def needs(self, record=None, **kwargs):
        """Enabling Needs."""
        roles = get_roles(record, "public_viewer")
        if len(roles) == 0:
            return []
        return [RoleNeed(role) for role in roles]


class Curator(Generator):
    """Allow Curator"""

    def __init__(self):
        """Constructor."""
        super(Curator, self).__init__()

    def needs(self, record=None, **kwargs):
        """Enabling Needs."""
        roles = get_roles(record, "curator")
        if len(roles) == 0:
            return []
        return [RoleNeed(role) for role in roles]


class IfRestricted(Generator):
    """IfRestricted.
    IfRestricted(
    ‘metadata’,
    RecordPermissionLevel(‘view’),
    ActionNeed(superuser-access),
    )
    A record permission level defines an aggregated set of
    low-level permissions,
    that grants increasing level of permissions to a record.
    """

    def __init__(self, field, then_, else_):
        """Constructor."""
        self.field = field
        self.then_ = then_
        self.else_ = else_

    def needs(self, record=None, **kwargs):
        """Enabling Needs."""
        if not record:
            return []

        is_field_restricted = (
            record and
            record.get('access', {}).get(self.field, "restricted")
        )

        if is_field_restricted == "restricted":
            return getattr(self.then_[0], 'needs')()
        else:
            return getattr(self.else_[0], 'needs')()

        return []

    def query_filter(self, **kwargs):
        """Filters for current identity as super user."""
        # TODO: Implement with new permissions metadata
        return Q('match_all')