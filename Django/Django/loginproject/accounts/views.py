from django.shortcuts import render, redirect

from .storage import add_user, check_user, find_user
from .validation import validate_login, validate_register


def login_view(request):
    error = ""

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        error = validate_login(username, password)

        if error == "":
            saved_name = check_user(username, password)

            if saved_name is None:
                error = "Invalid username or password."
            else:
                request.session["username"] = saved_name
                return redirect("home")

    return render(request, "accounts/login.html", {"error": error})


def register_view(request):
    error = ""

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        confirm = request.POST.get("confirm", "")

        error = validate_register(username, password, confirm)

        if error == "" and find_user(username) is not None:
            error = "This username is already taken."

        if error == "":
            add_user(username, password)
            return redirect("/login/?registered=1")

    return render(request, "accounts/register.html", {"error": error})


def home_view(request):
    username = request.session.get("username")

    if not username:
        return redirect("login")

    return render(request, "accounts/home.html", {"username": username})


def logout_view(request):
    request.session.flush()
    return redirect("login")