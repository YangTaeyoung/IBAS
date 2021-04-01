# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Answer(models.Model):
    answer_id = models.AutoField(db_column='ANSWER_ID', primary_key=True)  # Field name made lowercase.
    answer_user = models.ForeignKey('User', on_delete=models.CASCADE,
                                    db_column='ANSWER_USER')  # Field name made lowercase.
    answer_quest = models.ForeignKey('QuestForm', models.DO_NOTHING,
                                     db_column='ANSWER_QUEST')  # Field name made lowercase.
    answer_cont = models.CharField(db_column='ANSWER_CONT', max_length=5000)  # Field name made lowercase.
    answer_created = models.DateTimeField(db_column='ANSWER_CREATED', auto_now_add=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ANSWER'


class Bank(models.Model):
    bank_no = models.AutoField(db_column='BANK_NO', primary_key=True)  # Field name made lowercase.
    bank_plus = models.IntegerField(db_column='BANK_PLUS', blank=True, default=0)  # Field name made lowercase.
    bank_minus = models.IntegerField(db_column='BANK_MINUS', blank=True, default=0)  # Field name made lowercase.
    bank_title = models.CharField(db_column='BANK_TITLE', max_length=100, blank=True,
                                  null=True)  # Field name made lowercase.
    bank_used = models.DateTimeField(db_column='BANK_USED', blank=True)  # Field name made lowercase.
    bank_created = models.DateTimeField(db_column='BANK_CREATED', auto_now_add=True)  # Field name made lowercase.
    bank_updated = models.DateTimeField(db_column='BANK_UPDATED', auto_now=True, blank=True,
                                        null=True)  # Field name made lowercase.
    bank_checked = models.DateTimeField(db_column='BANK_CHECKED', null=True)
    bank_allowed = models.DateTimeField(db_column='BANK_ALLOWED', null=True)

    bank_cfo = models.ForeignKey('User', models.DO_NOTHING, db_column='BANK_CFO', null=True,
                                 related_name="cfo")  # Field name made lowercase.
    bank_used_user = models.ForeignKey('User', models.DO_NOTHING, db_column='BANK_USED_USER',
                                       related_name="used_user")  # Field name made lowercase.
    bank_apply = models.ForeignKey('BankApplyInfo', models.DO_NOTHING,
                                   db_column='BANK_APPLY')  # Field name made lowercase.
    bank_reason = models.CharField(db_column='BANK_REASON', max_length=300, blank=True,
                                   null=True)  # Field name made lowercase.
    bank_reject_reason = models.CharField(db_column='BANK_REJECT_REASON', max_length=200, blank=True,
                                          null=True)  # Field name made lowercase.
    bank_account = models.CharField(db_column='BANK_ACCOUNT', max_length=100, blank=True,
                                    null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BANK'


def bank_file_upload_to(instance, filename):
    return f'bank/{instance.bank_no.bank_no}/{filename}'


class BankFile(models.Model):
    bank_no = models.ForeignKey(Bank, on_delete=models.CASCADE, db_column='BANK_NO')  # Field name made lowercase.
    bank_file_id = models.AutoField(db_column='BANK_FILE_ID', primary_key=True)  # Field name made lowercase.
    bank_file_path = models.FileField(db_column='BANK_FILE_PATH', max_length=1000,
                                      upload_to=bank_file_upload_to)  # Field name made lowercase.
    bank_file_name = models.CharField(db_column='BANK_FILE_NAME', max_length=500)

    class Meta:
        managed = False
        db_table = 'BANK_FILE'


class BankApplyInfo(models.Model):
    bank_apply_no = models.AutoField(db_column="BANK_APPLY_NO", primary_key=True)
    bank_apply_name = models.CharField(db_column="BANK_APPLY_NAME", max_length=20)

    class Meta:
        managed = False
        db_table = "BANK_APPLY_INFO"


class Board(models.Model):
    board_no = models.AutoField(db_column='BOARD_NO', primary_key=True)  # Field name made lowercase.
    board_type_no = models.ForeignKey('BoardType', models.DO_NOTHING,
                                      db_column='BOARD_TYPE_NO')  # Field name made lowercase.
    board_title = models.CharField(db_column='BOARD_TITLE', max_length=100)  # Field name made lowercase.
    board_cont = models.CharField(db_column='BOARD_CONT', max_length=5000)  # Field name made lowercase.
    board_writer = models.ForeignKey('User', models.DO_NOTHING, db_column='BOARD_WRITER')  # Field name made lowercase.
    board_created = models.DateTimeField(db_column='BOARD_CREATED', auto_now_add=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BOARD'

    def get_board_pk(self):
        return self.board_no


# 제발... 제발.... 되라...
# 게시판 번호에 맞게 경로를 정하고 지정된 경로에 파일을 업로드 하는 함수.
def board_file_upload_to(instance, filename):
    return f'board/{instance.board_no.board_no}/{filename}'


class BoardFile(models.Model):
    board_no = models.ForeignKey(Board, on_delete=models.CASCADE, db_column='BOARD_NO',
                                 null=True)  # Field name made lowercase.
    board_file_id = models.AutoField(db_column='BOARD_FILE_ID', primary_key=True)  # Field name made lowercase.

    # 조용식이 만진 부분
    # upload_to에 대한 인자를 위에 정의한 함수로 대체해야 경로를 커스터마이징 할 수 있음.
    board_file_path = models.ImageField(db_column='BOARD_FILE_PATH', upload_to=board_file_upload_to, blank=True,
                                        null=True)  # Field name made lowercase.
    board_file_name = models.CharField(db_column='BOARD_FILE_NAME', max_length=300)

    class Meta:
        managed = False
        db_table = 'BOARD_FILE'


class BoardType(models.Model):
    board_type_no = models.AutoField(db_column='BOARD_TYPE_NO', primary_key=True)  # Field name made lowercase.
    board_type_name = models.CharField(db_column='BOARD_TYPE_NAME', max_length=50)  # Field name made lowercase.
    board_type_exp = models.CharField(db_column='BOARD_TYPE_EXP', max_length=100)

    class Meta:
        managed = False
        db_table = 'BOARD_TYPE'


class ChiefCarrier(models.Model):
    carrier_no = models.AutoField(db_column='CARRIER_NO', primary_key=True)  # Field name made lowercase.
    carrier_content = models.CharField(db_column='CARRIER_CONTENT', max_length=300, blank=True,
                                       null=True)  # Field name made lowercase.
    chief_user = models.ForeignKey('User', on_delete=models.CASCADE,
                                   db_column='CHIEF_USER')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CHIEF_CARRIER'


class Comment(models.Model):
    comment_id = models.AutoField(db_column='COMMENT_ID', primary_key=True)  # Field name made lowercase.
    comment_board_no = models.ForeignKey(Board,
                                         db_column='COMMENT_BOARD_NO',
                                         on_delete=models.CASCADE)  # Field name made lowercase.
    comment_writer = models.ForeignKey('User', models.DO_NOTHING,
                                       db_column='COMMENT_WRITER')  # Field name made lowercase.
    comment_cont = models.CharField(db_column='COMMENT_CONT', max_length=5000)  # Field name made lowercase.
    comment_cont_ref = models.ForeignKey('self', on_delete=models.CASCADE, db_column='COMMENT_CONT_REF', blank=True,
                                         null=True)  # Field name made lowercase.
    comment_created = models.DateTimeField(db_column='COMMENT_CREATED', auto_now_add=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'COMMENT'


class ContestBoard(models.Model):
    contest_no = models.AutoField(db_column='CONTEST_NO', primary_key=True)  # Field name made lowercase.
    contest_name = models.CharField(db_column='CONTEST_NAME', max_length=500)  # Field name made lowercase.
    contest_title = models.CharField(db_column='CONTEST_TITLE', max_length=100)  # Field name made lowercase.
    contest_cont = models.TextField(db_column='CONTEST_CONT')  # Field name made lowercase.
    contest_asso = models.CharField(db_column='CONTEST_ASSO', max_length=100)  # Field name made lowercase.
    contest_deadline = models.DateTimeField(db_column='CONTEST_DEADLINE')  # Field name made lowercase.
    contest_created = models.DateTimeField(db_column='CONTEST_CREATED', auto_now_add=True)  # Field name made lowercase.
    contest_writer = models.IntegerField(db_column='CONTEST_WRITER')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CONTEST_BOARD'


class ContestFile(models.Model):
    contest_file_id = models.AutoField(db_column='CONTEST_FILE_ID', primary_key=True)  # Field name made lowercase.
    contest_no = models.ForeignKey(ContestBoard, on_delete=models.CASCADE,
                                   db_column='CONTEST_NO')  # Field name made lowercase.
    contest_file_path = models.CharField(db_column='CONTEST_FILE_PATH', max_length=1000)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CONTEST_FILE'


class Lect(models.Model):
    lect_no = models.AutoField(db_column='LECT_NO', primary_key=True)  # Field name made lowercase.
    lect_title = models.CharField(db_column='LECT_TITLE', max_length=100)  # Field name made lowercase.
    lect_chief = models.ForeignKey('User', models.DO_NOTHING, db_column='LECT_CHIEF')  # Field name made lowercase.
    lect_pic = models.ImageField(db_column='LECT_PIC', max_length=1000, upload_to='lect/')  # Field name made lowercase.
    lect_type = models.ForeignKey('LectType', models.DO_NOTHING, db_column='LECT_TYPE')  # Field name made lowercase.
    lect_created = models.DateTimeField(db_column='LECT_CREATED', auto_now_add=True)  # Field name made lowercase.
    lect_intro = models.CharField(db_column='LECT_INTRO', max_length=300)  # Field name made lowercase.
    lect_state = models.ForeignKey('StateInfo', models.DO_NOTHING, db_column='LECT_STATE')  # Field name made lowercase.
    lect_curri = models.TextField(db_column='LECT_CURRI')  # Field name made lowercase.
    lect_limit_num = models.IntegerField(db_column='LECT_LIMIT_NUM')  # Field name made lowercase.
    lect_place_or_link = models.CharField(db_column='LECT_PLACE_OR_LINK', max_length=1000)  # Field name made lowercase.
    lect_method = models.ForeignKey('MethodInfo', models.DO_NOTHING,
                                    db_column='LECT_METHOD')  # Field name made lowercase.
    lect_deadline = models.DateTimeField(db_column='LECT_DEADLINE')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LECT'


class LectBoard(models.Model):
    lect_board_no = models.AutoField(db_column='LECT_BOARD_NO', primary_key=True)  # Field name made lowercase.
    lect_board_title = models.CharField(db_column='LECT_BOARD_TITLE', max_length=100)  # Field name made lowercase.
    lect_board_created = models.DateTimeField(db_column='LECT_BOARD_CREATED',
                                              auto_now_add=True)  # Field name made lowercase.
    lect_board_cont = models.TextField(db_column='LECT_BOARD_CONT')  # Field name made lowercase.
    lect_board_writer = models.ForeignKey('User', models.DO_NOTHING,
                                          db_column='LECT_BOARD_WRITER')  # Field name made lowercase.
    lect_no = models.ForeignKey(Lect, models.DO_NOTHING, db_column='LECT_NO')  # Field name made lowercase.
    lect_board_deadline = models.DateTimeField(db_column='LECT_BOARD_DEADLINE')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LECT_BOARD'


class LectBoardAnswer(models.Model):
    lect_ans_no = models.AutoField(db_column='LECT_ANS_NO', primary_key=True)  # Field name made lowercase.
    lect_board_answer = models.ForeignKey(LectBoard, models.DO_NOTHING,
                                          db_column='LECT_BOARD_ANSWER')  # Field name made lowercase.
    lect_user_stu = models.ForeignKey('User', models.DO_NOTHING,
                                      db_column='LECT_USER_STU')  # Field name made lowercase.
    lect_ans_cont = models.CharField(db_column='LECT_ANS_CONT', max_length=5000, blank=True,
                                     null=True)  # Field name made lowercase.
    lect_ans_created = models.DateTimeField(db_column='LECT_ANS_CREATED',
                                            auto_now_add=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LECT_BOARD_ANSWER'


class LectBoardAnswerFile(models.Model):
    lect_ans_file_id = models.AutoField(db_column='LECT_ANS_FILE_ID', primary_key=True)  # Field name made lowercase.
    lect_ans_no = models.ForeignKey(LectBoardAnswer, on_delete=models.CASCADE,
                                    db_column='LECT_ANS_NO')  # Field name made lowercase.
    lect_ans_file_path = models.CharField(db_column='LECT_ANS_FILE_PATH', max_length=1000)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LECT_BOARD_ANSWER_FILE'


class LectBoardComment(models.Model):
    lect_board_comment_id = models.AutoField(db_column='LECT_BOARD_COMMENT_ID',
                                             primary_key=True)  # Field name made lowercase.
    lect_board_board_no = models.ForeignKey(LectBoard, on_delete=models.CASCADE,
                                            db_column='LECT_BOARD_BOARD_NO')  # Field name made lowercase.
    lect_board_comment_cont = models.TextField(db_column='LECT_BOARD_COMMENT_CONT')  # Field name made lowercase.
    lect_board_comment_writer = models.ForeignKey('User', on_delete=models.CASCADE,
                                                  db_column='LECT_BOARD_COMMENT_WRITER')  # Field name made lowercase.
    lect_board_comment_date = models.DateTimeField(db_column='LECT_BOARD_COMMENT_DATE')  # Field name made lowercase.
    lect_board_comment_ref = models.ForeignKey('self', on_delete=models.CASCADE, db_column='LECT_BOARD_COMMENT_REF',
                                               blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LECT_BOARD_COMMENT'


class LectBoardEx(models.Model):
    lect_board_ex_no = models.AutoField(db_column='LECT_BOARD_EX_NO', primary_key=True)  # Field name made lowercase.
    lect_board_no = models.ForeignKey(LectBoard, on_delete=models.CASCADE,
                                      db_column='LECT_BOARD_NO')  # Field name made lowercase.
    lect_board_ex_content = models.TextField(db_column='LECT_BOARD_EX_CONTENT', blank=True,
                                             null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LECT_BOARD_EX'


class LectBoardExFile(models.Model):
    lect_board_ex_file_id = models.AutoField(db_column='LECT_BOARD_EX_FILE_ID',
                                             primary_key=True)  # Field name made lowercase.
    lect_board_ex_no = models.ForeignKey(LectBoardEx, on_delete=models.CASCADE,
                                         db_column='LECT_BOARD_EX_NO')  # Field name made lowercase.
    lect_board_ex_file_path = models.CharField(db_column='LECT_BOARD_EX_FILE_PATH',
                                               max_length=1000)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LECT_BOARD_EX_FILE'


class LectBoardFile(models.Model):
    lect_board_file_id = models.AutoField(db_column='LECT_BOARD_FILE_ID',
                                          primary_key=True)  # Field name made lowercase.
    lect_board_no = models.ForeignKey(LectBoard, on_delete=models.CASCADE,
                                      db_column='LECT_BOARD_NO')  # Field name made lowercase.
    lect_board_file_path = models.CharField(db_column='LECT_BOARD_FILE_PATH',
                                            max_length=1000)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LECT_BOARD_FILE'


class LectCheck(models.Model):
    check_id = models.AutoField(db_column='CHECK_ID', primary_key=True)  # Field name made lowercase.
    check_date = models.DateTimeField(db_column='CHECK_DATE')  # Field name made lowercase.
    check_lect = models.ForeignKey(Lect, models.DO_NOTHING, db_column='CHECK_LECT')  # Field name made lowercase.
    check_user = models.ForeignKey('User', models.DO_NOTHING, db_column='CHECK_USER')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LECT_CHECK'


class LectType(models.Model):
    type_no = models.AutoField(db_column='TYPE_NO', primary_key=True)  # Field name made lowercase.
    type_name = models.IntegerField(db_column='TYPE_NAME')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LECT_TYPE'


class LectUser(models.Model):
    lect_user_stu = models.AutoField(db_column='LECT_USER_STU', primary_key=True)  # Field name made lowercase.
    lect_no = models.ForeignKey(Lect, models.DO_NOTHING, db_column='LECT_NO')  # Field name made lowercase.
    lect_user = models.ForeignKey('User', models.DO_NOTHING, db_column='LECT_USER')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LECT_USER'


class MajorInfo(models.Model):
    major_no = models.AutoField(db_column='MAJOR_NO', primary_key=True)  # Field name made lowercase.
    major_colleage = models.CharField(db_column='MAJOR_COLLEAGE', max_length=10)  # Field name made lowercase.
    major_name = models.CharField(db_column='MAJOR_NAME', unique=True, max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MAJOR_INFO'


class MethodInfo(models.Model):
    method_no = models.AutoField(db_column='METHOD_NO', primary_key=True)  # Field name made lowercase.
    method_name = models.CharField(db_column='METHOD_NAME', max_length=100)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'METHOD_INFO'


class QuestForm(models.Model):
    quest_no = models.AutoField(db_column='QUEST_NO', primary_key=True)  # Field name made lowercase.
    quest_name = models.CharField(db_column='QUEST_NAME', max_length=500)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QUEST_FORM'


class StateInfo(models.Model):
    state_no = models.AutoField(db_column='STATE_NO', primary_key=True)  # Field name made lowercase.
    state_name = models.CharField(db_column='STATE_NAME', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'STATE_INFO'


def user_pic_upload_to(instance, filename): # 프로필 사진 경로 설정하는 함수
    return f'member/{instance.user_stu}/{filename}' # 저장 경로는 member/학번/경로 임.


class User(models.Model):
    user_email = models.CharField(db_column='USER_EMAIL', max_length=100)  # Field name made lowercase.
    user_stu = models.IntegerField(db_column='USER_STU', primary_key=True)  # Field name made lowercase.
    user_name = models.CharField(db_column='USER_NAME', max_length=50)  # Field name made lowercase.
    user_major = models.ForeignKey(MajorInfo, models.DO_NOTHING, db_column='USER_MAJOR')  # Field name made lowercase.
    user_pic = models.ImageField(db_column='USER_PIC', upload_to=user_pic_upload_to, blank=True,
                                 null=True)  # Field name made lowercase.
    user_auth = models.ForeignKey('UserAuth', models.DO_NOTHING, db_column='USER_AUTH')  # Field name made lowercase.
    user_role = models.ForeignKey('UserRole', models.DO_NOTHING, db_column='USER_ROLE')  # Field name made lowercase.
    user_joined = models.DateTimeField(db_column='USER_JOINED', auto_now_add=True)  # Field name made lowercase.
    user_grade = models.IntegerField(db_column='USER_GRADE')  # Field name made lowercase.
    user_gen = models.IntegerField(db_column='USER_GEN')  # Field name made lowercase.
    is_activated = models.IntegerField(db_column='IS_ACTIVATED', default=0)  # Field name made lowercase.
    user_phone = models.CharField(db_column='USER_PHONE', unique=True, max_length=15)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'USER'


class UserAuth(models.Model):
    auth_no = models.AutoField(db_column='AUTH_NO', primary_key=True)  # Field name made lowercase.
    auth_name = models.CharField(db_column='AUTH_NAME', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'USER_AUTH'


class UserDeleteFile(models.Model):
    user_delete_id = models.AutoField(db_column='USER_DELETE_ID', primary_key=True)  # Field name made lowercase.
    user_stu = models.ForeignKey(User, on_delete=models.CASCADE, db_column='USER_STU')  # Field name made lowercase.
    user_delete_file_path = models.CharField(db_column='USER_DELETE_FILE_PATH',
                                             max_length=1000)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'USER_DELETE_FILE'


class UserEmail(models.Model):
    email_no = models.AutoField(primary_key=True)
    user_email = models.CharField(max_length=100)
    user_stu = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_stu')

    class Meta:
        managed = False
        db_table = 'USER_EMAIL'


class UserRole(models.Model):
    role_no = models.AutoField(db_column='ROLE_NO', primary_key=True)  # Field name made lowercase.
    role_name = models.CharField(db_column='ROLE_NAME', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'USER_ROLE'


class History(models.Model):
    history_no = models.AutoField(db_column="HISTORY_NO", primary_key=True)
    history_cont = models.CharField(db_column="HISTORY_CONT", max_length=500)
    history_writer = models.ForeignKey(User, models.DO_NOTHING, db_column="HISTORY_WRITER")
    history_date = models.DateTimeField(db_column="HISTORY_DATE")

    class Meta:
        managed = False
        db_table = "HISTORY"


class AccountEmailaddress(models.Model):
    email = models.CharField(unique=True, max_length=254)
    verified = models.IntegerField()
    primary = models.IntegerField()
    user = models.ForeignKey('AuthUser', on_delete=models.CASCADE)

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
    username = models.CharField(unique=True, max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
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
