# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CERN.
# Copyright (C) 2019 Northwestern University.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Permissions for UltravioLet  Records. Mostly similar to InvenioRDM but adds policy for Proprietary records"""
from flask import current_app
from flask_principal import Permission, RoleNeed
from invenio_records_permissions.generators import AnyUser, \
    AuthenticatedUser, Disable, SystemProcess
from invenio_rdm_records.services.permissions import RDMRecordPermissionPolicy
from invenio_rdm_records.services.generators import RecordOwners, SecretLinks, RecordCommunitiesAction
from .generators import ProprietaryRecordPermissions, AdminSuperUser, Curator, Depositor, Viewer, RestrictedDataUser, PublicViewer, IfRestricted
from invenio_communities.permissions import CommunityPermissionPolicy


class UltraVioletPermissionPolicy(RDMRecordPermissionPolicy):
    """Access control configuration for records.

    Note that even if the array is empty, the invenio_access Permission class
    always adds the ``superuser-access``, so admins will always be allowed.
    """

    NEED_LABEL_TO_ACTION = {
        'bucket-update': 'update_files',
        'bucket-read': 'read_files',
        'object-read': 'read_files',
    }

    #
    # High-level permissions (used by low-level)
    #
    can_manage = [SystemProcess(), AdminSuperUser(), Depositor()]
    can_curate = can_manage + [SecretLinks("edit"), Curator()]
    can_preview = can_manage + [SecretLinks("preview"), Curator()]
    can_view = can_manage + [SecretLinks("view"), ProprietaryRecordPermissions(), RecordCommunitiesAction("view")]

    can_authenticated = [AuthenticatedUser(), SystemProcess()]
    can_all = [AnyUser(), SystemProcess(), PublicViewer()]

    #
    #  Records
    #
    # Allow submitting new record
    can_create = can_manage

    #
    # Drafts
    #
    # Allow ability to search drafts
    can_search_drafts = can_authenticated
    # Allow reading metadata of a draft
    can_read_draft = can_preview
    # Allow reading files of a draft
    can_draft_read_files = can_preview
    # Allow updating metadata of a draft
    can_update_draft = can_curate
    # Allow uploading, updating and deleting files in drafts
    can_draft_create_files = can_curate
    can_draft_update_files = can_curate
    can_draft_delete_files = can_curate

    #
    # PIDs
    #
    can_pid_reserve = can_curate
    can_pid_delete = can_curate

    #
    # Actions
    #
    # Allow to put a record in edit mode (create a draft from record)
    can_edit = can_curate
    # Allow deleting/discarding a draft and all associated files
    can_delete_draft = can_curate
    # Allow creating a new version of an existing published record.
    can_new_version = can_curate
    # Allow publishing a new record or changes to an existing record.
    can_publish = can_curate
    # Allow lifting a record or draft.
    can_lift_embargo = can_manage
    # Allow deleting of records by admins
    can_delete = can_manage
    can_delete_files = can_manage

    #
    # Disabled actions (these should not be used or changed)
    #
    can_update = [Disable()]
    can_create_files = [Disable()]
    can_update_files = [Disable()]




class NYURecordPermissionPolicy(RDMRecordPermissionPolicy):
    """Access Control Configurations for records restricted to NYU"""

    NEED_LABEL_TO_ACTION = {
        'bucket-update': 'update_files',
        'bucket-read': 'read_files',
        'object-read': 'read_files',
    }

    #
    # High-level permissions (used by low-level)
    #
    can_manage = [RecordOwners(), SystemProcess(), AdminSuperUser()]
    can_curate = can_manage + [SecretLinks("edit"), Curator()]
    can_preview = can_manage + [SecretLinks("preview"), Viewer(), Depositor()]
    can_view = can_manage + [SecretLinks("view"), Viewer(), Depositor()]

    can_authenticated = [AuthenticatedUser(), SystemProcess()]
    can_all = [AnyUser(), SystemProcess()]

    #
    #  Records
    #
    # Allow searching of records
    can_search = can_all
    # Allow reading metadata of a record
    can_read = [IfRestricted('record', then_=can_view, else_=can_all)]
    # Allow reading the files of a record
    can_read_files = [IfRestricted('files', then_=can_view, else_=can_all)]
    # Allow submitting new record
    can_create = can_authenticated + [Depositor()]

    #
    # Drafts
    #
    # Allow ability to search drafts
    can_search_drafts = can_authenticated + [Depositor()]
    # Allow reading metadata of a draft
    can_read_draft = can_preview
    # Allow reading files of a draft
    can_draft_read_files = can_preview
    # Allow updating metadata of a draft
    can_update_draft = can_curate
    # Allow uploading, updating and deleting files in drafts
    can_draft_create_files = can_curate
    can_draft_update_files = can_curate
    can_draft_delete_files = can_curate

    #
    # PIDs
    #
    can_pid_reserve = can_curate
    can_pid_delete = can_curate

    #
    # Actions
    #
    # Allow to put a record in edit mode (create a draft from record)
    can_edit = can_curate
    # Allow deleting/discarding a draft and all associated files
    can_delete_draft = can_curate
    # Allow creating a new version of an existing published record.
    can_new_version = can_curate
    # Allow publishing a new record or changes to an existing record.
    can_publish = can_curate
    # Allow lifting a record or draft.
    can_lift_embargo = can_manage

    #
    # Disabled actions (these should not be used or changed)
    #
    # - Records/files are updated/deleted via drafts so we don't support
    #   using below actions.
    can_update = [Disable()]
    can_delete = [Disable()]
    can_create_files = [Disable()]
    can_update_files = [Disable()]
    can_delete_files = [Disable()]



