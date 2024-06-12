# third-party imports
from flask import render_template, redirect, url_for, abort, flash, request, session
from flask_login import login_required, current_user

# local imports
from . import public_app
from .. import db
from ..models import UsageHelp, Criteria, SubCriteria, LocationPoint, TourType, TourList, TourDistance
from ..forms import UsageHelpForm, CriteriaForm, SubCriteriaForm, LocationPointForm, TourTypeForm, TourListForm, TourRecommendation1Form, TourRecommendation2Form
from ..utils import check_admin, save_resized_image, process_input_list_based_on_weight

import numpy as np

# Homepage routes

@public_app.route("/", methods=["GET", "POST"])
def homepage():
  return render_template("public/index.html", title="Development")

# About routes

@public_app.route("/tentang", methods=["GET", "POST"])
def about():
  return render_template("public/about/about.html", title="Tentang - Development")

# Services routes

@public_app.route("/layanan", methods=["GET", "POST"])
@login_required
def services():
  return render_template("public/services/services.html", title="Layanan - Development")

# Usage Help routes

@public_app.route("/bantuan-penggunaan", methods=["GET", "POST"])
@login_required
def usage_help():
  page = request.args.get("page", 1, type=int)
  datas = UsageHelp.query.order_by(UsageHelp.posted_date.desc()).paginate(page=page, per_page=5)
  return render_template("public/services/usage_help/usage-help.html", title="Bantuan Penggunaan - Development", datas=datas)

@public_app.route("/bantuan-penggunaan/tambah", methods=["GET", "POST"])
@login_required
def create_usage_help():
  check_admin()
  form = UsageHelpForm()

  if form.validate_on_submit():
    if form.image.data:
      image = save_resized_image(form.image.data, 1280, 720)
      new_data = UsageHelp(title=form.title.data, description=form.description.data, image=image, user=current_user)
    else:
      new_data = UsageHelp(title=form.title.data, description=form.description.data, user=current_user)

    db.session.add(new_data)
    db.session.commit()

    flash("Data telah berhasil ditambahkan!", "success")
    return redirect(url_for("public_app.usage_help"))

  return render_template("public/services/usage_help/usage-help_form.html", title="Tambah Bantuan Penggunaan - Development", form=form, operation="Tambah")

@public_app.route("/bantuan-penggunaan/<id>/edit", methods=["GET", "POST"])
@login_required
def update_usage_help(id):
  check_admin()
  data = UsageHelp.query.filter_by(id=id).first_or_404()
  form = UsageHelpForm()

  if form.validate_on_submit():
    if form.image.data:
      image = save_resized_image(form.image.data, 1280, 720)
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

  return render_template("public/services/usage_help/usage-help_form.html", title="Edit Bantuan Penggunaan - Development", form=form, operation="Edit")

@public_app.route("/bantuan-penggunaan/<id>/hapus", methods=["GET", "POST"])
@login_required
def delete_usage_help(id):
  check_admin()
  data = UsageHelp.query.filter_by(id=id).first_or_404()

  db.session.delete(data)
  db.session.commit()

  flash("Data telah berhasil dihapus!", "success")
  return redirect(url_for("public_app.usage_help"))

# System Data routes

@public_app.route("/data-sistem", methods=["GET", "POST"])
@login_required
def system_data():
  return render_template("public/services/system_data/system-data.html", title="Data Sistem - Development")

# System Data - Criteria routes

@public_app.route("/kriteria", methods=["GET", "POST"])
@login_required
def criteria():
  page = request.args.get("page", 1, type=int)
  datas = Criteria.query.order_by(Criteria.posted_date.desc()).paginate(page=page, per_page=5)
  return render_template("public/services/system_data/criteria.html", title="Kriteria - Development", datas=datas)

@public_app.route("/kriteria/tambah", methods=["GET", "POST"])
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

  return render_template("public/services/system_data/criteria_form.html", title="Tambah Kriteria - Development", form=form, operation="Tambah")

@public_app.route("/kriteria/<id>/edit", methods=["GET", "POST"])
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

  return render_template("public/services/system_data/criteria_form.html", title="Edit Kriteria - Development", form=form, operation="Edit")

