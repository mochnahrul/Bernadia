# third-party imports
import numpy as np
from flask import render_template, redirect, url_for, flash, request, session
from flask_login import login_required, current_user
from wtforms import FieldList, FormField

# local imports
from . import public_app
from .. import db
from ..models import UsageHelp, Criteria, SubCriteria, LocationPoint, TourType, TourList, TourDistance
from ..forms import UsageHelpForm, CriteriaForm, SubCriteriaForm, LocationPointForm, TourTypeForm, TourListForm, TourRecommendation1Form, TourRecommendation2Form, DistanceForm
from ..utils import check_admin, save_resized_image, process_input_list_based_on_weight


# Homepage routes

@public_app.route("/", methods=["GET", "POST"])
def homepage():
  return render_template("public/index.html", title="Bondowoso Tourism")

# About routes

@public_app.route("/tentang", methods=["GET", "POST"])
def about():
  return render_template("public/about/about.html", title="Tentang - Bondowoso Tourism")

# Services routes

@public_app.route("/layanan", methods=["GET", "POST"])
@login_required
def services():
  return render_template("public/services/services.html", title="Layanan - Bondowoso Tourism")

# Usage Help routes

@public_app.route("/layanan/bantuan-penggunaan", methods=["GET", "POST"])
@login_required
def usage_help():
  page = request.args.get("page", 1, type=int)
  datas = UsageHelp.query.order_by(UsageHelp.posted_date.desc()).paginate(page=page, per_page=6)
  return render_template("public/services/usage_help/usage-help.html", title="Bantuan Penggunaan - Bondowoso Tourism", datas=datas)

@public_app.route("/layanan/bantuan-penggunaan/tambah", methods=["GET", "POST"])
@login_required
def create_usage_help():
  check_admin()
  form = UsageHelpForm()

  if form.validate_on_submit():
    if form.image.data:
      image = save_resized_image(form.image.data, 1280, 720, "usage_help")
      new_data = UsageHelp(title=form.title.data, description=form.description.data, image=image, user=current_user)
    else:
      new_data = UsageHelp(title=form.title.data, description=form.description.data, user=current_user)

    db.session.add(new_data)
    db.session.commit()

    flash("Data telah berhasil ditambahkan!", "success")
    return redirect(url_for("public_app.usage_help"))

  return render_template("public/services/usage_help/usage-help_form.html", title="Tambah Bantuan Penggunaan - Bondowoso Tourism", form=form, operation="Tambah")

@public_app.route("/layanan/bantuan-penggunaan/<id>/edit", methods=["GET", "POST"])
@login_required
def update_usage_help(id):
  check_admin()
  data = UsageHelp.query.filter_by(id=id).first_or_404()
  form = UsageHelpForm()

  if form.validate_on_submit():
    if form.image.data:
      image = save_resized_image(form.image.data, 1280, 720, "usage_help")
      data.image = image

    data.title = form.title.data
    data.description = form.description.data
    data.user = current_user

    db.session.commit()

    flash("Data telah berhasil diperbarui!", "success")
    return redirect(url_for("public_app.usage_help"))
  elif request.method == "GET":
    form.title.data = data.title
    form.description.data = data.description

  return render_template("public/services/usage_help/usage-help_form.html", title="Edit Bantuan Penggunaan - Bondowoso Tourism", form=form, operation="Edit")

@public_app.route("/layanan/bantuan-penggunaan/<id>/hapus", methods=["GET", "POST"])
@login_required
def delete_usage_help(id):
  check_admin()
  data = UsageHelp.query.filter_by(id=id).first_or_404()

  db.session.delete(data)
  db.session.commit()

  flash("Data telah berhasil dihapus!", "success")
  return redirect(url_for("public_app.usage_help"))

# System Data routes

@public_app.route("/layanan/data-sistem", methods=["GET", "POST"])
@login_required
def system_data():
  return render_template("public/services/system_data/system-data.html", title="Data Sistem - Bondowoso Tourism")

