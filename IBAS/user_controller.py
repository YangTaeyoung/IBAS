from DB.models import User


def is_chief_there():
    return len(User.objects.filter(user_role=1)) != 0 and len(User.objects.filter(user_role=1)) != 0
