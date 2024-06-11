# third-party imports
from flask import render_template, redirect, url_for, abort, flash, request
from flask_login import login_required, login_user, logout_user, current_user

# local imports
from . import control_panel_app
from .. import db, bcrypt
from ..models import User
from ..forms import RegisterForm, LoginForm, ForgotPasswordForm, ResetPasswordForm, EditProfileForm
from ..utils import send_password_reset


@control_panel_app.route("/daftar", methods=["GET", "POST"])
def register():
  if current_user.is_authenticated:
    return redirect(url_for("public_app.homepage"))

  form = RegisterForm()

  if form.validate_on_submit():
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")

    new_user = User(name=form.name.data, role="admin", gender=form.gender.data, phone=form.phone.data, email=form.email.data, password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    flash("Akun anda telah berhasil dibuat! Anda sekarang dapat masuk.")
    return redirect(url_for("control_panel_app.login"))

  return render_template("control_panel/auth/register.html", title="Daftar - Development", form=form)

@control_panel_app.route("/masuk", methods=["GET", "POST"])
def login():
  if current_user.is_authenticated:
    return redirect(url_for("public_app.homepage"))

  form = LoginForm()

  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user and bcrypt.check_password_hash(user.password, form.password.data):
      login_user(user)

      flash("Selamat Datang kembali. Anda telah berhasil masuk.")
      return redirect(url_for("public_app.homepage"))
    else:
      flash("Anda gagal masuk. Silakan periksa kembali email dan password Anda, pastikan sudah benar.")

  return render_template("control_panel/auth/login.html", title="Masuk - Development", form=form)

@control_panel_app.route("/lupa-password", methods=["GET", "POST"])
def forgot_password():
  if current_user.is_authenticated:
    return redirect(url_for("public_app.homepage"))

  form = ForgotPasswordForm()

  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()

    send_password_reset(user)

    flash("Kami telah mengirimkan email untuk mengatur ulang password Anda ke alamat email Anda.")
    return redirect(url_for("control_panel_app.login"))

  return render_template("control_panel/auth/forgot-password.html", title="Lupa Password - Development", form=form)

@control_panel_app.route("/lupa-password/<token>", methods=["GET", "POST"])
def reset_password(token):
  if current_user.is_authenticated:
    return redirect(url_for("public_app.homepage"))

  user = User.verify_reset_token(token)

  if user is None:
    flash("Token Anda tidak valid atau telah kedaluwarsa.")
    return redirect(url_for("control_panel_app.forgot_password"))

  form = ResetPasswordForm()

  if form.validate_on_submit():
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
    user.password = hashed_password

    db.session.commit()

    flash("Password Anda telah berhasil diperbarui. Harap ingat untuk menggunakannya untuk masuk berikutnya.")
    return redirect(url_for("control_panel_app.login"))

  return render_template("control_panel/auth/reset-password.html", title="Pengaturan Ulang Password - Development", form=form)

@control_panel_app.route("/pengguna/<id>", methods=["GET", "POST"])
def profile(id):
  user = User.query.filter_by(id=id).first_or_404()
  return render_template("control_panel/account/profile.html", title=f"{user.name} - Development", user=user)

@control_panel_app.route("/pengguna/<id>/edit", methods=["GET", "POST"])
@login_required
def edit_profile(id):
  user = User.query.filter_by(id=id).first_or_404()

  if current_user.is_anonymous or current_user.email != user.email:
    abort(403)

  form = EditProfileForm()

  if form.validate_on_submit():
    user.name = form.name.data
    user.gender = form.gender.data
    user.phone = form.phone.data
    user.email = form.email.data

    db.session.commit()

    flash("Profil Anda telah berhasil diperbarui. Terima kasih telah memperbarui informasi Anda.")
    return redirect(url_for("control_panel_app.profile", id=current_user.id))
  elif request.method == "GET":
    form.name.data = user.name
    form.phone.data = user.phone
    form.gender.data = user.gender
    form.email.data = user.email

  return render_template("control_panel/account/profile_form.html", title="Edit Profile - Development", user=user, form=form)

@control_panel_app.route("/signout")
@login_required
def logout():
  logout_user()

  flash("Anda telah berhasil keluar. Selamat tinggal dan sampai jumpa lagi!")
  return redirect(url_for("control_panel_app.login"))