# System Data - Criteria routes

@public_app.route("/layanan/kriteria", methods=["GET", "POST"])
@login_required
def criteria():
  page = request.args.get("page", 1, type=int)
  datas = Criteria.query.order_by(Criteria.posted_date.desc()).paginate(page=page, per_page=5)
  return render_template("public/services/system_data/criteria.html", title="Kriteria - Bondowoso Tourism", datas=datas)

@public_app.route("/layanan/kriteria/tambah", methods=["GET", "POST"])
@login_required
def create_criteria():
  check_admin()
  form = CriteriaForm()

  if form.validate_on_submit():
    new_data = Criteria(name=form.name.data, code=form.code.data, attribute=form.attribute.data, weight=form.weight.data, user=current_user)

    db.session.add(new_data)
    db.session.commit()

    flash("Data telah berhasil ditambahkan!", "success")
    return redirect(url_for("public_app.criteria"))

  return render_template("public/services/system_data/criteria_form.html", title="Tambah Kriteria - Bondowoso Tourism", form=form, operation="Tambah")

@public_app.route("/layanan/kriteria/<id>/edit", methods=["GET", "POST"])
@login_required
def update_criteria(id):
  check_admin()
  data = Criteria.query.filter_by(id=id).first_or_404()
  form = CriteriaForm()

  if form.validate_on_submit():
    data.name = form.name.data
    data.code = form.code.data
    data.attribute = form.attribute.data
    data.weight = form.weight.data
    data.user = current_user

    db.session.commit()

    flash("Data telah berhasil diperbarui!", "success")
    return redirect(url_for("public_app.criteria"))
  elif request.method == "GET":
    form.name.data = data.name
    form.code.data = data.code
    form.attribute.data = data.attribute
    form.weight.data = data.weight

  return render_template("public/services/system_data/criteria_form.html", title="Edit Kriteria - Bondowoso Tourism", form=form, operation="Edit")

@public_app.route("/layanan/kriteria/<id>/hapus", methods=["GET", "POST"])
def delete_criteria(id):
  check_admin()
  data = Criteria.query.filter_by(id=id).first_or_404()

  db.session.delete(data)
  db.session.commit()

  flash("Data telah berhasil dihapus!", "success")
  return redirect(url_for("public_app.criteria"))

# System Data - Sub Criteria routes

@public_app.route("/layanan/sub-kriteria", methods=["GET", "POST"])
@login_required
def sub_criteria():
  page = request.args.get("page", 1, type=int)
  datas = SubCriteria.query.order_by(SubCriteria.posted_date.desc()).paginate(page=page, per_page=5)
  return render_template("public/services/system_data/sub-criteria.html", title="Sub Kriteria - Bondowoso Tourism", datas=datas)

@public_app.route("/layanan/sub-kriteria/tambah", methods=["GET", "POST"])
@login_required
def create_sub_criteria():
  check_admin()
  form = SubCriteriaForm()

  if form.validate_on_submit():
    new_data = SubCriteria(criteria=form.criteria.data, name=form.name.data, value=form.value.data, user=current_user)

    db.session.add(new_data)
    db.session.commit()

    flash("Data telah berhasil ditambahkan!", "success")
    return redirect(url_for("public_app.sub_criteria"))

  return render_template("public/services/system_data/sub-criteria_form.html", title="Tambah Sub Kriteria - Bondowoso Tourism", form=form, operation="Tambah")

@public_app.route("/layanan/sub-kriteria/<id>/edit", methods=["GET", "POST"])
@login_required
def update_sub_criteria(id):
  check_admin()
  data = SubCriteria.query.filter_by(id=id).first_or_404()
  form = SubCriteriaForm()

  if form.validate_on_submit():
    data.criteria = form.criteria.data
    data.name = form.name.data
    data.value = form.value.data
    data.user = current_user

    db.session.commit()

    flash("Data telah berhasil diperbarui!", "success")
    return redirect(url_for("public_app.sub_criteria"))
  elif request.method == "GET":
    form.criteria.data = data.criteria
    form.name.data = data.name
    form.value.data = data.value

  return render_template("public/services/system_data/sub-criteria_form.html", title="Edit Sub Kriteria - Bondowoso Tourism", form=form, operation="Edit")

