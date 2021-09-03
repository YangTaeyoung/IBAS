# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from abc import abstractmethod
from datetime import date, timedelta
import os
from django.db import models
from datetime import datetime
from django.utils import timezone
from IBAS.settings.base import MEDIA_ROOT
import pytz
from django_summernote.fields import SummernoteTextField

CONT_SIZE = 1000000


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


class Alarm(models.Model):
    alarm_no = models.AutoField(db_column='ALARM_NO', primary_key=True)
    alarm_user = models.ForeignKey('User', on_delete=models.CASCADE, db_column='ALARM_USER')
    alarm_cont = models.CharField(db_column='ALARM_CONT', max_length=150)
    alarm_link = models.CharField(db_column='ALARM_LINK', max_length=150, null=True)
    alarm_ischecked = models.IntegerField(db_column='ALARM_ISCHECKED', default=0)
    alarm_date = models.DateTimeField(db_column='ALARM_DATE', auto_now_add=True)

    class Meta:
        managed = False
        db_table = "ALARM"


class Bank(models.Model):
    bank_no = models.AutoField(db_column='BANK_NO', primary_key=True)
    bank_plus = models.IntegerField(db_column='BANK_PLUS', blank=True)
    bank_minus = models.IntegerField(db_column='BANK_MINUS', blank=True)
    bank_title = models.CharField(db_column='BANK_TITLE', max_length=100)
    bank_used = models.DateTimeField(db_column='BANK_USED')
    bank_created = models.DateTimeField(db_column='BANK_CREATED', auto_now_add=True)
    bank_updated = models.DateTimeField(db_column='BANK_UPDATED', auto_now=True, blank=True, null=True)
    bank_checked = models.DateTimeField(db_column='BANK_CHECKED', null=True)
    bank_allowed = models.DateTimeField(db_column='BANK_ALLOWED', null=True)
    bank_cfo = models.ForeignKey('User', models.DO_NOTHING, db_column='BANK_CFO', null=True, related_name="cfo")
    bank_used_user = models.ForeignKey('User', models.DO_NOTHING, blank=True, db_column='BANK_USED_USER',
                                       related_name="used_user", null=True)
    bank_apply = models.ForeignKey('BankApplyInfo', models.DO_NOTHING, db_column='BANK_APPLY')
    bank_reason = models.CharField(db_column='BANK_REASON', max_length=300, blank=True, null=True)
    bank_reject_reason = models.CharField(db_column='BANK_REJECT_REASON', max_length=200, blank=True, null=True)
    bank_account = models.CharField(db_column='BANK_ACCOUNT', max_length=100, null=True)

    class Meta:
        managed = False
        db_table = 'BANK'

    @property
    def get_file_path(self):
        return os.path.join(MEDIA_ROOT, 'bank', str(self.bank_no))


# 추상클래스 File
class File(models.Model):
    def file_upload_to(self, filename):
        pass

    file_id = models.AutoField(db_column='FILE_ID', primary_key=True)  # Field name made lowercase.
    file_name = models.CharField(db_column='FILE_NAME', max_length=300)
    file_path = models.FileField(db_column='FILE_PATH', max_length=1000, blank=True)

    class Meta:
        abstract = True


class CommentType(models.Model):
    comment_type_no = models.AutoField(db_column="TYPE_NO", primary_key=True)
    comment_type_name = models.CharField(db_column="TYPE_NAME", max_length=20)

    class Meta:
        managed = False
        db_table = "COMMENT_TYPE"


# COMMENT 공용테이블
class Comment(models.Model):
    comment_id = models.AutoField(db_column='COMMENT_ID', primary_key=True)
    comment_writer = models.ForeignKey('User', models.DO_NOTHING, db_column='COMMENT_WRITER', blank=True)
    comment_cont = models.CharField(db_column='COMMENT_CONT', max_length=5000)
    comment_cont_ref = models.ForeignKey('self', on_delete=models.CASCADE, db_column='COMMENT_CONT_REF', blank=True,
                                         null=True, related_name="re_comments")
    comment_created = models.DateTimeField(db_column='COMMENT_CREATED', auto_now_add=True)
    comment_type = models.ForeignKey("CommentType", on_delete=models.CASCADE, db_column="COMMENT_TYPE")
    comment_board_ref = models.IntegerField(db_column="COMMENT_BOARD_REF")

    class Meta:
        managed = False
        db_table = "COMMENT"