@public_app.route("/kriteria/<id>/hapus", methods=["GET", "POST"])
def delete_criteria(id):
  check_admin()
  data = Criteria.query.filter_by(id=id).first_or_404()

  db.session.delete(data)
  db.session.commit()

  flash("Data telah berhasil dihapus!", "success")
  return redirect(url_for("public_app.criteria"))

# System Data - Sub Criteria routes

@public_app.route("/sub-kriteria", methods=["GET", "POST"])
@login_required
def sub_criteria():
  page = request.args.get("page", 1, type=int)
  datas = SubCriteria.query.order_by(SubCriteria.posted_date.desc()).paginate(page=page, per_page=5)
  return render_template("public/services/system_data/sub-criteria.html", title="Sub Kriteria - Development", datas=datas)

@public_app.route("/sub-kriteria/tambah", methods=["GET", "POST"])
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

  return render_template("public/services/system_data/sub-criteria_form.html", title="Tambah Sub Kriteria - Development", form=form, operation="Tambah")

@public_app.route("/sub-kriteria/<id>/edit", methods=["GET", "POST"])
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

  return render_template("public/services/system_data/sub-criteria_form.html", title="Edit Sub Kriteria - Development", form=form, operation="Edit")

@public_app.route("/sub-kriteria/<id>/hapus", methods=["GET", "POST"])
@login_required
def delete_sub_criteria(id):
  check_admin()
  data = SubCriteria.query.filter_by(id=id).first_or_404()

  db.session.delete(data)
  db.session.commit()

  flash("Data telah berhasil dihapus!", "success")
  return redirect(url_for("public_app.sub_criteria"))

# System Data - Location Point routes

@public_app.route("/titik-lokasi", methods=["GET", "POST"])
@login_required
def location_point():
  page = request.args.get("page", 1, type=int)
  datas = LocationPoint.query.order_by(LocationPoint.posted_date.desc()).paginate(page=page, per_page=5)
  return render_template("public/services/system_data/location-point.html", title="Titik Lokasi - Development", datas=datas)

@public_app.route("/titik-lokasi/tambah", methods=["GET", "POST"])
@login_required
def create_location_point():
  check_admin()
  form = LocationPointForm()

  if form.validate_on_submit():
    new_data = LocationPoint(name=form.name.data, user=current_user)

    db.session.add(new_data)
    db.session.commit()

    flash("Data telah berhasil ditambahkan!", "success")
    return redirect(url_for("public_app.location_point"))

  return render_template("public/services/system_data/location-point_form.html", title="Tambah Titik Lokasi - Development", form=form, operation="Tambah")

@public_app.route("/titik-lokasi/<id>/edit", methods=["GET", "POST"])
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

  return render_template("public/services/system_data/location-point_form.html", title="Edit Titik Lokasi - Development", form=form, operation="Edit")

@public_app.route("/titik-lokasi/<id>/hapus", methods=["GET", "POST"])
@login_required
def delete_location_point(id):
  check_admin()
  data = LocationPoint.query.filter_by(id=id).first_or_404()

  db.session.delete(data)
  db.session.commit()

  flash("Data telah berhasil dihapus!", "success")
  return redirect(url_for("public_app.location_point"))

# System Data - Tour Type routes

@public_app.route("/jenis-wisata", methods=["GET", "POST"])
@login_required
def tour_type():
  page = request.args.get("page", 1, type=int)
  datas = TourType.query.order_by(TourType.posted_date.desc()).paginate(page=page, per_page=5)
  return render_template("public/services/system_data/tour-type.html", title="Jenis Wisata - Development", datas=datas)

@public_app.route("/jenis-wisata/tambah", methods=["GET", "POST"])
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

  return render_template("public/services/system_data/tour-type_form.html", title="Tambah Jenis Wisata - Development", form=form, operation="Tambah")

@public_app.route("/jenis-wisata/<id>/edit", methods=["GET", "POST"])
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

  return render_template("public/services/system_data/tour-type_form.html", title="Edit Jenis Wisata - Development", form=form, operation="Edit")