@public_app.route("/layanan/sub-kriteria/<id>/hapus", methods=["GET", "POST"])
@login_required
def delete_sub_criteria(id):
  check_admin()
  data = SubCriteria.query.filter_by(id=id).first_or_404()

  db.session.delete(data)
  db.session.commit()

  flash("Data telah berhasil dihapus!", "success")
  return redirect(url_for("public_app.sub_criteria"))

# System Data - Location Point routes

@public_app.route("/layanan/titik-lokasi", methods=["GET", "POST"])
@login_required
def location_point():
  page = request.args.get("page", 1, type=int)
  datas = LocationPoint.query.order_by(LocationPoint.posted_date.desc()).paginate(page=page, per_page=5)
  return render_template("public/services/system_data/location-point.html", title="Titik Lokasi - Bondowoso Tourism", datas=datas)

@public_app.route("/layanan/titik-lokasi/tambah", methods=["GET", "POST"])
@login_required
def create_location_point():
  check_admin()
  form = LocationPointForm()

  if form.validate_on_submit():
    new_data = LocationPoint(name=form.name.data, user=current_user)

    db.session.add(new_data)
    db.session.commit()

    tour_lists = TourList.query.all()
    for tour in tour_lists:
      new_distance = TourDistance(tour_list_id=tour.id, location_point_id=new_data.id, distance=0)
      db.session.add(new_distance)

    db.session.commit()

    flash("Data telah berhasil ditambahkan!", "success")
    return redirect(url_for("public_app.location_point"))

  return render_template("public/services/system_data/location-point_form.html", title="Tambah Titik Lokasi - Bondowoso Tourism", form=form, operation="Tambah")

@public_app.route("/layanan/titik-lokasi/<id>/edit", methods=["GET", "POST"])
@login_required
def update_location_point(id):
  check_admin()
  data = LocationPoint.query.filter_by(id=id).first_or_404()
  form = LocationPointForm()

  if form.validate_on_submit():
    data.name = form.name.data
    data.user = current_user

    db.session.commit()

    flash("Data telah berhasil diperbarui!", "success")
    return redirect(url_for("public_app.location_point"))
  elif request.method == "GET":
    form.name.data = data.name

  return render_template("public/services/system_data/location-point_form.html", title="Edit Titik Lokasi - Bondowoso Tourism", form=form, operation="Edit")

@public_app.route("/layanan/titik-lokasi/<id>/hapus", methods=["GET", "POST"])
@login_required
def delete_location_point(id):
  check_admin()
  data = LocationPoint.query.filter_by(id=id).first_or_404()

  db.session.delete(data)
  db.session.commit()

  flash("Data telah berhasil dihapus!", "success")
  return redirect(url_for("public_app.location_point"))

# System Data - Tour Type routes

@public_app.route("/layanan/jenis-wisata", methods=["GET", "POST"])
@login_required
def tour_type():
  page = request.args.get("page", 1, type=int)
  datas = TourType.query.order_by(TourType.posted_date.desc()).paginate(page=page, per_page=5)
  return render_template("public/services/system_data/tour-type.html", title="Jenis Wisata - Bondowoso Tourism", datas=datas)

@public_app.route("/layanan/jenis-wisata/tambah", methods=["GET", "POST"])
@login_required
def create_tour_type():
  check_admin()
  form = TourTypeForm()

  if form.validate_on_submit():
    new_data = TourType(name=form.name.data, user=current_user)

    db.session.add(new_data)
    db.session.commit()

    flash("Data telah berhasil ditambahkan!", "success")
    return redirect(url_for("public_app.tour_type"))

  return render_template("public/services/system_data/tour-type_form.html", title="Tambah Jenis Wisata - Bondowoso Tourism", form=form, operation="Tambah")

