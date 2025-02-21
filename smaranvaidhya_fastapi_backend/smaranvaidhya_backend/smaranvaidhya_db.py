import psycopg2
import json
import psycopg2.extras
from datetime import datetime
from sqlalchemy.orm import Session  

def connection():
        conn = psycopg2.connect(
                database="healthcare_db", user='healthcare_user', password='12345678', host='127.0.0.1', port= '5432'
        )
        return conn

def validate_login_details(login_data):
        conn = connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        valid_user = False
        user_id = None  
        email = login_data["email"]
        user_type = login_data["user_login_type"]
        try:
                if user_type == "patient":
                        QUERY = "SELECT patient_id, email, password FROM smaranvaidhya.patient_login WHERE email = %s"
                elif user_type == "doctor":
                        QUERY = "SELECT doctor_id, email, password FROM smaranvaidhya.doctor_login WHERE email = %s"
                elif user_type == "admin":
                        QUERY = "SELECT admin_id, email, password FROM smaranvaidhya.admin_login WHERE email = %s"
                else:
                        return valid_user, None
                cursor.execute(QUERY, (email,))
                reg_records = cursor.fetchall()
                for row in reg_records:
                        if login_data["email"] == row["email"] and login_data["password"] == row["password"]:
                                valid_user = True
                                user_id = row["patient_id"] if user_type == "patient" else row["doctor_id"] if user_type == "doctor" else row["admin_id"]
        except Exception as e:
                print("Error:", str(e))
        finally:
                if conn:
                        cursor.close()
                        conn.close()
        return valid_user, user_id  

def save_user_registration_details(request_data):
        conn = connection()
        cursor = conn.cursor()
        try:
                QUERY1 = '''
                SELECT count(patient_id) FROM smaranvaidhya.patient_registration
                '''
                reg_result = cursor.execute(QUERY1)
                reg_records = cursor.fetchall()
                for row in reg_records:
                        no_of_patients = row[0]
                patients_reg_no = ''
                if(no_of_patients < 9):
                        patients_id_no = 'P' + '00' + str(no_of_patients+1)
                elif(no_of_patients < 99):
                        patients_id_no = 'P' + '0' + str(no_of_patients+1)
                else:
                        patients_id_no = 'P' + str(no_of_patients+1)
                print(patients_id_no)
                current_date = datetime.now().date()
                formatted_date = current_date.strftime('%Y-%m-%d')
                print("formmatted date" ,formatted_date )

                INSERT_QUERY = '''
                        INSERT INTO smaranvaidhya.patient_registration(
                        patient_id,
                        first_name,
                        last_name,  
                        date_of_birth,
                        gender,
                        email,
                        phone_number,
                        password,
                        state,
                        city,
                        zip_code,
                        registration_date
                        ) 
                        VALUES('{}','{}', '{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')'''.format(
                                patients_id_no,
                                request_data['first_name'],
                                request_data['last_name'],
                                request_data['date_of_birth'],
                                request_data['gender'],
                                request_data['email'],
                                request_data['phone_number'],
                                request_data['password'],
                                request_data['state'],
                                request_data['city'],
                                request_data['zip_code'],
                                formatted_date
                        )
                print(INSERT_QUERY)
                cursor.execute(INSERT_QUERY)
                conn.commit()
                INSERT_QUERY1 = '''
                        INSERT INTO smaranvaidhya.patient_login(
                        patient_id,
                        email,
                        password
                        ) 
                        VALUES('{}','{}','{}')'''.format(
                                patients_id_no,
                                request_data['email'],
                                request_data['password']
                        )
                cursor.execute(INSERT_QUERY1)
                conn.commit()
        except Exception as e:
                print("Error", str(e), "Occurred")
        finally:
                if conn:
                        cursor.close()
                        conn.close()
        return "Success"

def post_contact_us_data(request_data):
        conn = connection()
        cursor = conn.cursor()
        try:
                INSERT_QUERY = '''
                        INSERT INTO smaranvaidhya.contact_us_data(
                        full_name,
                        email,
                        message 
                        ) 
                        VALUES('{}','{}', '{}')'''.format(
                                request_data['full_name'],
                                request_data['email'],
                                request_data['message'],
                        )
                print(INSERT_QUERY)
                cursor.execute(INSERT_QUERY)
                conn.commit()
        except Exception as e:
                print("Error", str(e), "Occurred")
        finally:
                if conn:
                        cursor.close()
                        conn.close()
        return "Success"

