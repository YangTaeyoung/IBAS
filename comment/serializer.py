from DB.models import Comment, User, MajorInfo
from rest_framework import serializers


class MajorSerializer(serializers.ModelSerializer):
    class Meta:
        model = MajorInfo
        fields = ('major_name', )


class UserSerializer(serializers.ModelSerializer):
    user_major = serializers.ReadOnlyField(source='user_major.major_name')

    class Meta:
        model = User
        fields = ('user_stu', 'user_name', 'user_pic', 'user_major')
        depth = 1


class CommentSerializer(serializers.ModelSerializer):
    comment_writer = UserSerializer()

    class Meta:
        model = Comment
        fields = ('comment_id', 'comment_writer', 'comment_cont', 'comment_created')
        depth = 1