@public_app.route("/layanan/jenis-wisata/<id>/edit", methods=["GET", "POST"])
@login_required
def update_tour_type(id):
  check_admin()
  data = TourType.query.filter_by(id=id).first_or_404()
  form = TourTypeForm()

  if form.validate_on_submit():
    data.name = form.name.data
    data.user = current_user

    db.session.commit()

    flash("Data telah berhasil diperbarui!", "success")
    return redirect(url_for("public_app.tour_type"))
  elif request.method == "GET":
    form.name.data = data.name

  return render_template("public/services/system_data/tour-type_form.html", title="Edit Jenis Wisata - Bondowoso Tourism", form=form, operation="Edit")

@public_app.route("/layanan/jenis-wisata/<id>/hapus", methods=["GET", "POST"])
@login_required
def delete_tour_type(id):
  check_admin()
  data = TourType.query.filter_by(id=id).first_or_404()

  db.session.delete(data)
  db.session.commit()

  flash("Data telah berhasil dihapus!", "success")
  return redirect(url_for("public_app.tour_type"))

# Tour List routes

@public_app.route("/layanan/daftar-wisata", methods=["GET", "POST"])
@login_required
def tour_list():
  page = request.args.get("page", 1, type=int)
  datas = TourList.query.order_by(TourList.posted_date.desc()).paginate(page=page, per_page=6)
  return render_template("public/services/tour_list/tour-list.html", title="Daftar Wisata - Bondowoso Tourism", datas=datas)

@public_app.route("/layanan/daftar-wisata/<id>", methods=["GET", "POST"])
@login_required
def tour_list_detail(id):
  data = TourList.query.filter_by(id=id).first_or_404()
  facility = SubCriteria.query.filter_by(criteria_id=2, value=data.facility).first_or_404()
  distance = TourDistance.query.filter_by(tour_list_id=id).first_or_404()
  infrastructure = SubCriteria.query.filter_by(criteria_id=4, value=data.infrastructure).first_or_404()
  transportation_access = SubCriteria.query.filter_by(criteria_id=5, value=data.transportation_access).first_or_404()
  return render_template("public/services/tour_list/tour-list_detail.html", title=f"{data.name} - Bondowoso Tourism", data=data, distance=distance, facility=facility, infrastructure=infrastructure, transportation_access=transportation_access)

@public_app.route("/layanan/daftar-wisata/tambah", methods=["GET", "POST"])
@login_required
def create_tour_list():
  check_admin()
  location_points = LocationPoint.query.all()
  count = len(location_points)

  # define the local form dynamically
  class LocalForm(TourListForm):
    distances = FieldList(FormField(DistanceForm), min_entries=count)

  form = LocalForm()

  # set default values for the location points
  for i, location_point in enumerate(location_points):
    if i < len(form.distances.entries):
      form.distances.entries[i].form.location_point.data = location_point

  if form.validate_on_submit():
    if form.image.data:
      image = save_resized_image(form.image.data, 1280, 720, "tour_list")
      new_tour_list = TourList(name=form.name.data, tour_type=form.tour_type.data, ticket=form.ticket.data, facility=str(form.facility.data), infrastructure=str(form.infrastructure.data), transportation_access=str(form.transportation_access.data), description=form.description.data, image=image, user=current_user)
    else:
      new_tour_list = TourList(name=form.name.data, tour_type=form.tour_type.data, ticket=form.ticket.data, facility=str(form.facility.data), infrastructure=str(form.infrastructure.data), transportation_access=str(form.transportation_access.data), description=form.description.data, user=current_user)

    db.session.add(new_tour_list)
    db.session.commit()

    for distance_form in form.distances:
      distance = TourDistance(tour_list_id=new_tour_list.id, location_point_id=distance_form.location_point.data.id, distance=distance_form.distance.data)
      db.session.add(distance)

    db.session.commit()

    flash("Data telah berhasil ditambahkan!", "success")
    return redirect(url_for("public_app.tour_list"))

  return render_template("public/services/tour_list/tour-list_form.html", title="Tambah Daftar Wisata - Bondowoso Tourism", form=form, operation="Tambah")

