# Import Flask tools
from flask import Blueprint, render_template, request, redirect, url_for, flash

# For login-required pages
from flask_login import login_required, current_user

# Database + models
from app import db
from app.models import Course, Module, ModuleNote

# Forms
from app.forms import ModuleNoteForm


# --------------------------------------------
# Create Blueprint
# --------------------------------------------
main_bp = Blueprint("main", __name__, template_folder="templates")


# --------------------------------------------
# Route 1: Home page ('/')
# --------------------------------------------
@main_bp.route("/")
def index():
    return render_template("main/index.html")


# --------------------------------------------
# Route 2: Feature demo page ('/feature')
# --------------------------------------------
@main_bp.route("/feature")
def feature():
    return render_template("main/feature.html")


# --------------------------------------------
# Route 3: Course Detail Page (with notes support)
# --------------------------------------------
@main_bp.route("/courses/<int:course_id>", methods=["GET", "POST"])
@login_required
def course_detail(course_id):

    # Get course or 404
    course = Course.query.get_or_404(course_id)

    # For simplicity in M2, use the first module as the "current" module
    current_module = course.modules[0] if course.modules else None

    form = ModuleNoteForm()
    module_note = None

    if current_module:
        # Look for an existing note for this user + module
        module_note = ModuleNote.query.filter_by(
            user_id=current_user.id,
            module_id=current_module.id
        ).first()

        # -----------------------
        # Handle saving notes (POST)
        # -----------------------
        if form.validate_on_submit():
            if module_note is None:
                module_note = ModuleNote(
                    user_id=current_user.id,
                    module_id=current_module.id,
                    content=form.content.data,
                )
                db.session.add(module_note)
            else:
                module_note.content = form.content.data

            db.session.commit()
            flash("Notes saved.", "success")
            return redirect(url_for("main.course_detail", course_id=course_id))

        # -----------------------
        # Pre-fill form on GET
        # -----------------------
        elif request.method == "GET" and module_note is not None:
            form.content.data = module_note.content

    # ---------------------------------
    # M2 fake demo progress (can be replaced by Jacob's real progress)
    # ---------------------------------
    course_name = course.title if hasattr(course, "title") else "Course"
    status = "completed"       # Demo value
    status_label = "Completed"
    progress_percent = 100
    completion_date = "Nov 26, 2025"

    return render_template(
        "main/course_detail.html",
        course=course,
        current_module=current_module,
        form=form,
        module_note=module_note,
        course_name=course_name,
        status=status,
        status_label=status_label,
        progress_percent=progress_percent,
        completion_date=completion_date,
    )

