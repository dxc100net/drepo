# Generated by Django 3.1.12 on 2021-09-29 03:06

from django.conf import settings
from django.db import migrations, transaction


def migrate_duplicate_users_orgs(apps, schema_editor):
    org_member_model = apps.get_model('orgs', 'OrganizationMember')
    users_orgs_ids = set([
        (str(user_id), str(org_id))
        for user_id, org_id in org_member_model.objects.values_list('user_id', 'org_id')
    ])
    db_alias = schema_editor.connection.alias

    with transaction.atomic():
        org_member_model.objects.using(db_alias).all().delete()
        orgs_members = [
            org_member_model(user_id=user_id, org_id=org_id, role='User')
            for user_id, org_id in users_orgs_ids
        ]
        org_member_model.objects.using(db_alias).bulk_create(orgs_members)


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orgs', '0010_auto_20210219_1241'),
    ]

    operations = [
        migrations.RunPython(migrate_duplicate_users_orgs),
        migrations.AlterUniqueTogether(
            name='organizationmember',
            unique_together={('org', 'user')},
        )
    ]