@public_app.route("/layanan/daftar-wisata/<id>/edit", methods=["GET", "POST"])
@login_required
def update_tour_list(id):
  check_admin()
  data = TourList.query.filter_by(id=id).first_or_404()
  location_points = LocationPoint.query.all()
  distances_data = TourDistance.query.filter_by(tour_list_id=id).all()
  count = len(location_points)

  # define the local form dynamically
  class LocalForm(TourListForm):
    distances = FieldList(FormField(DistanceForm), min_entries=count)

  form = LocalForm()

  if form.validate_on_submit():
    if form.image.data:
      image = save_resized_image(form.image.data, 1280, 720, "tour_list")
      data.image = image

    data.name = form.name.data
    data.tour_type = form.tour_type.data
    data.ticket = form.ticket.data
    data.facility = str(form.facility.data)
    data.infrastructure = str(form.infrastructure.data)
    data.transportation_access = str(form.transportation_access.data)
    data.description = form.description.data
    data.user = current_user

    # update distances
    TourDistance.query.filter_by(tour_list_id=id).delete() # remove old distances
    for distance_form in form.distances:
      distance = TourDistance(tour_list_id=data.id, location_point_id=distance_form.location_point.data.id, distance=distance_form.distance.data)
      db.session.add(distance)
    db.session.commit()

    flash("Data telah berhasil diperbarui!", "success")
    return redirect(url_for("public_app.tour_list"))
  elif request.method == "GET":
    facility = SubCriteria.query.filter_by(criteria_id=2, value=data.facility).first()
    infrastructure = SubCriteria.query.filter_by(criteria_id=4, value=data.infrastructure).first()
    transportation_access = SubCriteria.query.filter_by(criteria_id=5, value=data.transportation_access).first()

    form.name.data = data.name
    form.tour_type.data = data.tour_type
    form.ticket.data = data.ticket
    form.facility.data = facility
    form.infrastructure.data = infrastructure
    form.transportation_access.data = transportation_access
    form.description.data = data.description

    for i, distance in enumerate(distances_data):
      if i < len(form.distances.entries):
        form.distances.entries[i].form.location_point.data = distance.location_point
        form.distances.entries[i].form.distance.data = distance.distance

  return render_template("public/services/tour_list/tour-list_form.html", title="Edit Daftar Wisata - Bondowoso Tourism", form=form, operation="Edit")

@public_app.route("/layanan/daftar-wisata/<id>/hapus", methods=["GET", "POST"])
@login_required
def delete_tour_list(id):
  check_admin()
  data = TourList.query.filter_by(id=id).first_or_404()

  TourDistance.query.filter_by(tour_list_id=id).delete()
  
  db.session.delete(data)
  db.session.commit()

  flash("Data telah berhasil dihapus!", "success")
  return redirect(url_for("public_app.tour_list"))

# Tour Recommendation routes

@public_app.route("/layanan/rekomendasi-wisata", methods=["GET", "POST"])
@login_required
def tour_recommendation():
  form = TourRecommendation1Form()

  if form.validate_on_submit():
    location_point = str(form.location_point.data)
    tour_type = str(form.tour_type.data)

    session["location_point"] = location_point
    session["tour_type"] = tour_type
    session["form1_filled"] = True 
    return redirect(url_for("public_app.tour_recommendation_sub_criteria"))

  return render_template("public/services/tour_recommendation/tour-recommendation-1.html", title="Rekomendasi Wisata - Bondowoso Tourism", form=form)

