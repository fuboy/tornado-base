from itsdangerous import URLSafeTimedSerializer


def generate_confirmation_token(content, secret_key, pass_salt):
    serializer = URLSafeTimedSerializer(secret_key)
    return serializer.dumps(content, salt=pass_salt)


def confirm_token(token, secret_key, pass_salt, expiration=3600):
    serializer = URLSafeTimedSerializer(secret_key)
    try:
        content = serializer.loads(token, salt=pass_salt, max_age=expiration)
    except:
        return False

    return content
