# third-party imports
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SelectField, EmailField, PasswordField, IntegerField, TextAreaField, RadioField, FieldList, FormField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from wtforms_sqlalchemy.fields import QuerySelectField
from flask_login import current_user

# local imports
from .models import User, Criteria, TourType, LocationPoint


class RegisterForm(FlaskForm):
  name = StringField("Nama", validators=[DataRequired(), Length(min=4, max=60)])
  gender = SelectField("Jenis Kelamin", choices=[("", "Pilih Jenis Kelamin"), ("Laki-laki", "Laki-laki"), ("Perempuan", "Perempuan")], validators=[DataRequired()])
  phone = StringField("Nomor HP", validators=[DataRequired(), Length(min=10, max=20)])
  email = EmailField("Email", validators=[DataRequired(), Email(message="Email yang Anda masukkan tidak valid."), Length(max=60)])
  password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=128)])
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
  submit = SubmitField("Kirim")

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
  description = TextAreaField("Deskripsi", render_kw={"rows": 3})
  image = FileField("Gambar", validators=[FileAllowed(["jpg", "jpeg", "png"], message="File yang Anda unggah tidak diperbolehkan. Silakan unggah file dalam format .jpg, .jpeg, atau .png.")])
  submit = SubmitField("Kirim")

class CriteriaForm(FlaskForm):
  name = StringField("Nama Kriteria", validators=[DataRequired(), Length(max=128)])
  code = StringField("Kode Kriteria", validators=[DataRequired(), Length(max=128)])
  attribute = SelectField("Atribut", choices=[("", "Pilih Atribut"), ("cost", "Cost"), ("benefit", "Benefit")], validators=[DataRequired()])
  weight = IntegerField("Bobot", validators=[DataRequired()])
  submit = SubmitField("Kirim")

class SubCriteriaForm(FlaskForm):
  criteria = QuerySelectField("Kriteria", validators=[DataRequired()], query_factory=lambda: Criteria.query.order_by(Criteria.name.asc()).all(), get_label="name", allow_blank=True, blank_text="Pilih Kriteria")
  name = StringField("Nama Sub Kriteria", validators=[DataRequired(), Length(max=128)])
  value = IntegerField("Nilai Sub Kriteria", validators=[DataRequired()])
  submit = SubmitField("Kirim")

class LocationPointForm(FlaskForm):
  name = StringField("Nama Titik Lokasi", validators=[DataRequired(), Length(max=128)])
  submit = SubmitField("Kirim")

class TourTypeForm(FlaskForm):
  name = StringField("Nama Jenis Wisata", validators=[DataRequired(), Length(max=128)])
  submit = SubmitField("Kirim")

class DistanceForm(FlaskForm):
  location_point = QuerySelectField("Lokasi", validators=[DataRequired()], query_factory=lambda: LocationPoint.query.all(), get_label="name", allow_blank=True, blank_text="Pilih Lokasi")
  distance = IntegerField("Jarak", validators=[DataRequired()])

class TourListForm(FlaskForm):
  name = StringField("Nama Objek Wisata", validators=[DataRequired(), Length(max=128)])
  tour_type = QuerySelectField("Jenis Wisata", validators=[DataRequired()], query_factory=lambda: TourType.query.order_by(TourType.name.asc()).all(), get_label="name", allow_blank=True, blank_text="Pilih Jenis Wisata")
  ticket  = SelectField("Tiket", choices=[("", "Pilih Tiket"), (1, "1"), (2, "2")], validators=[DataRequired()])
  facility  = SelectField("Fasilitas", choices=[("", "Pilih Fasilitas"), (1, "1"), (2, "2")], validators=[DataRequired()])
  infrastructure  = SelectField("Infrastruktur", choices=[("", "Pilih Infrastruktur"), (1, "1"), (2, "2")], validators=[DataRequired()])
  transportation_access  = SelectField("Akses Transportasi", choices=[("", "Pilih Infrastruktur"), (1, "1"), (2, "2")], validators=[DataRequired()])
  description = TextAreaField("Deskripsi Wisata", render_kw={"rows": 3})
  image = FileField("Gambar", validators=[FileAllowed(["jpg", "jpeg", "png"], message="File yang Anda unggah tidak diperbolehkan. Silakan unggah file dalam format .jpg, .jpeg, atau .png.")])
  distances = FieldList(FormField(DistanceForm), min_entries=1)
  submit = SubmitField("Kirim")

class TourRecommendation1Form(FlaskForm):
  location_point = RadioField("Titik Lokasi", choices=[("1", "Alun-Alun Bondowoso"), ("2", "Tugu Batas Kabupaten Situbondo dengan Bondowoso Prajekan"), ("3", "Gapura Batas Bondowoso Arak - Arak dengan Situbondo"), ("4", "Gapura Batas Bondowoso Maesan dengan Jember"), ("5", "Batas Bondowoso Ijen dengan Banyuwangi")], validators=[DataRequired()])
  tour_type = RadioField("Jenis Wisata", choices=[("1", "Wisata Alam"), ("2", "Wisata Pemandian"), ("3", "Wisata Sejarah")], validators=[DataRequired()])
  submit = SubmitField("Berikutnya")

class TourRecommendation2Form(FlaskForm):
  ticket = RadioField("Tiket", choices=[("1", "Rp. 0"), ("2", "Kurang dari atau Rp. 5.000"), ("3", "Antara 5000 sampai Rp. 10.000"), ("4", "Lebih dari Rp. 10.000")], validators=[DataRequired()])
  facility = RadioField("Fasilitas", choices=[("1", "Belum ada fasilitas"), ("2", "Fasilitas sangat kurang lengkap (Hanya terdapat tempat parkir dan tempat istirahat)"), ("3", "Fasilitas kurang lengkap"), ("4", "Fasilitas cukup lengkap"), ("5", "Fasilitas lengkap"),], validators=[DataRequired()])
  distance = RadioField("Jarak", choices=[("1", "≤10KM"), ("2", "≤20KM"), ("3", "≤30KM"), ("4", "≤40KM"), ("5", "≤50KM"), ("6", ">50KM"),], validators=[DataRequired()])



  infrastructure = RadioField("Infrastruktur", choices=[("1", "Belum ada infrastruktur yang tersedia"), ("2", "Infrastruktur sangat kurang bagus"), ("3", "Infrastruktur kurang bagus"), ("4", "Infrastruktur cukup bagus"), ("5", "Infrastruktur bagus"),], validators=[DataRequired()])
  transportation_access = RadioField("Akses Transportasi", choices=[("1", "Jalan kurang lebar"), ("2", "Jalan cukup lebar"), ("3", "Jalan lebar")], validators=[DataRequired()])
  submit = SubmitField("Kirim")
  