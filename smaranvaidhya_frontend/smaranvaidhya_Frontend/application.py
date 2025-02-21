from flask import Flask,render_template,request,url_for,jsonify,json,session,redirect,Response
from flask_cors import CORS,cross_origin
import json
import requests
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
import base64

app = Flask(__name__)
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = True
app.secret_key = 'This_is_very_secret'
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, id, email, user_type):
        self.id = id
        self.email = email
        self.user_type = user_type

@login_manager.user_loader
def load_user(user_id):
    if 'user_id' in session:
        return User(session['user_id'], session['email'], session['user_type'])
    return None

def get_logged_in_user():
    user_login = False
    user_logged_in = None
    email = session.get('email')
    user_type = session.get('user_type')
    user_id = session.get('user_id')
    if email and user_type and user_id:
        user_login = True
        user_logged_in = {
            "email": email,
            "user_type": user_type,
            "user_id": user_id
        }
    return user_login, user_logged_in

@app.route('/Homepage')
def Homepage():
    user_login = get_logged_in_user()
    return render_template('homePage.html',user_login = user_login)

@app.route('/bookAppointment')
@login_required
def bookAppointment():
    user_login = get_logged_in_user()
    user_info = session.get('email')
    user_type = session.get('user_type')
    return render_template('bookAppointment.html',user_login = user_login,user_type = user_type,user_info = user_info)

@app.route('/confirmBooking')
@login_required
def confirmBooking():
    user_login = get_logged_in_user()
    user_info = session.get('email')
    user_type = session.get('user_type')
    return render_template('confirmBooking.html',user_login = user_login,user_type = user_type,user_info = user_info)

@app.route('/patientLoginPage')
def patientLoginPage():
    user_login, user_info = get_logged_in_user()
    user_id = session.get('user_id') if user_login else None
    return render_template('patientLoginPage.html', user_login=user_login, user_id=user_id,user_info=user_info)

@app.route('/aboutPage')
def aboutPage():
    user_login = get_logged_in_user()
    return render_template('aboutPage.html',user_login = user_login)

@app.route('/contactUsPage')
def contactUsPage():
    user_login = get_logged_in_user()
    return render_template('contactUsPage.html',user_login = user_login)

@app.route('/doctorsInfo')
@login_required
def doctorsInfo():
    user_login = get_logged_in_user()
    user_info = session.get('email')
    user_type = session.get('user_type')
    return render_template('doctorsInfo.html',user_login = user_login,user_type = user_type,user_info = user_info)

@app.route('/doctorsView')
@login_required
def doctorsView():
    user_login = get_logged_in_user()
    user_info = session.get('email')
    user_type = session.get('user_type')
    return render_template('doctorView.html',user_login = user_login,user_type = user_type,user_info = user_info)

@app.route('/Profile')
@login_required
def userProfile():
    user_login = get_logged_in_user()
    user_info = session.get('email')
    user_type = session.get('user_type')
    return render_template('profile.html',user_login = user_login,user_type = user_type,user_info = user_info)

@app.route('/patientHistory')
@login_required
def patientHistory():
    user_login = get_logged_in_user()
    user_info = session.get('email')
    user_type = session.get('user_type')
    return render_template('patientHistory.html',user_login = user_login,user_type = user_type,user_info = user_info)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('patientLoginPage'))

def post_api_function(url, data):
    response = ''
    try:
        response = requests.post(url, json=data)
        print(response)
    except Exception as e:
        print('An exception', e,'Occured')
    return response

def get_api_function(url):
    response = ''
    try:
        response = requests.get(url)
        print(response)
    except Exception as e:
        print('An exception', e,'Occured')
    return response

def get_service_url():
    return 'http://127.0.0.1:2000'

@app.route('/attempt_to_login_for_user', methods=['POST'])
def attempt_to_login_for_user():
    url = get_service_url() + '/attempt_to_login_for_user'
    request_data = request.json
    response = requests.post(url, json=request_data)
    response_data = response.json()
    print("Login Response Data:", response_data)  
    if response_data["status"] == "Login Successful":
        if "user_id" not in response_data:
            return jsonify({"status": "error", "message": "User ID missing in response"}), 500
        session["email"] = request_data["email"]
        session["user_type"] = request_data["user_login_type"]
        session["user_id"] = response_data["user_id"]
        user = User(request_data["email"], response_data["user_id"], request_data["user_login_type"])
        login_user(user)
    else:
        session.clear()
    return jsonify(response_data)

