# from chat import models
from chat import models
from django.contrib.auth.models import User


def check_registration(request):
    password_error = False
    username_error = False
    username_exist_error = False
    firstName_error = False
    lastName_error = False

    if request.POST["username"] == "":
        username_exist_error = True
    if User.objects.filter(username=request.POST["username"]).exists():
        username_error = True
    if request.POST["firstName"] == "":
        firstName_error = True
    if request.POST["lastName"] == "":
        lastName_error = True
    if (
        not request.POST["password_1"] == request.POST["password_2"]
        or request.POST["password_1"] == ""
    ):
        password_error = True

    return {
        "password_error": password_error,
        "username_error": username_error,
        "username_exist_error": username_exist_error,
        "firstName_error": firstName_error,
        "lastName_error": lastName_error,
    }


def is_valid_registration(registration):
    print("registration valid check:", registration)
    print("registration valid check password:", registration["password_error"])

    if (
        not registration["password_error"]
        and not registration["username_error"]
        and not registration["username_exist_error"]
        and not registration["firstName_error"]
        and not registration["lastName_error"]
    ):
        return True
    else:
        return False


def create_user(request):
    user = User.objects.create_user(
        username=request.POST["username"],
        password=request.POST["password_1"],
        first_name=request.POST["firstName"],
        last_name=request.POST["lastName"],
    )
    return user
