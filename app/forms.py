# third-party imports
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_ckeditor import CKEditorField
from wtforms import StringField, SelectField, EmailField, PasswordField, IntegerField, FloatField, TextAreaField, FieldList, FormField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Email, Length, EqualTo, ValidationError
from wtforms_sqlalchemy.fields import QuerySelectField, QueryRadioField
from flask_login import current_user

# local imports
from .models import User, Criteria, TourType, LocationPoint, SubCriteria


class RegisterForm(FlaskForm):
  name = StringField("Nama", validators=[DataRequired(), Length(min=4, max=60, message="Kolom harus memiliki panjang setidaknya 4 karakter.")])
  gender = SelectField("Jenis Kelamin", choices=[("", "Pilih Jenis Kelamin"), ("Laki-laki", "Laki-laki"), ("Perempuan", "Perempuan")], validators=[DataRequired()])
  phone = StringField("Nomor HP", validators=[DataRequired(), Length(min=10, max=20, message="Kolom harus memiliki panjang setidaknya 10 karakter.")])
  email = EmailField("Email", validators=[DataRequired(), Email(message="Email yang Anda masukkan tidak valid."), Length(max=60)])
  password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=128, message="Kolom harus memiliki panjang setidaknya 8 karakter.")])
  confirm = PasswordField("Konfirmasi Password", validators=[DataRequired(), Length(min=8, max=128), EqualTo("password", message="Konfirmasi password tidak cocok.")])
  submit = SubmitField("Daftar Sekarang")

  def validate_phone(self, phone):
    user = User.query.filter_by(phone=phone.data).first()
    if user:
      raise ValidationError("Nomor HP yang Anda masukkan sudah digunakan.")

  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user:
      raise ValidationError("Email yang Anda masukkan sudah digunakan.")

class LoginForm(FlaskForm):
  email = StringField("Email", validators=[DataRequired(), Email(message="Email yang Anda masukkan tidak valid."), Length(max=60)])
  password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=128)])
  submit = SubmitField("Masuk")

class ForgotPasswordForm(FlaskForm):
  email = EmailField("Email", validators=[DataRequired(), Email(message="Email yang Anda masukkan tidak valid."), Length(max=60)])
  submit = SubmitField("Kirim")

  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user is None:
      raise ValidationError("Email yang Anda masukkan tidak terdaftar.")

class ResetPasswordForm(FlaskForm):
  password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=128)])
  confirm = PasswordField("Konfirmasi Password", validators=[DataRequired(), Length(min=8, max=128), EqualTo("password", message="Konfirmasi password tidak cocok.")])
  submit = SubmitField("Atur Ulang")

class EditProfileForm(FlaskForm):
  name = StringField("Nama", validators=[DataRequired(), Length(min=4, max=60)])
  gender = SelectField("Jenis Kelamin", choices=[("", "Pilih Jenis Kelamin"), ("Laki-laki", "Laki-laki"), ("Perempuan", "Perempuan")], validators=[DataRequired()])
  phone = StringField("Nomor HP", validators=[DataRequired(), Length(min=10, max=20)])
  email = EmailField("Email", validators=[DataRequired(), Email(message="Email yang Anda masukkan tidak valid."), Length(max=60)])
  submit = SubmitField("Selesai")

  def validate_phone(self, phone):
    if phone.data != current_user.phone:
      user = User.query.filter_by(phone=phone.data).first()
      if user:
        raise ValidationError("Nomor HP yang Anda masukkan sudah digunakan.")

  def validate_email(self, email):
    if email.data != current_user.email:
      user = User.query.filter_by(email=email.data).first()
      if user:
        raise ValidationError("Email yang Anda masukkan sudah digunakan.")

class UsageHelpForm(FlaskForm):
  title = StringField("Judul", validators=[DataRequired(), Length(max=128)])
  description = StringField("Deskripsi", validators=[DataRequired()])
  image = FileField("Gambar", validators=[FileAllowed(["jpg", "jpeg", "png"], message="File yang Anda unggah tidak diperbolehkan. Silakan unggah file dalam format .jpg, .jpeg, atau .png.")])
  body = CKEditorField("Konten", validators=[DataRequired()])
  submit = SubmitField("Selesai")

class CriteriaForm(FlaskForm):
  name = StringField("Nama Kriteria", validators=[DataRequired(), Length(max=128)])
  code = StringField("Kode Kriteria", validators=[DataRequired(), Length(max=128)])
  attribute = SelectField("Atribut", choices=[("", "Pilih Atribut"), ("Cost", "Cost"), ("Benefit", "Benefit")], validators=[DataRequired()])
  weight = FloatField("Bobot", validators=[DataRequired()])
  submit = SubmitField("Selesai")