@app.route('/save_user_registration_details', methods=['POST'])
def save_user_registration_details():
    url = get_service_url() + '/save_user_registration_details'
    request_data = request.json
    print(request_data)
    response = post_api_function(url, request_data)
    return response.json() if response else jsonify({"status": "error", "message": "Server error."})

@app.route('/post_contact_us_data', methods=['POST'])   
def post_contact_us_data():
    url = get_service_url() + '/post_contact_us_data'
    request_data = request.json
    print(request_data)
    response = post_api_function(url, request_data)
    return response.json() if response else jsonify({"status": "error", "message": "Server error."})

@app.route('/post_doctor_information_data', methods=['POST'])
def post_doctor_information_data():
    url = get_service_url() + '/post_doctor_information_data'
    form_data = request.form.to_dict()
    if 'doctor_image' in request.files:
        image_file = request.files['doctor_image']
        form_data['doctor_image'] = base64.b64encode(image_file.read()).decode('utf-8')
    response = post_api_function(url, form_data)
    return response.json() if response else jsonify({"status": "error", "message": "Server error."})

@app.route('/get_doctor_data', methods=['GET'])
def get_doctor_data():
    url = get_service_url() + '/get_doctor_data'
    response = get_api_function(url)
    return json.dumps(response.json())

@app.route('/post_appointment_booking_data', methods=['POST'])
def post_appointment_booking_data():
    # Check if the user is logged in
    if 'user_id' not in session:
        return jsonify({"status": "error", "message": "User not logged in"}), 401

    # Get the JSON data from the request
    request_data = request.get_json()
    if not request_data:
        return jsonify({"status": "error", "message": "No data received"}), 400

    # Add the patient_id from the session
    request_data['patient_id'] = session['user_id']

    # Forward the data to the backend
    url = get_service_url() + '/post_appointment_booking_data'
    response = post_api_function(url, request_data)

    # Return the response from the backend
    if response:
        return jsonify(response.json()), response.status_code
    else:
        return jsonify({"status": "error", "message": "Backend server error"}), 500


@app.route('/get_doctor_view_data', methods=['GET'])
def get_doctor_view_data():
    user_login, user_logged_in = get_logged_in_user()
    if not user_login:
        return jsonify({'error': 'User not logged in'}), 401
    doctor_id = user_logged_in["user_id"]
    if not doctor_id:
        return jsonify({'error': 'Doctor ID not found'}), 400
    url = get_service_url() + f'/get_doctor_view_data?doctor_id={doctor_id}'
    response = get_api_function(url)
    return jsonify(response.json())  

@app.route('/get_user_profile', methods=['GET'])
def get_user_profile():
    user_login, user_logged_in = get_logged_in_user()
    if not user_login:
        return jsonify({'error': 'User not logged in'}), 401
    user_id = user_logged_in.get("user_id")  
    if not user_id:
        return jsonify({'error': 'Patient ID not found'}), 400
    url = get_service_url() + f'/get_user_profile?user_id={user_id}'
    response = get_api_function(url)
    if response.status_code == 200:
        return jsonify(response.json())  
    else:
        return jsonify({'error': 'Failed to fetch user profile'}), response.status_code

@app.route('/update_user_profile/<user_id>', methods=['PUT'])
def update_user_profile(user_id):
    user_login, user_logged_in = get_logged_in_user()
    if not user_login:
        return jsonify({'error': 'User not logged in'}), 401
    user_id = request.view_args.get("user_id")  
    data = request.get_json(silent=True)
    url = get_service_url() + f'/update_user_profile/{user_id}'
    headers = {"Content-Type": "application/json"}
    response = requests.put(url, json=data, headers=headers)
    if response.status_code == 200:
        return jsonify(response.json())
    return jsonify({'error': response.json().get('detail', 'Update failed')}), response.status_code

@app.route('/get_user_history', methods=['GET'])
def get_user_history():
    user_login, user_logged_in = get_logged_in_user()
    if not user_login:
        return jsonify({'error': 'User not logged in'}), 401
    user_id = user_logged_in.get("user_id")  
    if not user_id:
        return jsonify({'error': 'Patient ID not found'}), 400
    url = get_service_url() + f'/get_user_history?user_id={user_id}'
    response = get_api_function(url)
    if response.status_code == 200:
        return jsonify(response.json())  
    else:
        return jsonify({'error': 'Failed to fetch user profile'}), response.status_code

if __name__ == '__main__':
    app.run(debug=True, port=7078)