class DataUseRecordPermissionPolicy(RDMRecordPermissionPolicy):
    """Access Control Configurations for records for which user has agreed the terms of use"""

    NEED_LABEL_TO_ACTION = {
        'bucket-update': 'update_files',
        'bucket-read': 'read_files',
        'object-read': 'read_files',
    }

    #
    # High-level permissions (used by low-level)
    #
    can_manage = [RecordOwners(), SystemProcess(), AdminSuperUser()]
    can_curate = can_manage + [SecretLinks("edit"), Curator()]
    can_preview = can_manage + [SecretLinks("preview"), RestrictedDataUser()]
    can_view = can_manage + [SecretLinks("view"), RestrictedDataUser()]

    can_authenticated = [AuthenticatedUser(), SystemProcess()]
    can_all = [AnyUser(), SystemProcess()]

    #
    #  Records
    #
    # Allow searching of records
    can_search = can_all
    # Allow reading metadata of a record
    can_read = [IfRestricted('record', then_=can_view, else_=can_all)]
    # Allow reading the files of a record
    can_read_files = [IfRestricted('files', then_=can_view, else_=can_all)]
    # Allow submitting new record
    can_create = can_authenticated

    #
    # Drafts
    #
    # Allow ability to search drafts
    can_search_drafts = can_authenticated
    # Allow reading metadata of a draft
    can_read_draft = can_preview
    # Allow reading files of a draft
    can_draft_read_files = can_preview
    # Allow updating metadata of a draft
    can_update_draft = can_curate
    # Allow uploading, updating and deleting files in drafts
    can_draft_create_files = can_curate
    can_draft_update_files = can_curate
    can_draft_delete_files = can_curate

    #
    # PIDs
    #
    can_pid_reserve = can_curate
    can_pid_delete = can_curate

    #
    # Actions
    #
    # Allow to put a record in edit mode (create a draft from record)
    can_edit = can_curate
    # Allow deleting/discarding a draft and all associated files
    can_delete_draft = can_curate
    # Allow creating a new version of an existing published record.
    can_new_version = can_curate
    # Allow publishing a new record or changes to an existing record.
    can_publish = can_curate
    # Allow lifting a record or draft.
    can_lift_embargo = can_manage

    #
    # Disabled actions (these should not be used or changed)
    #
    # - Records/files are updated/deleted via drafts so we don't support
    #   using below actions.
    can_update = [Disable()]
    can_delete = [Disable()]
    can_create_files = [Disable()]
    can_update_files = [Disable()]
    can_delete_files = [Disable()]


def ultraviolet_admin_permission_factory(admin_view):
    return Permission(RoleNeed(current_app.config["ADMIN_ROLE"]))


class UVCommunitiesPermissionPolicy(CommunityPermissionPolicy):
    """Communities permission policy of NYU Ultraviolet."""

    # for now, we want to restrict the creation of communities to admins
    # and disable write operations if the system is in read-only mode
    #
    # current state: invenio-communities v3.1.0
    #
    # TODO: discuss who should have permissions to create communities
    #       -> new role?
    can_create = [SystemProcess(), AdminSuperUser()]