def post_doctor_information_data(request_data):
        conn = connection()  
        cursor = conn.cursor()
        try:
                QUERY1 = '''
                        SELECT count(id) FROM smaranvaidhya.doctor_information
                        '''
                reg_result = cursor.execute(QUERY1)
                reg_records = cursor.fetchall()
                for row in reg_records:
                        no_of_doctors = row[0]
                doctor_id_no = ''
                if no_of_doctors < 9:
                        doctor_id_no = 'D' + '00' + str(no_of_doctors + 1)
                elif no_of_doctors < 99:
                        doctor_id_no = 'D' + '0' + str(no_of_doctors + 1)
                else:
                        doctor_id_no = 'D' + str(no_of_doctors + 1)
                print(doctor_id_no)
                current_date = datetime.now().date()
                formatted_date = current_date.strftime('%Y-%m-%d')
                print("formatted date", formatted_date)

                INSERT_QUERY = '''
                        INSERT INTO smaranvaidhya.doctor_information (
                        id,
                        first_name,
                        last_name,
                        date_of_birth,
                        gender,
                        email,
                        phone_number,
                        state,
                        city,
                        zip_code,
                        clinic_hospital,
                        specialist,
                        available_from,
                        available_to,
                        time_per_patient,
                        max_appointments,
                        highest_qualification,
                        years_of_experience,
                        in_person_fee,
                        video_fee,
                        phone_fee,
                        emergency_availability,
                        emergency_contact,
                        doctor_image,
                        hospital_clinic_address,
                        monday, 
                        tuesday,
                        wednesday,
                        thursday,
                        friday,
                        saturday,
                        sunday,
                        upi_id
                        ) 
                        VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')'''.format(
                                doctor_id_no,
                                request_data['first_name'],
                                request_data['last_name'],
                                request_data['date_of_birth'],
                                request_data['gender'],
                                request_data['email'],
                                request_data['phone_number'],
                                request_data['state'],
                                request_data['city'],
                                request_data['zip_code'],
                                request_data['clinic_hospital'],
                                request_data['specialist'],
                                request_data['available_from'],
                                request_data['available_to'],
                                request_data['time_per_patient'],
                                request_data['max_appointments'],
                                request_data['highest_qualification'],
                                request_data['years_of_experience'],
                                request_data['in_person_fee'],
                                request_data['video_fee'],
                                request_data['phone_fee'],
                                request_data['emergency_availability'],
                                request_data['emergency_contact'],
                                request_data['doctor_image'],
                                request_data['hospital_clinic_address'],
                                request_data['monday'],
                                request_data['tuesday'],
                                request_data['wednesday'],
                                request_data['thursday'],
                                request_data['friday'],
                                request_data['saturday'],
                                request_data['sunday'],
                                request_data['upi_id']
                        )
                print(INSERT_QUERY)
                cursor.execute(INSERT_QUERY)
                conn.commit()
                doctorPassword = str(request_data['dob'])[:4] + str(request_data['mobile_no'])[5:]
                print(doctorPassword)
                print(request_data['mobile_no'], request_data['dob'])
                LOGIN_QUERY1 = '''
                        INSERT INTO smaranvaidhya.doctor_login(
                        doctor_id,
                        email_id,
                        password
                        ) 
                        VALUES('{}','{}','{}')'''.format(
                                doctor_id_no,
                                request_data['email'],
                                doctorPassword
                        )
                cursor.execute(LOGIN_QUERY1)
                conn.commit()
        except Exception as e:
                print("Error", str(e), "Occurred")
        finally:
                if conn:
                        cursor.close()
                        conn.close()
        return "Success"

def get_doctor_data():
        conn = connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        try:
                QUERY = '''
                        SELECT 
                        id,
                        first_name,
                        last_name,
                        TO_CHAR(date_of_birth, 'DD-MON-YYYY') AS date_of_birth,
                        gender,
                        email,
                        phone_number,
                        state,
                        city,
                        zip_code,
                        clinic_hospital,
                        specialist,
                        TO_CHAR(available_from, 'HH24:MI:SS') AS available_from,
                        TO_CHAR(available_to, 'HH24:MI:SS') AS available_to,
                        time_per_patient,
                        max_appointments,
                        highest_qualification,
                        years_of_experience,
                        in_person_fee,
                        video_fee,
                        phone_fee,
                        emergency_availability,
                        emergency_contact,
                        doctor_image,
                        hospital_clinic_address,
                        monday, 
                        tuesday,
                        wednesday,
                        thursday,
                        friday,
                        saturday,
                        sunday,
                        upi_id
                        FROM smaranvaidhya.doctor_information
                        '''
                print(QUERY)
                cursor.execute(QUERY)
                records = cursor.fetchall()
                # Process each row's doctor_image field
                for record in records:
                        if record["doctor_image"] is not None:
                                record["doctor_image"] = record["doctor_image"].tobytes().decode("utf-8")
                json_result = json.dumps(records, indent=2)
                print(json_result)
        except Exception as e:
                print("Error", str(e), "Occurred")
        finally:
                if conn:
                        cursor.close()
                        conn.close()
        return json_result