@public_app.route("/jenis-wisata/<id>/hapus", methods=["GET", "POST"])
@login_required
def delete_tour_type(id):
  check_admin()
  data = TourType.query.filter_by(id=id).first_or_404()

  db.session.delete(data)
  db.session.commit()

  flash("Data telah berhasil dihapus!", "success")
  return redirect(url_for("public_app.tour_type"))

# Tour List routes

@public_app.route("/daftar-wisata", methods=["GET", "POST"])
@login_required
def tour_list():
  page = request.args.get("page", 1, type=int)
  datas = TourList.query.order_by(TourList.posted_date.desc()).paginate(page=page, per_page=5)
  return render_template("public/services/tour_list/tour-list.html", title="Daftar Wisata - Development", datas=datas)

@public_app.route("/daftar-wisata/tambah", methods=["GET", "POST"])
@login_required
def create_tour_list():
  check_admin()
  form = TourListForm()

  if form.validate_on_submit():
    if form.image.data:
      image = save_resized_image(form.image.data, 1280, 720)
      new_tour_list = TourList(name=form.name.data, tour_type=form.tour_type.data, ticket=form.ticket.data, facility=form.facility.data, infrastructure=form.infrastructure.data, transportation_access=form.transportation_access.data, description=form.description.data, image=image, user=current_user)
    else:
      new_tour_list = TourList(name=form.name.data, tour_type=form.tour_type.data, ticket=form.ticket.data, facility=form.facility.data, infrastructure=form.infrastructure.data, transportation_access=form.transportation_access.data, description=form.description.data, user=current_user)

    db.session.add(new_tour_list)
    db.session.commit()

    for distance_form in form.distances:
      distance = TourDistance(tour_list_id=new_tour_list.id, location_point_id=distance_form.location_point.data.id, distance=distance_form.distance.data)
      db.session.add(distance)

    db.session.commit()

    flash("Data telah berhasil ditambahkan!", "success")
    return redirect(url_for("public_app.tour_list"))
  else:
    for fieldName, errorMessages in form.errors.items():
      for err in errorMessages:
        print(f"Error in {fieldName}: {err}")

  return render_template("public/services/tour_list/tour-list_form.html", title="Tambah Daftar Wisata - Development", form=form, operation="Tambah")

@public_app.route("/daftar-wisata/<id>/edit", methods=["GET", "POST"])
@login_required
def update_tour_list(id):
  check_admin()
  data = TourList.query.filter_by(id=id).first_or_404()
  form = TourListForm()

  if form.validate_on_submit():
    if form.image.data:
      image = save_resized_image(form.image.data, 1280, 720)
      data.image = image

    data.name = form.name.data
    data.tour_type = form.tour_type.data
    data.ticket = form.ticket.data
    data.facility = form.facility.data
    data.infrastructure = form.infrastructure.data
    data.transportation_access = form.transportation_access.data
    data.description = form.description.data
    data.user = current_user

    TourDistance.query.filter_by(tour_list_id=data.id).delete()
    for distance_form in form.distances:
      distance = TourDistance(tour_list_id=data.id, location_point_id=distance_form.location_point.data.id, distance=distance_form.distance.data)
      db.session.add(distance)

    db.session.commit()

    flash("Data telah berhasil diperbarui!", "success")
    return redirect(url_for("public_app.tour_list"))
  elif request.method == "GET":
    form.name.data = data.name
    form.tour_type.data = data.tour_type
    form.ticket.data = data.ticket
    form.facility.data = data.facility
    form.infrastructure.data = data.infrastructure
    form.transportation_access.data = data.transportation_access
    form.description.data = data.description

    distances = TourDistance.query.filter_by(tour_list_id=data.id).all()
    for distance in distances:
      form.distances.append_entry({"location_point": distance.location_point, "distance": distance.distance})

  return render_template("public/services/tour_list/tour-list_form.html", title="Edit Daftar Wisata - Development", form=form, operation="Edit")

