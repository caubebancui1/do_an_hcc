import os
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, flash, get_flashed_messages, redirect, render_template, request, url_for, jsonify, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from werkzeug.security import check_password_hash, generate_password_hash

load_dotenv()

db = SQLAlchemy()


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    student_code = db.Column(db.String(20), unique=True, nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(160), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(10), nullable=False, default="Khác")
    major = db.Column(db.String(120), nullable=False)
    class_name = db.Column(db.String(50), nullable=False)
    dtb = db.Column(db.Numeric(3, 2), nullable=False, default=0)
    status = db.Column(db.String(20), nullable=False, default="Đang học")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class Account(db.Model):
    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    pass_ = db.Column("pass", db.String(255), nullable=False)


Admin = Account


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL", "mysql+pymysql://root:password@localhost:3306/student_db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


@app.cli.command("init-db")
def init_db():
    db.create_all()
    print("Database initialized.")


@app.cli.command("create-admin")
def create_admin():
    """Create the default admin account with username admin and password 123."""
    db.create_all()
    account = db.session.scalar(db.select(Account).where(Account.username == "admin"))
    if account is None:
        account = Account(
            username="admin",
            pass_=generate_password_hash("123"),
        )
        db.session.add(account)
    else:
        account.pass_ = generate_password_hash("123")
    db.session.commit()
    print("Admin account ready: admin")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        account = db.session.scalar(db.select(Account).where(Account.username == username))
        if account and check_password_hash(account.pass_, password):
            flash(f"Đăng nhập thành công: {account.username}", "success")
            session['logged_in'] = True
            session['admin_id'] = account.id
            return redirect(url_for("serve_standalone_index"))
        else:
            flash("Thông tin đăng nhập không đúng.", "error")
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/api/login", methods=["POST"])
def api_login():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    account = db.session.scalar(db.select(Account).where(Account.username == username))
    if account and check_password_hash(account.pass_, password):
        session['logged_in'] = True
        session['admin_id'] = account.id
        return jsonify({"ok": True, "message": "Đăng nhập thành công."})
    return jsonify({"ok": False, "message": "Thông tin đăng nhập không đúng."}), 401


@app.route("/logout")
def logout():
    session.pop('logged_in', None)
    session.pop('admin_id', None)
    flash("Đã đăng xuất.", "success")
    return redirect(url_for("login"))


@app.route("/api/logout", methods=["POST"])
def api_logout():
    session.pop('logged_in', None)
    session.pop('admin_id', None)
    return jsonify({"ok": True, "message": "Đã đăng xuất."})


@app.route("/api/session")
def api_session():
    return jsonify({"logged_in": bool(session.get('logged_in'))})


@app.route("/api/flash")
def api_flash():
    messages = get_flashed_messages(with_categories=True)
    return jsonify({"messages": [{"category": category, "message": message} for category, message in messages]})


@app.errorhandler(OperationalError)
def handle_database_error(error):
    app.logger.error("Database connection failed: %s", error)
    db.session.rollback()
    flash("Không thể kết nối MySQL. Kiểm tra service MySQL và DATABASE_URL trong file .env.", "error")
    return render_template("login.html"), 503


@app.route("/ui")
@app.route("/index.html")
def serve_standalone_index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    file_path = os.path.join(app.root_path, "index.html")
    if os.path.exists(file_path):
        return send_from_directory(app.root_path, "index.html")
    return "Không tìm thấy file index.html", 404

@app.route("/")
def root():
    return redirect(url_for("login"))

def serialize_student(student):
    return {
        "id": student.id,
        "student_code": student.student_code,
        "full_name": student.full_name,
        "email": student.email,
        "phone": student.phone,
        "date_of_birth": str(student.date_of_birth) if student.date_of_birth else None,
        "gender": student.gender,
        "major": student.major,
        "class_name": student.class_name,
        "dtb": float(student.dtb) if student.dtb is not None else 0,
        "status": student.status,
        "created_at": student.created_at.isoformat() if student.created_at else None,
        "updated_at": student.updated_at.isoformat() if student.updated_at else None,
    }