def post_appointment_booking_data(request_data):
        conn = connection()
        cursor = conn.cursor()
        try:
                INSERT_QUERY = """
                INSERT INTO smaranvaidhya.appointment_data (
                doctor_id,
                patient_id,
                patient_name,
                contact_number,
                gender,
                age,
                date_of_appointment,
                slot_of_appointment,
                reason_for_visit,
                pre_existing_conditions,
                current_medications,
                allergies,
                mode_of_payment,
                consultancytype,  
                fees
                ) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')
                """.format(
                request_data['doctor_id'],
                request_data['patient_id'],
                request_data['patient_name'],
                request_data['contact_number'],
                request_data['gender'],
                request_data['age'],
                request_data['date_of_appointment'],
                request_data['slot_of_appointment'],
                request_data['reason_for_visit'],
                request_data['pre_existing_conditions'],
                request_data['current_medications'],
                request_data['allergies'],
                request_data['mode_of_payment'],
                request_data['consultancytype'],  
                request_data['fees']
                )
                print(INSERT_QUERY)  # Debugging output
                cursor.execute(INSERT_QUERY)
                conn.commit()
                return "Success"
        except Exception as e:
                print("Error:", str(e))
                return "Failed: " + str(e)
        finally:
                if conn:
                        cursor.close()
                        conn.close()


def get_user_profile(user_id):
        conn = connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        try:
                QUERY = '''
                SELECT 
                patient_id,
                first_name,
                last_name,  
                TO_CHAR(date_of_birth, 'DD-MON-YYYY') AS date_of_birth,
                gender,
                email,
                phone_number,
                password,
                state,
                city,
                zip_code
                FROM smaranvaidhya.patient_registration
                WHERE patient_id = %s
                '''
                cursor.execute(QUERY, (user_id,))
                record = cursor.fetchone()  # Fetch only one user instead of fetchall()
                if not record:
                        return None  # Return None if no user found
                print(json.dumps(record, indent=2))  # Debugging output
                return record  # Return dictionary directly
        except Exception as e:
                print("Error", str(e), "Occurred")
                raise e
        
        finally:
                if conn:
                        cursor.close()
                        conn.close()

def update_user_profile(user_id, data):
        conn = None
        cursor = None
        try:
                conn = connection()  # Establish database connection
                cursor = conn.cursor()
                QUERY = '''
                UPDATE smaranvaidhya.patient_registration
                SET first_name = %s, last_name = %s, email = %s, phone_number = %s, 
                password = %s, city = %s, state = %s, zip_code = %s
                WHERE patient_id = %s
                RETURNING patient_id
                '''
                cursor.execute(QUERY, (
                data["first_name"], 
                data["last_name"], 
                data["email"],
                data["phone_number"], 
                data["password"], 
                data["city"],
                data["state"], 
                data["zip_code"], 
                user_id
                ))
                updated_row = cursor.fetchone()  # Fetch the updated row
                conn.commit()  # Commit the transaction
                return bool(updated_row)  # Return True if update was successful
        except psycopg2.Error as e:
                print(f"Database Error: {e.pgcode} - {e.pgerror}")
                if conn:
                        conn.rollback()  # Rollback in case of error
                raise
        finally:
                if cursor:
                        cursor.close()
                if conn:
                        conn.close()

def get_user_history(user_id):
        conn = connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        try:
                QUERY = '''
                SELECT 
                appointment_id,
                doctor_id,
                patient_name,
                gender,
                age,
                TO_CHAR(date_of_appointment, 'DD-MON-YYYY') AS date_of_appointment,
                TO_CHAR(slot_of_appointment, 'HH24:MI:SS') AS slot_of_appointment,
                mode_of_payment,
                contact_number,
                reason_for_visit,
                pre_existing_conditions,
                current_medications,
                allergies
                FROM smaranvaidhya.appointment_data
                WHERE patient_id = %s
                '''
                cursor.execute(QUERY, (user_id,))
                record = cursor.fetchall()  # Fetch only one user instead of fetchall()
                if not record:
                        return None  # Return None if no user found
                print(json.dumps(record, indent=2))  # Debugging output
                return record  # Return dictionary directly
        except Exception as e:
                print("Error", str(e), "Occurred")
                raise e
        finally:
                if conn:
                        cursor.close()
                        conn.close()

def get_doctor_view_data(doctor_id):
        conn = connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        try:
                QUERY = '''
                SELECT 
                appointment_id,
                patient_id,
                patient_name,
                gender,
                age,
                TO_CHAR(date_of_appointment, 'DD-MON-YYYY') AS date_of_appointment,
                TO_CHAR(slot_of_appointment, 'HH24:MI:SS') AS slot_of_appointment,
                mode_of_payment,
                contact_number,
                reason_for_visit,
                pre_existing_conditions,
                current_medications,
                allergies
                FROM smaranvaidhya.appointment_data
                WHERE doctor_id = %s
                '''
                cursor.execute(QUERY, (doctor_id,))
                record = cursor.fetchall()  # Fetch only one user instead of fetchall()
                if not record:
                        return None  # Return None if no user found
                print(json.dumps(record, indent=2))  # Debugging output
                return record  # Return dictionary directly
        except Exception as e:
                print("Error", str(e), "Occurred")
                raise e
        finally:
                if conn:
                        cursor.close()
                        conn.close()