@public_app.route("/layanan/rekomendasi-wisata/sub-kriteria", methods=["GET", "POST"])
@login_required
def tour_recommendation_sub_criteria():
  if not session.get("form1_filled"):
    return redirect(url_for("public_app.tour_recommendation"))

  form = TourRecommendation2Form()

  if form.validate_on_submit():
    location_point = session.get("location_point")
    tour_type = session.get("tour_type")
    ticket = str(form.ticket.data)
    facility = str(form.facility.data)
    distance = str(form.distance.data)
    infrastructure = str(form.infrastructure.data)
    transportation_access = str(form.transportation_access.data)

    criteria = Criteria.query.all()

    avg_weight = [criteria.weight for criteria in criteria]
    weight_type = [1 if criteria.attribute == "Cost" else 2 for criteria in criteria]

    tours_and_distances = db.session.query(
      TourList.id,
      TourList.name,
      TourList.ticket,
      TourList.facility,
      TourList.infrastructure,
      TourList.transportation_access,
      TourDistance.distance
    ).join(
      TourDistance,
      TourList.id == TourDistance.tour_list_id
    ).filter(
      TourList.tour_type_id == tour_type,
      TourDistance.location_point_id == location_point
    ).all()

    facility_subcriteria = SubCriteria.query.filter_by(criteria_id=2, value=facility).first()
    infrastructure_subcriteria = SubCriteria.query.filter_by(criteria_id=4, value=infrastructure).first()
    transportation_access_subcriteria = SubCriteria.query.filter_by(criteria_id=5, value=transportation_access).first()

    ticket_category = 0
    distance_category = 0

    list_ids = []
    list_names = []
    filtered_np_list = []

    for tour in tours_and_distances:
      if tour.ticket == 0:
        ticket_category = 1
      elif tour.ticket <= 5000:
        ticket_category = 2
      elif tour.ticket <= 10000:
        ticket_category = 3
      elif tour.ticket > 10000:
        ticket_category = 4

      if tour.distance <= 10:
        distance_category = 1
      elif tour.distance <= 20:
        distance_category = 2
      elif tour.distance <= 30:
        distance_category = 3
      elif tour.distance <= 40:
        distance_category = 4
      elif tour.distance <= 50:
        distance_category = 5
      elif tour.distance > 50:
        distance_category = 6

      if ticket_category > int(ticket) or tour.facility < int(facility_subcriteria.value) or int(tour.infrastructure) < int(infrastructure_subcriteria.value) or tour.transportation_access < int(transportation_access_subcriteria.value) or distance_category > int(distance):
        continue

      list_ids.append(tour.id)
      list_names.append(tour.name)
      filtered_np_list.append([
        float(ticket_category),
        float(tour.facility),
        float(distance_category),
        float(tour.infrastructure),
        float(tour.transportation_access)
      ])

    filtered_np_array = np.array(filtered_np_list)

    if filtered_np_array.size == 0:
      return render_template("public/services/tour_recommendation/tour-recommendation_result.html", title="Rekomendasi Wisata - Bondowoso Tourism", result=[], error_message="Wisata yang Anda cari tidak ditemukan.")

    if len(filtered_np_array) == 1:
      preference_metric = np.array([1.0])
    else:
      preference_metric = process_input_list_based_on_weight(filtered_np_array, np.array(avg_weight), weight_type)

    paired_list = list(zip(preference_metric, list_names, list_ids))

    sorted_paired_list = sorted(paired_list, reverse=True)

    top_3_paired_list = sorted_paired_list[:3]

    result = [{"ranking": str(rank), "score": str(int(value * 100)), "tour_object": name, "action": id} for rank, (value, name, id) in enumerate(top_3_paired_list, start=1)]

    session.pop("location_point", None)
    session.pop("ticket_price", None)
    session.pop("form1_filled", None)

    return render_template("public/services/tour_recommendation/tour-recommendation_result.html", title="Rekomendasi Wisata - Bondowoso Tourism", result=result)

  return render_template("public/services/tour_recommendation/tour-recommendation-2.html", title="Rekomendasi Wisata - Bondowoso Tourism", form=form)