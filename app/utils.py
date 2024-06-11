# third-party imports
import os, secrets
from PIL import Image
from flask import url_for, abort, current_app
from flask_mail import Message
from flask_login import current_user


# local imports
from . import mail
from .models import User


# function to check if the user is an admin
def check_admin():
  if not current_user.role == "admin":
    abort(403)

# function to send a password reset message via email
def send_password_reset(user):
  token = user.get_reset_token()
  message = Message("Password reset request", sender="intellicrop@gmail.com", recipients=[user.email])
  message.body = f'''Hello, {user.name}\n \nTo reset your password, visit the following link:\n{url_for("control_panel_app.reset_password", token=token, _external=True)}\n \nIf you did not make this request, please disregard this email, and no changes will be made.'''
  mail.send(message)

# function to save a resized image in a directory
def save_resized_image(input, width, height):
  if input:
    upload_dir = os.path.join(current_app.root_path, "static/media/uploads")
    if not os.path.exists(upload_dir):
      os.makedirs(upload_dir)

    random_hex = secrets.token_hex(8)
    _, image_ext = os.path.splitext(input.filename)
    image_fn = f"{random_hex}{image_ext}"
    image_path = os.path.join(upload_dir, image_fn)

    image = Image.open(input)
    image.thumbnail((width, height))
    image.save(image_path)

    return image_fn