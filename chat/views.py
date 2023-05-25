from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from .models import Chat, Message
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse


# Create your views here.
@login_required(login_url="/login/")
def index(request):
    print(request.method)
    if request.method == "POST" and not request.POST["textMessage"] == "":
        myChat = Chat.objects.get(id=1)
        Message.objects.create(
            text=request.POST["textMessage"],
            author=request.user,
            receiver=request.user,
            chat=myChat,
        )
    chatMessages = Message.objects.filter(chat__id=1)
    return render(request, "chat/index.html", {"messages": chatMessages})


def login_view(request):
    redirect = request.GET.get("next")
    print("request", request.POST.get("username"))
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(redirect_to="redirect")
            # return redirect(request.POST.get("redirect"))
        else:
            return render(
                request, "auth/login.html", {"login_error": True, "redirect": "/chat/"}
            )

    return render(request, "auth/login.html", {"redirect": redirect})


def register_view(request):
    if request.method == "POST":
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

        if (
            not password_error
            and not username_error
            and not username_exist_error
            and not firstName_error
            and not lastName_error
        ):
            user = User.objects.create_user(
                username=request.POST["username"],
                password=request.POST["password_1"],
                first_name=request.POST["firstName"],
                last_name=request.POST["lastName"],
            )
            user.save()
            login(request, user)
            return HttpResponseRedirect(redirect_to="/chat/")
        else:
            return render(
                request,
                "register/register.html",
                {
                    "password_error": password_error,
                    "username_error": username_error,
                    "username_exist_error": username_exist_error,
                    "firstName_error": firstName_error,
                    "lastName_error": lastName_error,
                },
            )
    return render(request, "register/register.html")


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return render(request, "auth/login.html")