class SubCriteriaForm(FlaskForm):
  criteria = QuerySelectField("Kriteria", validators=[DataRequired()], query_factory=lambda: Criteria.query.order_by(Criteria.name.asc()).all(), get_label="name", allow_blank=True, blank_text="Pilih Kriteria")
  name = StringField("Nama Sub Kriteria", validators=[DataRequired(), Length(max=128)])
  value = IntegerField("Nilai Sub Kriteria", validators=[DataRequired()])
  submit = SubmitField("Selesai")

class LocationPointForm(FlaskForm):
  name = StringField("Nama Titik Lokasi", validators=[DataRequired(), Length(max=128)])
  submit = SubmitField("Selesai")

class TourTypeForm(FlaskForm):
  name = StringField("Nama Jenis Wisata", validators=[DataRequired(), Length(max=128)])
  submit = SubmitField("Selesai")

class DistanceForm(FlaskForm):
  location_point = QuerySelectField("Titik Lokasi", validators=[DataRequired()], query_factory=lambda: LocationPoint.query.all(), get_label="name", allow_blank=True, blank_text="Pilih Lokasi")
  distance = IntegerField("Jarak", validators=[InputRequired()])

class TourListForm(FlaskForm):
  name = StringField("Nama Objek Wisata", validators=[DataRequired(), Length(max=128)])
  tour_type = QuerySelectField("Jenis Wisata", validators=[DataRequired()], query_factory=lambda: TourType.query.order_by(TourType.name.asc()).all(), get_label="name", allow_blank=True, blank_text="Pilih Jenis Wisata")
  ticket = IntegerField("Harga Tiket", validators=[InputRequired()])
  facility = QuerySelectField("Fasilitas", validators=[DataRequired()], query_factory=lambda: SubCriteria.query.filter_by(criteria_id=2).all(), get_label="name", allow_blank=True, blank_text="Pilih Fasilitas")
  infrastructure = QuerySelectField("Infrastruktur", validators=[DataRequired()], query_factory=lambda: SubCriteria.query.filter_by(criteria_id=4).all(), get_label="name", allow_blank=True, blank_text="Pilih Infrastruktur")
  transportation_access = QuerySelectField("Akses Transportasi", validators=[DataRequired()], query_factory=lambda: SubCriteria.query.filter_by(criteria_id=5).all(), get_label="name", allow_blank=True, blank_text="Pilih Akses Transportasi")
  description = StringField("Deskripsi Wisata", validators=[DataRequired()])
  image = FileField("Gambar", validators=[FileAllowed(["jpg", "jpeg", "png"], message="File yang Anda unggah tidak diperbolehkan. Silakan unggah file dalam format .jpg, .jpeg, atau .png.")])
  body = CKEditorField("Konten", validators=[DataRequired()])
  distances = FieldList(FormField(DistanceForm))
  submit = SubmitField("Selesai")

class TourRecommendation1Form(FlaskForm):
  location_point = QueryRadioField("Titik Lokasi", validators=[DataRequired()], query_factory=lambda: LocationPoint.query.all(), get_label="name")
  tour_type = QueryRadioField("Jenis Wisata", validators=[DataRequired()], query_factory=lambda: TourType.query.all(), get_label="name")
  submit = SubmitField("Berikutnya")

class TourRecommendation2Form(FlaskForm):
  ticket = QueryRadioField("Tiket", validators=[DataRequired()], query_factory=lambda: SubCriteria.query.filter_by(criteria_id=1).all(), get_label="name")
  facility = QueryRadioField("Fasilitas", validators=[DataRequired()], query_factory=lambda: SubCriteria.query.filter_by(criteria_id=2).all(), get_label="name")
  distance = QueryRadioField("Jarak", validators=[DataRequired()], query_factory=lambda: SubCriteria.query.filter_by(criteria_id=3).all(), get_label="name")
  infrastructure = QueryRadioField("Infrastruktur", validators=[DataRequired()], query_factory=lambda: SubCriteria.query.filter_by(criteria_id=4).all(), get_label="name")
  transportation_access = QueryRadioField("Akses Transportasi", validators=[DataRequired()], query_factory=lambda: SubCriteria.query.filter_by(criteria_id=5).all(), get_label="name")
  submit = SubmitField("Selesai")