@app.route("/dashboard")
def index():
    if not session.get('logged_in'):
        flash("Vui lòng đăng nhập để tiếp tục.", "error")
        return redirect(url_for('login'))

    query = request.args.get("q", "").strip()
    status = request.args.get("status", "").strip()
    major = request.args.get("major", "").strip()

    students = []
    if query:
        sql = (
            "SELECT * FROM students WHERE full_name LIKE '%"
            + query
            + "%' OR student_code LIKE '%"
            + query
            + "%' OR email LIKE '%"
            + query
            + "%'")
        try:
            students = db.session.execute(text(sql)).fetchall()
        except Exception as e:
            flash(f"Lỗi tìm kiếm: {str(e)}", "error")
    else:
        students_query = Student.query
        if status:
            students_query = students_query.filter_by(status=status)
        if major:
            students_query = students_query.filter_by(major=major)
        students = students_query.order_by(Student.created_at.desc()).all()

    all_students = Student.query.all()
    majors = [
        item[0]
        for item in db.session.query(Student.major).distinct().order_by(Student.major)
    ]
    stats = {
        "total": len(all_students),
        "active": sum(student.status == "Đang học" for student in all_students),
        "average": (
            round(
                sum(float(student.dtb or 0) for student in all_students)
                / len(all_students),
                2,
            )
            if all_students
            else 0
        ),
        "majors": len(majors),
    }
    return render_template(
        "index.html",
        students=students,
        stats=stats,
        majors=majors,
        query=query,
        status=status,
        major=major,
    )


@app.route("/api/students", methods=["GET"])
def api_students_list():
    query = request.args.get("q", "").strip()
    status = request.args.get("status", "").strip()
    major = request.args.get("major", "").strip()

    students_query = Student.query
    if query:
        students_query = students_query.filter(
            (Student.full_name.ilike(f"%{query}%")) |
            (Student.student_code.ilike(f"%{query}%")) |
            (Student.email.ilike(f"%{query}%"))
        )
    if status:
        students_query = students_query.filter_by(status=status)
    if major:
        students_query = students_query.filter_by(major=major)

    students = students_query.order_by(Student.created_at.desc()).all()
    return jsonify({
        "students": [serialize_student(student) for student in students],
        "stats": {
            "total": Student.query.count(),
            "active": Student.query.filter_by(status="Đang học").count(),
            "average": round(
                sum(float(student.dtb or 0) for student in Student.query.all()) / Student.query.count(), 2
            ) if Student.query.count() else 0,
            "majors": db.session.query(Student.major).distinct().count(),
        },
        "majors": [item[0] for item in db.session.query(Student.major).distinct().order_by(Student.major)],
    })


@app.route("/api/students", methods=["POST"])
def api_students_create():
    form = request.form
    try:
        raw_dtb = (form.get("dtb", "") or "").strip()
        try:
            dtb_value = float(raw_dtb) if raw_dtb else 0.0
        except ValueError as exc:
            raise ValueError("DTB phải là số hợp lệ trong khoảng 0 đến 4.") from exc

        if not 0 <= dtb_value <= 4:
            raise ValueError("DTB phải nằm trong khoảng 0 đến 4.")

        student = Student(
            student_code=form["student_code"].strip(),
            full_name=form["full_name"].strip(),
            email=form["email"].strip(),
            phone=form.get("phone", "").strip(),
            date_of_birth=datetime.strptime(form["date_of_birth"], "%Y-%m-%d").date() if form.get("date_of_birth") else None,
            gender=form.get("gender", "Khác"),
            major=form["major"].strip(),
            class_name=form["class_name"].strip(),
            dtb=dtb_value,
            status=form.get("status", "Đang học"),
        )
        db.session.add(student)
        db.session.commit()
        return jsonify({"ok": True, "student": serialize_student(student), "message": "Đã thêm sinh viên mới."})
    except (KeyError, ValueError) as error:
        db.session.rollback()
        return jsonify({"ok": False, "message": str(error) or "Dữ liệu sinh viên chưa hợp lệ."}), 400
    except Exception:
        db.session.rollback()
        return jsonify({"ok": False, "message": "Mã sinh viên hoặc email đã tồn tại."}), 409