@public_app.route("/daftar-wisata/<id>/hapus", methods=["GET", "POST"])
@login_required
def delete_tour_list(id):
  check_admin()
  data = TourList.query.filter_by(id=id).first_or_404()

  db.session.delete(data)
  db.session.commit()

  flash("Data telah berhasil dihapus!", "success")
  return redirect(url_for("public_app.tour_list"))

# Tour Recommendation routes

@public_app.route("/rekomendasi-wisata", methods=["GET", "POST"])
@login_required
def tour_recommendation():
  form = TourRecommendation1Form()

  if form.validate_on_submit():
    session["location_point"] = form.location_point.data
    session["tour_type"] = form.tour_type.data
    session["form1_filled"] = True 
    return redirect(url_for("public_app.tour_recommendation_sub_criteria"))

  return render_template("public/services/tour_recommendation/tour-recommendation-1.html", title="Rekomendasi Wisata - Development", form=form)

@public_app.route("/rekomendasi-wisata/sub-kriteria", methods=["GET", "POST"])
@login_required
def tour_recommendation_sub_criteria():
  if not session.get("form1_filled"):
    return redirect(url_for("public_app.tour_recommendation"))

  form = TourRecommendation2Form()

  if form.validate_on_submit():
    location_point = session.get("location_point")
    tour_type = session.get("tour_type")
    ticket = form.ticket.data
    facility = form.facility.data
    distance = form.distance.data
    infrastructure = form.infrastructure.data
    transportation_access = form.transportation_access.data


    # Get the tour type based on the list -> 1.Alam,  2.Pemandian,  3.Sejarah

    # Get the distance from the location point

    # Filter the C1-C5 to match the form

    # Get the list of the metrics

    # Get the avg_weight of each Cs
    avg_weight = [0.1887, 0.1711, 0.2332, 0.1098, 0.2973]
    
    # weight type, 1 is for cost, 2 is for benefit
    weight_type = [1,2,1,2,2]

    filtered_np_list = np.array([
          [3.00, 4.00, 1.00, 5.00, 3.00],
          [3.00, 5.00, 6.00, 5.00, 3.00],
          [2.00, 4.00, 1.00, 5.00, 3.00],
          [3.00, 4.00, 2.00, 5.00, 3.00],
          [3.00, 5.00, 1.00, 5.00, 3.00],
          [2.00, 5.00, 3.00, 5.00, 3.00],
          [2.00, 4.00, 2.00, 5.00, 3.00],
          [4.00, 4.00, 2.00, 5.00, 3.00],
          [3.00, 4.00, 1.00, 5.00, 3.00],
          [2.00, 4.00, 3.00, 5.00, 3.00]
    ])

    list_names = ["Pemandian Alam Tasnan",
                  "Pemandian Air Panas Blawan",
                  "Pemandian Al-Amin",
                  "Pemandian WOW Klabang",
                  "Navara Water Park",
                  "Wisata Tirta Agung",
                  "Wisata Bukit Luwih",
                  "Bosamba Rafting",
                  "Pemandian Kharisma",
                  "Teduh Glamping"
                  ]

    preference_metric = process_input_list_based_on_weight(filtered_np_list, np.array(avg_weight), weight_type)

    # Pair the values with their ids
    paired_list = list(zip(preference_metric, list_names))

    # Sort the paired list based on the values
    sorted_paired_list = sorted(paired_list, reverse=True)
    print(sorted_paired_list)

    # Get the top 3 biggest numbers along with their ids
    top_3_paired_list = sorted_paired_list[:3]

    # Convert to dictionary format
    # top_3_dict = {id: value for value, id in top_3_paired_list}
    
  
    session.pop("location_point", None)
    session.pop("ticket_price", None)
    session.pop("form1_filled", None)

    result = [{"ranking": str(rank), "score": str(int(value * 100)), "tour_object": id} 
               for rank, (value, id) in enumerate(top_3_paired_list, start=1)]

    return render_template("public/services/tour_recommendation/tour-recommendation_result.html", title="Rekomendasi Wisata - Development", result=result)

  return render_template("public/services/tour_recommendation/tour-recommendation-2.html", title="Rekomendasi Wisata - Development", form=form)