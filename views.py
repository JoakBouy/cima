from flask import Blueprint, render_template, redirect, url_for
import requests
from flask import request, flash
from flask_login import login_required, current_user
from create_app import db

from models.base_model import Appointment

views = Blueprint('views', __name__)


@views.route('/')
def index():  # put application's code here
    appointments = Appointment.query.all()
    return render_template('index.html', user=current_user, appointments=appointments)


@views.route('/dashboard')
@login_required
def dashboard():
    appointments = Appointment.query.filter_by(user=current_user).all()
    return render_template("dashboard.html", appointments=appointments)


@views.route('/resource')
def resource():
    # Render the HTML template with the health topics
    selected_country = "ng"  # Replace with the desired country code
    news_articles = fetch_health_news(selected_country)
    return render_template('resources.html', news_articles=news_articles)


import requests


def fetch_health_news(selected_country):
    api_key = "9ea9960aac454f649e6fa5d78e9343be"
    api_url = f"https://newsapi.org/v2/top-headlines?category=health&country={selected_country}&apiKey={api_key}"

    try:
        response = requests.get(api_url)
        data = response.json()

        news_articles = []

        for article in data.get("articles", []):
            title = article.get("title", "")
            description = article.get("description", "")
            source = article.get("source", {}).get("name", "")
            url = article.get("url", "")

            news_articles.append({
                "title": title,
                "description": description,
                "source": source,
                "url": url
            })

        return news_articles

    except Exception as e:
        print("Error fetching data:", e)
        return []


# selected_country = "ng"
# news_articles = fetch_health_news(selected_country)

# for article in news_articles:
#     print("Title:", article["title"])
#     print("Description:", article["description"])
#     print("Source:", article["source"])
#     print("URL:", article["url"])
#     print("\n")


@views.route('/appointment', methods=['GET', 'POST'])
@login_required
def appointment():
    if request.method == 'POST':
        try:
            full_name = request.form.get('full_name')
            dehydration = request.form.get('dehydration', '0')  # Default to '0' if not provided
            vomiting = request.form.get('vomiting', '0')  # Default to '0' if not provided
            diarrhea = request.form.get('diarrhea', '0')  # Default to '0' if not provided
            abdominal_pain = request.form.get('abdominal_pain', '0')  # Default to '0' if not provided
            symptom_count = request.form.get('symptom_count', 0)  # Default to 0 if not provided
            phone_number = request.form.get('phone_number')
            note = request.form.get('note')

            # Validate form data
            if not full_name or not phone_number or not note:
                flash('Please fill in all required fields.', category='error')
                return redirect(url_for('views.appointment'))

            # Map "Yes" to 1 and "No" to 0 for relevant fields
            dehydration_int = 1 if dehydration.lower() == "yes" else 0
            vomiting_int = 1 if vomiting.lower() == "yes" else 0
            diarrhea_int = 1 if diarrhea.lower() == "yes" else 0
            abdominal_pain_int = 1 if abdominal_pain.lower() == "yes" else 0

            # Create a new Appointment instance and add it to the database
            appointment = Appointment(
                full_name=full_name,
                dehydration=dehydration,
                vomiting=vomiting,
                diarrhea=diarrhea,
                abdominal_pain=abdominal_pain,
                symptom_count=symptom_count,
                phone_number=phone_number,
                note=note,
                user=current_user  # Assuming you have a user relationship in Appointment model
            )

            # Make a request to FastAPI endpoint for model prediction
            fastapi_url = "http://localhost:8000/predict"
            payload = {
                "dehydration": 1,
                "vomiting": 0,
                "diarrhea": 1,
                "abdominal_pain": 1,
                "symptom_count": 3,
            }

            response = requests.post(fastapi_url, json=payload)
            print(payload)
            response = requests.post(fastapi_url, json=payload)

            if response.status_code == 200:
                diagnosis = response.json().get("diagnosis")
                appointment.diagnosis = diagnosis  # Assuming you have a 'diagnosis' column in your Appointment model
                flash(f'Diagnosis: {diagnosis}', category='success')
            else:
                flash('Error getting diagnosis.', category='error')

            db.session.add(appointment)
            db.session.commit()

            flash('Symptom diagnosis submitted successfully.', category='success')
            return redirect(url_for('views.dashboard'))

        except Exception as e:
            flash(f'Error: {e}', category='error')
            app.logger.error(f"Error in appointment route: {e}")
            return redirect(url_for('views.appointment'))

    return render_template('appointment.html', user=current_user)





@views.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@views.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
