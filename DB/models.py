# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class QuestForm(models.Model):
    quest_no = models.AutoField(db_column='QUEST_NO', primary_key=True)  # Field name made lowercase.
    quest_name = models.CharField(db_column='QUEST_NAME', max_length=500)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QUEST_FORM'


class User(models.Model):
    user_email = models.CharField(db_column='USER_EMAIL', max_length=100)  # Field name made lowercase.
    user_token = models.CharField(db_column='USER_TOKEN', max_length=1000)  # Field name made lowercase.
    user_stu = models.IntegerField(db_column='USER_STU', primary_key=True)  # Field name made lowercase.
    user_name = models.CharField(db_column='USER_NAME', max_length=50)  # Field name made lowercase.
    user_major = models.CharField(db_column='USER_MAJOR', max_length=50)  # Field name made lowercase.
    user_pic = models.CharField(db_column='USER_PIC', max_length=1000)  # Field name made lowercase.
    user_auth = models.IntegerField(db_column='USER_AUTH')  # Field name made lowercase.
    user_role = models.IntegerField(db_column='USER_ROLE')  # Field name made lowercase.
    user_joined = models.DateTimeField(db_column='USER_JOINED', blank=True, null=True)  # Field name made lowercase.
    user_grade = models.IntegerField(db_column='USER_GRADE')  # Field name made lowercase.
    user_gen = models.IntegerField(db_column='USER_GEN')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'USER'


class UserAuth(models.Model):
    auth_no = models.AutoField(db_column='AUTH_NO', primary_key=True)  # Field name made lowercase.
    auth_name = models.CharField(db_column='AUTH_NAME', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'USER_AUTH'


class UserRole(models.Model):
    role_no = models.AutoField(db_column='ROLE_NO', primary_key=True)  # Field name made lowercase.
    role_name = models.CharField(db_column='ROLE_NAME', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'USER_ROLE'


class AccountEmailaddress(models.Model):
    email = models.CharField(unique=True, max_length=254)
    verified = models.IntegerField()
    primary = models.IntegerField()
    user = models.ForeignKey('AuthUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account_emailaddress'


class AccountEmailconfirmation(models.Model):
    created = models.DateTimeField()
    sent = models.DateTimeField(blank=True, null=True)
    key = models.CharField(unique=True, max_length=64)
    email_address = models.ForeignKey(AccountEmailaddress, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account_emailconfirmation'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class DjangoSite(models.Model):
    domain = models.CharField(unique=True, max_length=100)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'django_site'


class SocialLoginBlog(models.Model):
    text = models.TextField()

    class Meta:
        managed = False
        db_table = 'social_login_blog'


class SocialaccountSocialaccount(models.Model):
    provider = models.CharField(max_length=30)
    uid = models.CharField(max_length=191)
    last_login = models.DateTimeField()
    date_joined = models.DateTimeField()
    extra_data = models.TextField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'socialaccount_socialaccount'
        unique_together = (('provider', 'uid'),)


class SocialaccountSocialapp(models.Model):
    provider = models.CharField(max_length=30)
    name = models.CharField(max_length=40)
    client_id = models.CharField(max_length=191)
    secret = models.CharField(max_length=191)
    key = models.CharField(max_length=191)

    class Meta:
        managed = False
        db_table = 'socialaccount_socialapp'


class SocialaccountSocialappSites(models.Model):
    socialapp = models.ForeignKey(SocialaccountSocialapp, models.DO_NOTHING)
    site = models.ForeignKey(DjangoSite, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'socialaccount_socialapp_sites'
        unique_together = (('socialapp', 'site'),)


class SocialaccountSocialtoken(models.Model):
    token = models.TextField()
    token_secret = models.TextField()
    expires_at = models.DateTimeField(blank=True, null=True)
    account = models.ForeignKey(SocialaccountSocialaccount, models.DO_NOTHING)
    app = models.ForeignKey(SocialaccountSocialapp, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'socialaccount_socialtoken'
        unique_together = (('app', 'account'),)


class Test(models.Model):
    test_no = models.AutoField(primary_key=True)
    test_name = models.TextField()

    class Meta:
        managed = False
        db_table = 'test'
