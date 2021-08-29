from rest_framework import serializers
from DB.models import MajorInfo, User, UserRole, UserAuth, LectBoard, Lect, Board, Bank, UserUpdateRequest


class MajorSerializer(serializers.ModelSerializer):
    class Meta:
        model = MajorInfo
        fields = '__all__'


class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAuth
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        depth = 2


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lect
        exclude = ('lect_chief', 'lect_curri', 'lect_created', 'lect_reject_reason', 'lect_paid')
        depth = 2


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('board_title', 'board_type_no', 'board_created', 'board_no')
        depth = 2


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = ('bank_apply', 'bank_title', 'bank_no', 'bank_created', 'bank_checked', 'bank_allowed')
        depth = 2


class UserRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserUpdateRequest
        exclude = ('updated_user', )
        depth = 2

