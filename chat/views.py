from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from chat.utils import check_registration, is_valid_registration, create_user
from .models import Chat, Message
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers


# Create your views here.
@login_required(login_url="/login/")
def index(request):
    """
    This function is used to render the chat index page

    Args:
        request (_type_): POST request

    Returns:
        _type_: chat index page
    """
    print(request.method)
    if request.method == "POST" and not request.POST["textMessage"] == "":
        myChat = Chat.objects.get(id=1)
        new_message = Message.objects.create(
            text=request.POST["textMessage"],
            author=request.user,
            receiver=request.user,
            chat=myChat,
        )
        serialized_new_message = serializers.serialize("json", [new_message])
        return JsonResponse(serialized_new_message[1:-1], safe=False)
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
        else:
            return render(
                request, "auth/login.html", {"login_error": True, "redirect": "/chat/"}
            )

    return render(request, "auth/login.html", {"redirect": redirect})


def register_view(request):
    if request.method == "POST":
        registration_check = check_registration(request)
        print("reg check:", registration_check)

        if is_valid_registration(registration_check):
            user = create_user(request)
            user.save()
            login(request, user)
            return HttpResponseRedirect(redirect_to="/chat/")
        else:
            print("reg check_2:", registration_check)
            return render(request, "register/register.html", registration_check)
    return render(request, "register/register.html")


def logout_view(request):
    print(request.user)