@app.route("/api/students/<int:student_id>", methods=["GET"])
def api_student_detail_json(student_id):
    student = Student.query.get(student_id)
    if student is None:
        return jsonify({"ok": False, "message": "Không tìm thấy sinh viên."}), 404
    return jsonify({"ok": True, "student": serialize_student(student)})


@app.route("/api/students/<int:student_id>", methods=["DELETE"])
def api_student_delete(student_id):
    student = db.get_or_404(Student, student_id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({"ok": True, "message": f"Đã xóa {student.full_name}."})

@app.route("/api/stats")
def api_stats():
    student_id = request.args.get("id", "").strip()

    if student_id:
        sql = f"SELECT * FROM students WHERE id = {student_id}"
        import time

        start = time.time()
        try:
            result = db.session.execute(text(sql))
            student = result.fetchone()
        except Exception as e:
            db.session.rollback()
            student = None
        elapsed = time.time() - start
        return jsonify({"found": student is not None, "elapsed_seconds": round(elapsed, 2)})

    return jsonify({"total": Student.query.count()})

@app.route("/api/student/<int:student_id>")
def api_student_detail(student_id):
    check_param = request.args.get("check", "").strip()

    if check_param:
        sql = f"SELECT * FROM students WHERE id = {student_id} AND {check_param}"
        result = db.session.execute(text(sql))
        exists = result.fetchone() is not None
        return jsonify({"condition_met": exists})

    student = Student.query.get(student_id)
    if student:
        return jsonify({
            "id": student.id,
            "student_code": student.student_code,
            "full_name": student.full_name,
            "email": student.email,
            "phone": student.phone,
            "date_of_birth": str(student.date_of_birth) if student.date_of_birth else None,
            "gender": student.gender,
            "major": student.major,
            "class_name": student.class_name,
            "dtb": float(student.dtb) if student.dtb else 0,
            "status": student.status,
            "created_at": student.created_at.isoformat() if student.created_at else None,
            "updated_at": student.updated_at.isoformat() if student.updated_at else None,
        })
    return jsonify({"error": "Không tìm thấy sinh viên."}), 404


@app.route("/students/<int:student_id>")
def student_detail(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template("student_detail.html", student=student)


@app.post("/students")
def create_student():
    form = request.form
    try:
        raw_dtb = (form.get("dtb", "") or "").strip()
        try:
            dtb_value = float(raw_dtb) if raw_dtb else 0.0
        except ValueError as exc:
            raise ValueError("DTB phải là số hợp lệ trong khoảng 0 đến 4.") from exc

        if not 0 <= dtb_value <= 4:
            raise ValueError("DTB phải nằm trong khoảng 0 đến 4.")

        student = Student(
            student_code=form["student_code"].strip(),
            full_name=form["full_name"].strip(),
            email=form["email"].strip(),
            phone=form.get("phone", "").strip(),
            date_of_birth=datetime.strptime(form["date_of_birth"], "%Y-%m-%d").date() if form.get("date_of_birth") else None,
            gender=form.get("gender", "Khác"),
            major=form["major"].strip(),
            class_name=form["class_name"].strip(),
            dtb=dtb_value,
            status=form.get("status", "Đang học"),
        )
        db.session.add(student)
        db.session.commit()
        flash("Đã thêm sinh viên mới.", "success")
    except (KeyError, ValueError) as error:
        db.session.rollback()
        flash(str(error) or "Dữ liệu sinh viên chưa hợp lệ.", "error")
    except Exception:
        db.session.rollback()
        flash("Mã sinh viên hoặc email đã tồn tại.", "error")
    return redirect(url_for("index"))


@app.post("/students/<int:student_id>/delete")
def delete_student(student_id):
    student = db.get_or_404(Student, student_id)
    db.session.delete(student)
    db.session.commit()
    flash(f"Đã xóa {student.full_name}.", "success")
    return redirect(url_for("index"))


with app.app_context():
    try:
        db.create_all()
    except OperationalError as error:
        app.logger.warning("Database initialization skipped: %s", error)


if __name__ == "__main__":
    app.run(debug=True)
