def validate_login(username, password):
    if username == "" or password == "":
        return "Please fill in both fields."

    if len(username) < 3:
        return "Username must be at least 3 characters."

    if len(username) > 30:
        return "Username must be at most 30 characters."

    if " " in username:
        return "Username must not contain spaces."

    return ""


def validate_register(username, password, confirm):
    error = validate_login(username, password)

    if error != "":
        return error

    if len(password) < 6:
        return "Password must be at least 6 characters."

    if password != confirm:
        return "Passwords do not match."

    return ""