class BankFile(File):
    def file_upload_to(self, filename):
        return os.path.join('bank', str(self.file_fk_id), filename)

    file_fk = models.ForeignKey(Bank, on_delete=models.CASCADE, db_column='BANK_NO', related_name='files')
    file_path = models.FileField(db_column='FILE_PATH', max_length=1000, upload_to=file_upload_to, blank=True)

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
    board_cont = SummernoteTextField(db_column='BOARD_CONT', max_length=CONT_SIZE)  # Field name made lowercase.
    board_writer = models.ForeignKey('User', on_delete=models.CASCADE, db_column='BOARD_WRITER')
    board_created = models.DateTimeField(db_column='BOARD_CREATED', auto_now_add=True)  # Field name made lowercase.
    board_fixdate = models.DateTimeField(db_column='BOARD_FIXDATE', null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'BOARD'

    @property
    def get_file_path(self):
        return os.path.join(MEDIA_ROOT, 'board', str(self.board_no))


class BoardFile(File):
    def file_upload_to(self, filename):
        return os.path.join('board', str(self.file_fk_id), filename)

    file_fk = models.ForeignKey(Board, on_delete=models.CASCADE, db_column='BOARD_NO', related_name='files')
    file_path = models.FileField(db_column='FILE_PATH', max_length=1000, upload_to=file_upload_to, blank=True)

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


class ContestBoard(models.Model):
    contest_no = models.AutoField(db_column='CONTEST_NO', primary_key=True)
    contest_title = models.CharField(db_column='CONTEST_TITLE', max_length=100)
    contest_cont = SummernoteTextField(db_column='CONTEST_CONT', max_length=CONT_SIZE)
    contest_writer = models.ForeignKey('User', on_delete=models.CASCADE, db_column='CONTEST_WRITER')
    contest_created = models.DateTimeField(db_column='CONTEST_CREATED', auto_now_add=True)
    contest_topic = models.CharField(db_column='CONTEST_TOPIC', max_length=500)
    contest_asso = models.CharField(db_column='CONTEST_ASSO', max_length=100)
    contest_start = models.DateTimeField(db_column='CONTEST_START')
    contest_deadline = models.DateTimeField(db_column='CONTEST_DEADLINE')

    class Meta:
        managed = False
        db_table = 'CONTEST_BOARD'

    # 템플릿 안에서 컨텍스트 객체를 통해 실행할 수 있음
    @property
    def is_past_due(self):
        today = date.today()
        if today <= self.contest_deadline.date():
            return True
        else:
            return False

    @property
    def get_file_path(self):
        return os.path.join(MEDIA_ROOT, 'contest', str(self.contest_no))


class ContestFile(File):
    def file_upload_to(self, filename):
        return os.path.join('board', 'contest', str(self.file_fk_id), filename)

    file_fk = models.ForeignKey(ContestBoard, on_delete=models.CASCADE, db_column='CONTEST_NO', related_name='files')
    file_path = models.FileField(db_column='FILE_PATH', max_length=1000, upload_to=file_upload_to, blank=True)

    class Meta:
        managed = False
        db_table = 'CONTEST_FILE'
        ordering = ['-file_path']  # 항상 게시글의 이미지를 먼저 가져오기 위함.(썸네일 관련)


class MethodInfo(models.Model):
    method_no = models.AutoField(db_column='METHOD_NO', primary_key=True)  # Field name made lowercase.
    method_name = models.CharField(db_column='METHOD_NAME', max_length=100)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'METHOD_INFO'


# 메소드 선택지를 위한 튜플  변수 생성
METHOD_CHOICES = []
for method in MethodInfo.objects.all():
    METHOD_CHOICES.append((method.method_no, method.method_name))
METHOD_CHOICES = tuple(METHOD_CHOICES)


# 강의 썸네일 사진 업로드 경로
def lect_pic_upload_to(instance, filename):
    return f'lect/pic/{instance.lect_no}/{filename}'


class Lect(models.Model):
    lect_no = models.AutoField(db_column='LECT_NO', primary_key=True)
    lect_title = models.CharField(db_column='LECT_TITLE', max_length=100)  # required
    lect_chief = models.ForeignKey('User', on_delete=models.CASCADE, db_column='LECT_CHIEF')
    lect_pic = models.ImageField(db_column='LECT_PIC', max_length=1000,
                                 upload_to=lect_pic_upload_to, null=True)  # required
    lect_type = models.ForeignKey('LectType', models.DO_NOTHING, db_column='LECT_TYPE')
    lect_created = models.DateTimeField(db_column='LECT_CREATED', auto_now_add=True)
    lect_intro = models.CharField(db_column='LECT_INTRO', max_length=300)  # required
    lect_state = models.ForeignKey('StateInfo', models.DO_NOTHING, db_column='LECT_STATE',
                                   default=1, null=True, blank=True)
    lect_curri = SummernoteTextField(db_column='LECT_CURRI', max_length=CONT_SIZE)  # required
    lect_limit_num = models.IntegerField(db_column='LECT_LIMIT_NUM', blank=True)  # required, default = 999
    lect_place_or_link = models.CharField(db_column='LECT_PLACE_OR_LINK', max_length=1000, null=True, blank=True)
    lect_method = models.ForeignKey('MethodInfo', models.DO_NOTHING, db_column='LECT_METHOD',
                                    choices=METHOD_CHOICES, null=True, blank=True)
    lect_deadline = models.DateTimeField(db_column='LECT_DEADLINE')  # required
    lect_reject_reason = models.CharField(db_column='LECT_REJECT_REASON', null=True, blank=True, max_length=200)
    lect_day = models.CharField(db_column="LECT_DAY", max_length=20)  # required
    lect_paid = models.IntegerField(db_column="LECT_PAID", null=True, blank=True, default=0)

    class Meta:
        managed = False
        db_table = 'LECT'

    @property
    def get_file_path(self):
        return os.path.join(MEDIA_ROOT, 'lect', "pic", str(self.lect_no))

    @property
    def is_expired(self):
        # 마감일을 2021.08.04 로 설정하면 db 에는 2021.08.04 00:00:00 으로 저장됨.
        # 마감일의 의미상 당일 23:59:59 까지는 가능해야함. 그래서 하루 더해줬음.
        return timezone.now() > self.lect_deadline + timedelta(days=1)

    # 등록된 학생 수를 구하는 함수.
    @property
    def get_enrolled_std_num(self):
        return len(self.enrolled_students.filter(status_id=1))



class LectAttendance(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    lect_no = models.ForeignKey('Lect', on_delete=models.CASCADE, db_column="LECT_NO", related_name='attendance')
    lect_board_no = models.ForeignKey('LectBoard', on_delete=models.CASCADE, db_column="LECT_BOARD_NO",
                                      related_name='attendance_info')  # 한 강의에 출석한 수강생들 목록
    student = models.ForeignKey('User', on_delete=models.SET_DEFAULT, db_column='STUDENT', default=0)
    lect_attend_date = models.DateTimeField(db_column='LECT_ATTEND_DATE', auto_now_add=True, null=True)

    class Meta:
        managed = False
        db_table = 'LECT_ATTENDANCE'
        unique_together = (('student', 'lect_board_no'),)


class LectAssignmentSubmit(models.Model):
    assignment_submit_no = models.AutoField(db_column="ASSIGNMENT_SUBMIT_NO", primary_key=True)
    assignment_title = models.CharField(db_column='ASSIGNMENT_TITLE', max_length=100)
    assignment_submit_created = models.DateTimeField(db_column='ASSIGNMENT_SUBMIT_CREATED', auto_now_add=True)
    assignment_cont = models.TextField(db_column='ASSIGNMENT_CONT')
    assignment_submitter = models.ForeignKey('User', on_delete=models.SET_DEFAULT, default=0,
                                             db_column='ASSIGNMENT_SUBMITTER')
    assignment_no = models.ForeignKey('LectBoard', on_delete=models.CASCADE, db_column='ASSIGNMENT_NO',
                                      related_name='submissions')
    lect_no = models.ForeignKey('Lect', on_delete=models.CASCADE, db_column='LECT_NO',
                                related_name='submitted_assignments')
    status = models.ForeignKey('LectAssignmentStatus', on_delete=models.SET_NULL, null=True, db_column="STATUS",
                               default=0)
    reject_reason = models.CharField(db_column="REJECT_REASON", max_length=200, null=True)

    class Meta:
        managed = False
        db_table = 'LECT_ASSIGNMENT_SUBMIT'

    def get_file_path(self):
        return os.path.join(MEDIA_ROOT, 'lecture', 'submitted', self.pk)


class LectAssignmentStatus(models.Model):
    status = models.IntegerField(db_column="STATUS", primary_key=True)
    description = models.CharField(db_column="DESCRIPTION", max_length=10)

    class Meta:
        managed = False
        db_table = 'LECT_ASSIGNMENT_STATUS'


class LectAssignmentSubmittedFile(File):
    def file_upload_to(self, filename):
        return os.path.join('lecture', 'submitted', str(self.file_fk_id), filename)

    file_fk = models.ForeignKey('LectAssignmentSubmit', on_delete=models.CASCADE,
                                db_column='ASSIGNMENT_SUBMIT_NO', related_name='files')
    file_path = models.FileField(db_column='FILE_PATH', upload_to=file_upload_to, max_length=1000, blank=True)

    class Meta:
        managed = False
        db_table = 'LECT_ASSIGNMENT_SUBMITTED_FILE'


class LectBoard(models.Model):
    lect_board_no = models.AutoField(db_column='LECT_BOARD_NO', primary_key=True)
    lect_board_title = models.CharField(db_column='LECT_BOARD_TITLE', max_length=100)
    lect_board_created = models.DateTimeField(db_column='LECT_BOARD_CREATED', auto_now_add=True)
    lect_board_cont = SummernoteTextField(db_column='LECT_BOARD_CONT', max_length=CONT_SIZE)
    lect_board_writer = models.ForeignKey('User', on_delete=models.CASCADE, db_column='LECT_BOARD_WRITER')
    lect_no = models.ForeignKey(Lect, on_delete=models.CASCADE, db_column='LECT_NO', related_name='lectures')
    lect_board_type = models.ForeignKey('LectBoardType', models.DO_NOTHING, db_column='LECT_BOARD_TYPE')
    lect_board_link = models.CharField(db_column='LECT_BOARD_LINK', max_length=500, null=True, blank=True)
    assignment_deadline = models.DateTimeField(db_column='LECT_ASSIGNMENT_DEADLINE', null=True)
    lect_board_ref = models.ForeignKey('LectBoard', db_column='LECT_BOARD_REF', related_name='assignments',
                                       on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'LECT_BOARD'
        ordering = ['-lect_board_created']

    @property
    def get_file_path(self):
        return os.path.join(MEDIA_ROOT, 'lecture', 'board', str(self.lect_board_no))

    @property
    def is_expired(self):
        return pytz.UTC.localize(datetime.now()) > pytz.UTC.localize(self.assignment_deadline)


class LectEnrollment(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    lect_no = models.ForeignKey('Lect', on_delete=models.CASCADE, db_column='LECT_NO', related_name='enrolled_students')
    student = models.ForeignKey('User', on_delete=models.CASCADE, db_column='STUDENT')
    status = models.ForeignKey('LectEnrollmentStatus', on_delete=models.DO_NOTHING, db_column='STATUS', default=1,
                               null=False)
    exit_time = models.DateTimeField('EXIT_TIME')

    class Meta:
        managed = False
        db_table = 'LECT_ENROLLMENT'
        unique_together = (('student', 'lect_no'),)


class LectEnrollmentStatus(models.Model):
    status = models.IntegerField(db_column='STATUS', primary_key=True)
    description = models.CharField(db_column='DESCRIPTION', max_length=10)

    class Meta:
        managed = False
        db_table = 'LECT_ENROLLMENT_STATUS'


class LectBoardType(models.Model):
    lect_board_type_no = models.AutoField(db_column='LECT_BOARD_TYPE_NO', primary_key=True)
    lect_board_type_name = models.CharField(db_column='LECT_BOARD_TYPE_NAME', max_length=20)
    lect_board_type_exp = models.CharField(db_column='LECT_BOARD_TYPE_EXP', max_length=20)

    class Meta:
        managed = False
        db_table = 'LECT_BOARD_TYPE'


class LectBoardFile(File):
    def file_upload_to(self, filename):
        return os.path.join('lecture', 'board', str(self.file_fk_id), filename)

    file_fk = models.ForeignKey('LectBoard', on_delete=models.CASCADE, db_column='LECT_BOARD_NO', related_name='files')
    file_path = models.FileField(db_column='FILE_PATH', upload_to=file_upload_to, max_length=1000, blank=True)

    class Meta:
        managed = False
        db_table = 'LECT_BOARD_FILE'


class LectMoneyStandard(models.Model):
    money_no = models.AutoField(db_column="MONEY_NO", primary_key=True)
    money_1to5 = models.IntegerField(db_column="MONEY1TO5")
    money_6to10 = models.IntegerField(db_column="MONEY6TO10")
    money_11to20 = models.IntegerField(db_column="MONEY11TO20")
    money_21over = models.IntegerField(db_column="MONEY21OVER")

    class Meta:
        managed = False
        db_table = "LECT_MONEY_STANDARD"


class LectSchedule(models.Model):
    lect_schedule_no = models.AutoField(db_column="LECT_SCHEDULE_NO", primary_key=True)
    lect_register_start = models.DateTimeField(db_column="LECT_REGISTER_START")
    lect_register_end = models.DateTimeField(db_column="LECT_REGISTER_END")

    class Meta:
        managed = False
        db_table = "LECT_SCHEDULE"


class LectType(models.Model):
    type_no = models.AutoField(db_column='TYPE_NO', primary_key=True)  # Field name made lowercase.
    type_name = models.CharField(db_column='TYPE_NAME', unique=True, max_length=20)  # Field name made lowercase.
    type_exp = models.CharField(db_column='TYPE_EXP', max_length=100)

    class Meta:
        managed = False
        db_table = 'LECT_TYPE'


class MajorInfo(models.Model):
    major_no = models.AutoField(db_column='MAJOR_NO', primary_key=True)  # Field name made lowercase.
    major_colleage = models.CharField(db_column='MAJOR_COLLEAGE', max_length=10)  # Field name made lowercase.
    major_name = models.CharField(db_column='MAJOR_NAME', unique=True, max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MAJOR_INFO'


class PolicyType(models.Model):
    type_no = models.AutoField(db_column="TYPE_NO", primary_key=True)
    type_name = models.CharField(db_column="TYPE_NAME", max_length=100)

    class Meta:
        managed = False
        db_table = "POLICY_TYPE"


class PolicyTerms(models.Model):
    policy_no = models.AutoField(db_column='POLICY_NO', primary_key=True)
    policy_title = models.CharField(db_column="POLICY_TITLE", max_length=500)
    policy_content = SummernoteTextField(db_column="POLICY_CONTENT", max_length=CONT_SIZE)
    policy_user = models.ForeignKey("User", on_delete=models.DO_NOTHING, db_column="POLICY_USER", null=True, blank=True)
    policy_type = models.ForeignKey("PolicyType", db_column="POLICY_TYPE", on_delete=models.CASCADE)
    policy_updated = models.DateTimeField(db_column="POLICY_UPDATED", auto_now=True)

    class Meta:
        managed = False
        db_table = "POLICY_TERMS"


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


def user_pic_upload_to(instance, filename):
    return f'member/{instance.user_stu}/{filename}'


class User(models.Model):
    user_stu = models.IntegerField(db_column='USER_STU', primary_key=True)
    user_name = models.CharField(db_column='USER_NAME', max_length=50)
    user_major = models.ForeignKey(MajorInfo, models.DO_NOTHING, db_column='USER_MAJOR', null=True)
    user_pic = models.ImageField(db_column='USER_PIC', upload_to=user_pic_upload_to, blank=True, null=True)
    user_auth = models.ForeignKey('UserAuth', models.DO_NOTHING, db_column='USER_AUTH', null=True)
    user_role = models.ForeignKey('UserRole', models.DO_NOTHING, db_column='USER_ROLE', null=True)
    user_joined = models.DateTimeField(db_column='USER_JOINED', auto_now_add=True)
    user_grade = models.IntegerField(db_column='USER_GRADE', null=True)
    user_gen = models.IntegerField(db_column='USER_GEN', null=True)
    user_phone = models.CharField(db_column='USER_PHONE', unique=True, max_length=15)
    user_intro = models.CharField(db_column="USER_INTRO", null=True, max_length=300)
    user_apply_publish = models.IntegerField(db_column="USER_APPLY_PUBLISH", null=True, default=0)

    class Meta:
        managed = False
        db_table = 'USER'

    @property
    def get_file_path(self):
        return os.path.join(MEDIA_ROOT, "member", str(self.user_stu))


class UserAuth(models.Model):
    auth_no = models.AutoField(db_column='AUTH_NO', primary_key=True)  # Field name made lowercase.
    auth_name = models.CharField(db_column='AUTH_NAME', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'USER_AUTH'


class UserDelete(models.Model):
    user_delete_no = models.AutoField(db_column="USER_DELETE_NO", primary_key=True)
    user_delete_title = models.CharField(db_column="USER_DELETE_TITLE", max_length=100)
    user_delete_content = SummernoteTextField(db_column="USER_DELETE_CONTENT", max_length=CONT_SIZE)
    user_delete_created = models.DateTimeField(db_column="USER_DELETE_CREATED", auto_now_add=True)
    deleted_user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='DELETED_USER',
                                     related_name="DELETED_USER")
    suggest_user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='SUGGEST_USER',
                                     related_name="SUGGEST_USER")
    user_delete_state = models.ForeignKey("UserDeleteState", on_delete=models.CASCADE, db_column="USER_DELETE_STATE")

    class Meta:
        managed = False
        db_table = 'USER_DELETE'

    @property
    def get_file_path(self):
        return os.path.join(MEDIA_ROOT, 'member', 'delete', str(self.user_delete_no))


class UserDeleteFile(File):
    def file_upload_to(self, filename):
        return os.path.join('member', 'delete', str(self.file_fk_id), filename)

    file_fk = models.ForeignKey(UserDelete, db_column="USER_DELETE_NO", on_delete=models.CASCADE, related_name='files')
    file_path = models.FileField(db_column='FILE_PATH', max_length=100,
                                 upload_to=file_upload_to)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'USER_DELETE_FILE'


class UserDeleteAor(models.Model):
    aor_no = models.AutoField(db_column="AOR_NO", primary_key=True)
    aor_user = models.ForeignKey(User, db_column="AOR_USER", on_delete=models.CASCADE)
    user_delete_no = models.ForeignKey(UserDelete, db_column="USER_DELETE_NO", on_delete=models.CASCADE)
    aor_created = models.DateTimeField(db_column="AOR_CREATED", auto_now=True)
    aor = models.IntegerField(db_column="AOR")

    class Meta:
        managed = False
        db_table = "USER_DELETE_AOR"


class UserDeleteState(models.Model):
    state_no = models.AutoField(db_column="STATE_NO", primary_key=True)
    state_name = models.CharField(db_column="STATE_NAME", unique=True, max_length=20)

    class Meta:
        managed = False
        db_table = "USER_DELETE_STATE"


class UserEmail(models.Model):
    user_email = models.CharField(max_length=100, db_column="USER_EMAIL", primary_key=True)
    provider = models.CharField(max_length=20, db_column="PROVIDER")
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


class UserSchedule(models.Model):
    user_schedule_no = models.AutoField(db_column="USER_SCHEDULE_NO", primary_key=True)
    generation = models.IntegerField(db_column="GENERATION")
    user_register_start = models.DateTimeField(db_column="USER_REGISTER_START")
    user_register_end = models.DateTimeField(db_column="USER_REGISTER_END")
    user_interview_start = models.DateTimeField(db_column="USER_INTERVIEW_START")
    user_interview_end = models.DateTimeField(db_column="USER_INTERVIEW_END")
    result_announce_date = models.DateTimeField(db_column="RESULT_ANNOUNCE_DATE")

    class Meta:
        managed = False
        db_table = "USER_SCHEDULE"


class UserUpdateRequest(models.Model):
    updated_no = models.AutoField(db_column='UPDATED_NO', primary_key=True)
    updated_user_name = models.CharField(db_column='UPDATED_USER_NAME', max_length=50)
    updated_reject_reason = models.CharField(db_column='UPDATED_REJECT_REASON', null=True, max_length=200)
    updated_user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="UPDATED_USER")
    updated_date = models.DateTimeField(db_column='UPDATED_DATE', auto_now_add=True)
    updated_state = models.ForeignKey(StateInfo, models.DO_NOTHING, db_column='UPDATED_STATE', default=1)

    class Meta:
        managed = False
        db_table = 'USER_UPDATE_REQUEST'


class History(models.Model):
    history_no = models.AutoField(db_column="HISTORY_NO", primary_key=True)
    history_title = models.CharField(db_column="HISTORY_TITLE", max_length=100)
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
