from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, EmailField
from wtforms.validators import DataRequired, Email, Length
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "change-this-before-deploying")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///codecraft.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER", "")
app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", "587"))
app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS", "true").lower() == "true"
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME", "")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD", "")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER", app.config["MAIL_USERNAME"] or "noreply@example.com")

db = SQLAlchemy(app)
mail = Mail(app)

class Inquiry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(30))
    service = db.Column(db.String(100), nullable=False)
    budget = db.Column(db.String(50))
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(30), default="New", nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

class ContactForm(FlaskForm):
    name = StringField("Your name", validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField("Email address", validators=[DataRequired(), Email(), Length(max=150)])
    phone = StringField("Phone / WhatsApp (optional)", validators=[Length(max=30)])
    service = SelectField("What do you need?", choices=[
        ("Business website", "Business website"),
        ("Portfolio website", "Portfolio website"),
        ("Custom web application", "Custom web application"),
        ("Flask / Python project", "Flask / Python project"),
        ("Website redesign", "Website redesign"),
        ("Maintenance and support", "Maintenance and support"),
        ("Other", "Other")
    ], validators=[DataRequired()])
    budget = SelectField("Approximate budget", choices=[
        ("Not sure yet", "Not sure yet"),
        ("Under ₹3,000", "Under ₹3,000"),
        ("₹3,000–₹8,000", "₹3,000–₹8,000"),
        ("₹8,000–₹15,000", "₹8,000–₹15,000"),
        ("₹15,000+", "₹15,000+")
    ])
    message = TextAreaField("Tell us about your idea", validators=[DataRequired(), Length(min=10, max=3000)])

@app.context_processor
def inject_globals():
    return {"business_name": "CodeCraft Technologies"}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/projects")
def projects():
    return render_template("projects.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        inquiry = Inquiry(
            name=form.name.data.strip(),
            email=form.email.data.strip(),
            phone=(form.phone.data or "").strip(),
            service=form.service.data,
            budget=form.budget.data,
            message=form.message.data.strip()
        )
        db.session.add(inquiry)
        db.session.commit()
        # Email notifications are optional; the inquiry is still saved if email isn't configured.
        if app.config["MAIL_SERVER"] and app.config["MAIL_USERNAME"] and app.config["MAIL_PASSWORD"]:
            try:
                msg = Message(
                    subject=f"New CodeCraft inquiry: {inquiry.service}",
                    recipients=[os.getenv("INQUIRY_EMAIL", app.config["MAIL_USERNAME"])],
                    body=f"Name: {inquiry.name}\nEmail: {inquiry.email}\nPhone: {inquiry.phone}\nService: {inquiry.service}\nBudget: {inquiry.budget}\n\nMessage:\n{inquiry.message}"
                )
                mail.send(msg)
            except Exception:
                app.logger.exception("Inquiry saved, but notification email could not be sent.")
        flash("Thanks! Your inquiry has been received. We'll get back to you soon.", "success")
        return redirect(url_for("contact"))
    return render_template("contact.html", form=form)

@app.errorhandler(404)
def not_found(_error):
    return render_template("404.html"), 404

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "true").lower() == "true")
