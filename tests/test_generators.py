import pytest
from invenio_access.models import RoleNeed
from invenio_access.permissions import authenticated_user, superuser_access, any_user
from invenio_files_rest.models import Bucket, Location, ObjectVersion
from io import BytesIO

import sys
sys.path.append("../ultraviolet_permissions")
from ultraviolet_permissions.generators import (
    AdminSuperUser,
    Depositor,
    Viewer,
    RestrictedDataUser,
    PublicViewer,
    Curator,
    IfSuppressedFile,
)


def test_admin_superuser():
    generator = AdminSuperUser()

    assert generator.needs() == [superuser_access]

@pytest.mark.parametrize("user_role", ["depositor"], indirect=True)
def test_depositor(user_roles_propriatery_record, propriatery_record):
    generator = Depositor()
    record = user_roles_propriatery_record
    other_record = propriatery_record

    assert generator.needs(record=record) == [RoleNeed("depositor")]
    assert generator.needs(record=other_record) == []


@pytest.mark.parametrize("user_role", ["viewer"], indirect=True)
def test_viewer(user_roles_propriatery_record, propriatery_record):
    generator = Viewer()
    record = user_roles_propriatery_record
    other_record = propriatery_record

    assert generator.needs(record=record) == [RoleNeed("viewer")]
    assert generator.needs(record=other_record) == []


@pytest.mark.parametrize("user_role", ["restricted_data_user"], indirect=True)
def test_restricted_data_user(user_roles_propriatery_record, propriatery_record):
    generator = RestrictedDataUser()
    record = user_roles_propriatery_record
    other_record = propriatery_record

    assert generator.needs(record=record) == [RoleNeed("restricted_data_user")]
    assert generator.needs(record=other_record) == []


@pytest.mark.parametrize("user_role", ["public_viewer"], indirect=True)
def test_public_viewer(user_roles_propriatery_record, propriatery_record):
    generator = PublicViewer()
    record = user_roles_propriatery_record
    other_record = propriatery_record

    assert generator.needs(record=record) == [RoleNeed("public_viewer")]
    assert generator.needs(record=other_record) == []


@pytest.mark.parametrize("user_role", ["curator"], indirect=True)
def test_curator(user_roles_propriatery_record, propriatery_record):
    generator = Curator()
    record = user_roles_propriatery_record
    other_record = propriatery_record

    assert generator.needs(record=record) == [RoleNeed("curator")]
    assert generator.needs(record=other_record) == []


def test_suppressed(db, bucket_from_dir, create_real_record, location):
    generator = IfSuppressedFile()

    suppressed_location = Location.get_by_name("suppressed")

    assert suppressed_location

    suppressed_bucket = Bucket.create(suppressed_location)
    ObjectVersion.create(
        suppressed_bucket, key="suppressed.txt", stream=BytesIO(b"suppressed")
    )
    record = create_real_record(bucket=suppressed_bucket)

    assert generator._condition(record) == True

    bucket = Bucket.create(location)
    ObjectVersion.create(bucket, key="public.txt", stream=BytesIO(b"public"))
    record = create_real_record(bucket=bucket)

    assert generator._condition(record) == False
