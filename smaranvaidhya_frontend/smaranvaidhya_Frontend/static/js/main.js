function verify_user_login(selectedLoginType, userEmailId, password) {
    var request_data = {
        user_login_type: selectedLoginType,
        email: userEmailId,
        password: password
    };
    $.ajax({
        url: '/attempt_to_login_for_user',
        type: "POST",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify(request_data),
        success: function(data) {
            console.log(data);
            if (data.status === "Login Successful") {
                console.log("Login done");
                console.log("User ID:", data.user_id);
                setTimeout(() => {
                    window.location.href = '/bookAppointment';
                }, 500);
            } else {
                alert("Login failed. Please check your credentials.");
            }
        },
        error: function(jqXhr, textStatus, errorMsg) {
            console.error("Error:", errorMsg);
            alert("Something went wrong. Please try again.");
        }
    });
}


function save_user_registration_details(request_data){
    // console.log(request_data);
    $.ajax({
        url:'/save_user_registration_details',
        type:"POST",
        dataType:"json",
        contentType : "application/json",
        data : JSON.stringify(request_data),
        beforeSend : function() {

        },
        success : function (data, status, xhr){
            
        },
        error : function(jqXhr, textStatus, errorMsg){
            console.log(errorMsg);
        }
    });
}

function formatDate(dateStr) {
    let date = new Date(dateStr);
    let year = date.getFullYear();
    let month = ('0' + (date.getMonth() + 1)).slice(-2); // Add leading zero if needed
    let day = ('0' + date.getDate()).slice(-2); // Add leading zero if needed
    return `${year}-${month}-${day}`;
}

function register_login_events(){
    $(document).on("change", "#userTypeDropdown", function(e){
        var selectedLoginType = $("#userTypeDropdown option:selected").val();
        console.log(selectedLoginType);
    });

    $(document).on("click", "#userLoginSubmit", function(e){
        var selectedLoginType = $("#userTypeDropdown option:selected").val();
        var userEmailId = $("#emailId").val();
        var password = $("#password").val();
        verify_user_login(selectedLoginType, userEmailId, password);
    });

    $(document).on("click", "#registrationSubmit", function (e) {
        var first_name = $("#userFirstName").val().trim();
        var last_name = $("#userLastName").val().trim();
        var date_of_birth = formatDate($("#dobDate").datepicker('getDate'));
        var gender = $("#userGender").val();
        var email = $("#userEmailId").val().trim();
        var phone_number = $("#userPhoneNumber").val().trim();
        var password = $("#userPassword").val();
        var confirmPassword = $("#userConfirmPassword").val();
        var state = $("#state").val().trim();
        var city = $("#city").val().trim();
        var zip_code = $("#zipCode").val().trim();

        if (password !== confirmPassword) {
            e.preventDefault(); // Prevent form submission
            alert("Password and Confirm Password do not match. Please try again.");
            return;
        }
        var request_data = {
            "first_name": first_name,
            "last_name": last_name,
            "date_of_birth": date_of_birth,
            "gender": gender,
            "email": email,
            "phone_number": parseInt(phone_number),
            "password": password,
            "city": city,
            "state": state,
            "zip_code": zip_code
        };    
        save_user_registration_details(request_data);
    });
    
    $(document).on("click", "#contactUsSubmit", function (e) {
        var full_name = $("#contactUsFullName").val();
        var email = $("#contactUsEmailId").val();
        var message = $("#contactUsMessage").val();
        var request_data = {
            "full_name": full_name,
            "email": email,
            "message": message,
        };
        // console.log(request_data);    
        post_contact_us_data(request_data);
    });

    $('#tabs li a').click(function(){
        var tab = $(this).attr('id');
        if($(this).hasClass('inactive')){ //this is the start of our condition 
            $('#tabs li a').addClass('inactive');           
            $(this).removeClass('inactive');
            $('.container').hide();
            $('#'+ tab + 'Container').fadeIn('slow');
        }
    });

    $(document).on("click", "#backButton", function(e){
        $("#subjectsContainer").addClass('d-none');
        $("#coursesContainer").removeClass('d-none');
        $("#backButton").addClass('d-none');
        populate_courses_data(courses_data)
    });
    
    $('#doctorRegistrationSubmit').on('click', function (e) {
        e.preventDefault(); // Prevent default form submission
        var formData = new FormData();
        formData.append('first_name', $('#doctorFirstName').val());
        formData.append('last_name', $('#doctorLastName').val());
        formData.append('date_of_birth', $('#dobDate').val());
        formData.append('gender', $('#gender').val());
        formData.append('email', $('#doctorEmailId').val());
        formData.append('phone_number', $('#doctorPhoneNumber').val());
        formData.append('state', $('#state').val());
        formData.append('city', $('#city').val());
        formData.append('zip_code', $('#zipCode').val());
        formData.append('clinic_hospital', $('#clinic-hospital').val());
        formData.append('specialist', $('#specialist').val());
        formData.append('available_from', $('#available-from').val());
        formData.append('available_to', $('#available-to').val());
        formData.append('time_per_patient', $('#time-per-patient').val());
        formData.append('max_appointments', $('#max-appointments').val());
        formData.append('highest_qualification', $('#highest-qualification').val());
        formData.append('years_of_experience', $('#years-of-experience').val());
        formData.append('in_person_fee', $('#in-person-fee').val());
        formData.append('video_fee', $('#video-fee').val());
        formData.append('phone_fee', $('#phone-fee').val());
        formData.append('emergency_availability', $('#emergency-availability').val());
        formData.append('emergency_contact', $('#emergency-contact').val());
        formData.append('hospital_clinic_address', $('#hospital-clinic-address').val());
        formData.append('upi_id', $('#upi_id').val());
        formData.append('monday', $('#monday').prop('checked') ? 1 : 0);
        formData.append('tuesday', $('#tuesday').prop('checked') ? 1 : 0);
        formData.append('wednesday', $('#wednesday').prop('checked') ? 1 : 0);
        formData.append('thursday', $('#thursday').prop('checked') ? 1 : 0);
        formData.append('friday', $('#friday').prop('checked') ? 1 : 0);
        formData.append('saturday', $('#saturday').prop('checked') ? 1 : 0);
        formData.append('sunday', $('#sunday').prop('checked') ? 1 : 0);
        formData.append('doctor_image', $('#doctor-image')[0].files[0]);
        var imageFile = $('#doctor-image')[0].files[0];
        if (imageFile) {
            var reader = new FileReader();
            reader.onload = function (e) {
                formData.append('doctor_image', e.target.result);
            };
            reader.readAsDataURL(imageFile);
        }
        $.ajax({
            url: '/post_doctor_information_data',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                // console.log('Response:', response);
                alert('Doctor registered successfully!');
            },
            error: function (xhr, status, error) {
                console.error('Error:', error);
                console.error('Response:', xhr.responseText);
                alert('There was an error while submitting the form.');
            }
        });
    });

    $(document).on("click", "#conAppointment", function (e) {
        e.preventDefault();
        console.log("Confirm Appointment button clicked!");  // Debugging step
    
        const appointmentDate = $("#date").val();
        const formattedDate = convertDateFormat(appointmentDate);
        var request_data = {
            "doctor_id": $("#doctor_id").val(),
            "patient_name": $("#patientName").val(),
            "contact_number": $("#contactNumber").val(),
            "gender": $("#gender").val(),
            "age": $("#age").val(),
            "reason_for_visit": $("#reason").val(),
            "pre_existing_conditions": $("#conditions").val(),
            "current_medications": $("#medications").val(),
            "allergies": $("#allergies").val(),
            "date_of_appointment": formattedDate,
            "slot_of_appointment": $("#slot").val(),
            "mode_of_payment": $("#paymentMethod").val(),
            "consultancytype": $("#selectedType").val(),
            "fees": $("#feeValue").val()
        };
    
        console.log("Request Data:", request_data);  // Debugging step
    
        if (typeof post_appointment_booking_data === "function") {
            post_appointment_booking_data(request_data);
        } else {
            console.error("post_appointment_booking_data function is not defined");
        }
    });
    
    
    
}

function post_contact_us_data(request_data){
    $.ajax({
        url:'/post_contact_us_data',
        type:"POST",
        dataType:"json",
        contentType : "application/json",
        data : JSON.stringify(request_data),
        beforeSend : function() {
            console.log(request_data);
        },
        success : function (data, status, xhr){
            console.log(raw_students_data)
        },
        error : function(jqXhr, textStatus, errorMsg){
            console.log(errorMsg);
        }
    });
}

function get_doctor_data() {
    $.ajax({
        url: '/get_doctor_data',
        type: "GET",
        contentType: "application/json",
        success: function (data) {
            raw_doctor_data = JSON.parse(data);
            doctor_data = JSON.parse(raw_doctor_data['data']);
            populate_doctor_data(doctor_data);
        },
        error: function (jqXhr, textStatus, errorMsg) {
            console.log(errorMsg);
        }
    });
}

function populate_doctor_data(doctor_data) {
    let doctorHtml = ``;
    doctor_data.forEach(row => {
        let slotsDropdownId = `slots-${row.id}`;
        let dateDropdownId = `date-${row.id}`;
        let bookButtonId = `bookappointmentbutton-${row.id}`;
        let consultationTypeDropdownId = `consultationType-${row.id}`;
        let feeDropdownId = `fee-${row.id}`;
        let paymentMethodDropdownId = `paymentMethod-${row.id}`;
        let upiDropdownId = `upi-${row.id}`;
        let workingDays = getWorkingDays(row);
        let validDates = getNextAvailableDates(workingDays, 14);

        doctorHtml += `
        <div class="doctor-card flex flex-col bg-white rounded-lg shadow-md p-4 mb-3 space-y-3">
            <div class="flex items-center space-x-4">
                <img src="data:image/jpeg;base64,${row['doctor_image'] || ''}" 
                    alt="Dr. ${row['first_name']} ${row['last_name']}" 
                    class="w-32 h-32 rounded-full object-cover border" />
                <div class="flex-1" style="margin-left:10px;">
                    <p class="text-xs"><strong>Doctor ID:</strong> ${row['id']}</p>
                    <h2 class="text-lg font-semibold">Dr. ${row['first_name']} ${row['last_name']}</h2>
                    <p class="text-sm text-gray-500">${row['specialist']} | ${row['years_of_experience']} yrs</p>
                    <p class="text-xs"><strong>Gender:</strong> ${row['gender']}</p>
                    <p class="text-xs"><strong>Date of Birth:</strong> ${row['date_of_birth']}</p>
                </div>
            </div>
            <div class="text-xs" style="margin-left:10px;">
                <p><strong>Qualification:</strong> ${row['highest_qualification']}</p>
                <p><strong>Availability:</strong> ${row['available_from']} - ${row['available_to']}</p>
                <p><strong>Location:</strong> ${row['city']}, ${row['state']} (${row['zip_code']})</p>
                <p><strong>Clinic/Hospital:</strong> ${row['clinic_hospital']}</p>
                <p><strong>Emergency:</strong> ${row['emergency_availability'] === 'yes' ? 'Available' : 'Not Available'} (📞 ${row['emergency_contact']})</p>
            </div>
            <div class="text-xs" style="margin-left:10px;">
                <p><strong>Fees:</strong></p>
                <ul class="list-disc pl-4">
                    <li>In-Person: ₹${row['in_person_fee']}</li>
                    <li>Video: ₹${row['video_fee']}</li>
                    <li>Phone: ₹${row['phone_fee']}</li>
                </ul>
            </div>
            <div class="text-xs" style="margin-left:10px;">
                <p><strong>Working Days:</strong></p>
                <ul class="working-days-list">
                    ${row['monday'] === "1" ? "<li>Monday</li>" : ""}
                    ${row['tuesday'] === "1" ? "<li>Tuesday</li>" : ""}
                    ${row['wednesday'] === "1" ? "<li>Wednesday</li>" : ""}
                    ${row['thursday'] === "1" ? "<li>Thursday</li>" : ""}
                    ${row['friday'] === "1" ? "<li>Friday</li>" : ""}
                    ${row['saturday'] === "1" ? "<li>Saturday</li>" : ""}
                    ${row['sunday'] === "1" ? "<li>Sunday</li>" : ""}
                </ul>
            </div>

            <div class="text-xs" style="margin-left:10px;">
                <label for="${dateDropdownId}"><strong>Select Date:</strong></label>
                <select id="${dateDropdownId}" class="date-dropdown w-full border p-2 rounded">
                    <option value="">Select Date</option>
                </select>
                <label for="${slotsDropdownId}"><strong>Select Time Slot:</strong></label>
                <select id="${slotsDropdownId}" class="time-slot-dropdown w-full border p-2 rounded">
                    <option value="">Select Date First</option>
                </select>
            </div>

            <div class="text-xs" style="margin-left:10px;">
                <label for="${consultationTypeDropdownId}"><strong>Select Consultation Type:</strong></label>
                <select id="${consultationTypeDropdownId}" class="consultation-type-dropdown w-full border p-2 rounded">
                    <option value="">Select Type</option>
                    <option value="in_person">In-Person</option>
                    <option value="video">Video</option>
                    <option value="phone">Phone</option>
                </select>

                <label for="${feeDropdownId}" class="mt-2"><strong>Consultation Fee:</strong></label>
                <select id="${feeDropdownId}" class="fee-dropdown w-full border p-2 rounded" disabled>
                    <option value="">Select Consultation Type First</option>
                </select>
            </div>

            <div class="flex flex-col items-start gap-2 mt-6" style="margin-left:10px;">
                <a href="${row['hospital_clinic_address']}" target="_blank" 
                    class="view-map text-blue-500 text-xs underline">
                    📍 View on Map
                </a>
                <a href="confirmBooking?id=${row['id']}&date=&slot=&selectedType=&feeValue=" 
                    id="${bookButtonId}"
                    class="book-btn text-white bg-red-500 px-4 py-2 rounded text-center w-full">
                    Book Appointment
                </a>
            </div>
        </div>`;

        setTimeout(() => {
            populateDropdown(dateDropdownId, validDates, 'date');
            document.getElementById(dateDropdownId).addEventListener("change", function () {
                let selectedDate = this.value;
                let slots = generateTimeSlots(row.available_from, row.available_to, row.time_per_patient);
                populateDropdown(slotsDropdownId, slots, 'time');
                updateBookingLink(dateDropdownId, slotsDropdownId, bookButtonId, row.id);
            });
            document.getElementById(consultationTypeDropdownId).addEventListener("change", function () {
                let selectedType = this.value;
                let feeDropdown = document.getElementById(feeDropdownId);
                feeDropdown.innerHTML = "";
                feeDropdown.disabled = false;
            
                let feeValue = "";
                if (selectedType === "in_person") {
                    feeValue = row['in_person_fee'];
                } else if (selectedType === "video") {
                    feeValue = row['video_fee'];
                } else if (selectedType === "phone") {
                    feeValue = row['phone_fee'];
                }
                if (feeValue) {
                    feeDropdown.innerHTML = `<option value="${feeValue}" selected>₹${feeValue}</option>`;
                } else {
                    feeDropdown.innerHTML = `<option value="">Select Consultation Type First</option>`;
                    feeDropdown.disabled = true;
                }
                updateBookingLink(dateDropdownId, slotsDropdownId, bookButtonId, row.id, consultationTypeDropdownId, feeDropdownId);
            });
            function updateBookingLink(dateDropdownId, slotsDropdownId, bookButtonId, doctorId, consultationTypeDropdownId, feeDropdownId) {
                let selectedDate = document.getElementById(dateDropdownId).value;
                let selectedSlot = document.getElementById(slotsDropdownId).value;
                let selectedType = document.getElementById(consultationTypeDropdownId).value;
                let selectedFee = document.getElementById(feeDropdownId).value;
                let bookingLink = `confirmBooking?id=${doctorId}&date=${selectedDate}&slot=${selectedSlot}&selectedType=${selectedType}&feeValue=${selectedFee}`;
                document.getElementById(bookButtonId).setAttribute("href", bookingLink);
            }
            document.getElementById(dateDropdownId).addEventListener("change", function () {
                updateBookingLink(dateDropdownId, slotsDropdownId, bookButtonId, row.id, consultationTypeDropdownId, feeDropdownId);
            });
            document.getElementById(slotsDropdownId).addEventListener("change", function () {
                updateBookingLink(dateDropdownId, slotsDropdownId, bookButtonId, row.id, consultationTypeDropdownId, feeDropdownId);
            });
        }, 100);
    });
    document.getElementById("maincomponent").innerHTML = doctorHtml;
}

function getWorkingDays(row) {
    let days = [];
    if (row.monday === "1") days.push("Monday");
    if (row.tuesday === "1") days.push("Tuesday");
    if (row.wednesday === "1") days.push("Wednesday");
    if (row.thursday === "1") days.push("Thursday");
    if (row.friday === "1") days.push("Friday");
    if (row.saturday === "1") days.push("Saturday");
    if (row.sunday === "1") days.push("Sunday");
    return days;
}

function getNextAvailableDates(workingDays, daysAhead) {
    let validDates = [];
    let today = moment();
    for (let i = 0; i < daysAhead; i++) {
        let currentDate = today.clone().add(i, 'days');
        let dayName = currentDate.format("dddd");
        if (workingDays.includes(dayName)) {
            validDates.push({ value: currentDate.format("YYYY-MM-DD"), text: currentDate.format("DD/MM/YYYY") });
        }
    }
    return validDates;
}

function generateTimeSlots(available_from, available_to, time_per_patient) {
    let slots = [];
    let startTime = moment(available_from, "HH:mm:ss");
    let endTime = moment(available_to, "HH:mm:ss");
    while (startTime.isBefore(endTime)) {
        slots.push({ value: startTime.format("HH:mm:ss"), text: startTime.format("hh:mm A") });
        startTime.add(time_per_patient, 'minutes');
    }
    return slots;
}

function populateDropdown(dropdownId, data, type) {
    let dropdown = document.getElementById(dropdownId);
    dropdown.innerHTML = `<option value="">${type === 'date' ? 'Select Date' : 'Select Time Slot'}</option>`;
    data.forEach(item => {
        let option = document.createElement("option");
        option.value = item.value;
        option.textContent = item.text;
        dropdown.appendChild(option);
    });
}

function updateBookingLink(dateDropdownId, slotsDropdownId, buttonId, doctorId) {
    let dateDropdown = document.getElementById(dateDropdownId);
    let slotsDropdown = document.getElementById(slotsDropdownId);
    let button = document.getElementById(buttonId);
    function updateHref() {
        let selectedDate = dateDropdown.value;
        let selectedSlot = slotsDropdown.value;
        button.href = selectedDate && selectedSlot ? `confirmBooking?id=${doctorId}&date=${selectedDate}&slot=${selectedSlot}` : "#";
    }
    dateDropdown.addEventListener("change", updateHref);
    slotsDropdown.addEventListener("change", updateHref);
}

function getBookingDetailsFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    let doctor_id = urlParams.get('id');
    let selectedDate = urlParams.get('date');
    let selectedSlot = urlParams.get('slot');
    let selectedConsultancy = urlParams.get('selectedType'); 
    let feeValue = urlParams.get('feeValue');

    if (doctor_id) {
        $("#doctor_id").val(doctor_id);
    }

    if (selectedDate) {
        // Convert from "YYYY-MM-DD" to "DD/MM/YYYY" for display
        let formattedDisplayDate = moment(selectedDate, "YYYY-MM-DD").format("DD/MM/YYYY");
        // Set the formatted display date if needed elsewhere (e.g., labels)
        $("#displayDate").text(formattedDisplayDate);  // Assuming you have a display element for the date
        
        // Set the date in "YYYY-MM-DD" format for the input field
        let inputDate = moment(selectedDate, "YYYY-MM-DD").format("YYYY-MM-DD");
        $("#date").val(inputDate); // Set the formatted date for the input field
    }

    if (selectedSlot) {
        $("#slot").val(selectedSlot);
    }

    if (selectedConsultancy) {
        $("#selectedType").val(selectedConsultancy);
    }

    if (feeValue) {
        $("#feeValue").val(feeValue);
    }
}

$(document).ready(function () {
    getBookingDetailsFromURL();
});

function get_doctor_view_data() {
    $.ajax({
        url: '/get_doctor_view_data',
        type: "GET",
        contentType: "application/json",
        success: function (data) {            
            let doctor_view_data = data.data ? data.data : data; 
            populate_doctor_view_data(doctor_view_data);
        },
        error: function (jqXhr, textStatus, errorMsg) {
            console.log("Error fetching data:", errorMsg);
        }
    });
}

function populate_doctor_view_data(doctor_view_data){
    let appointmentsHtml = ``;
    doctor_view_data.forEach(appointment => {
        appointmentsHtml += `
        <tr>
            <td>${appointment.appointment_id}</td>
            <td>${appointment.patient_id}</td>
            <td>${appointment.patient_name}</td>
            <td>${appointment.gender}</td>
            <td>${appointment.age}</td>
            <td>${appointment.date_of_appointment}</td>
            <td>${appointment.slot_of_appointment}</td>
            <td>${appointment.mode_of_payment}</td>
            <td>${appointment.contact_number}</td>
            <td>${appointment.reason_for_visit}</td>
            <td>${appointment.pre_existing_conditions}</td>
            <td>${appointment.current_medications}</td>
            <td>${appointment.allergies}</td>
        </tr>`;
    });
    document.getElementById("appointmentsTableBody").innerHTML = appointmentsHtml;
}

function get_user_history() {
    $.ajax({
        url: '/get_user_history',
        type: "GET",
        contentType: "application/json",
        success: function (data) {
            console.log(data);  
            populate_user_history(data);  
        },
        error: function (jqXhr, textStatus, errorMsg) {
            console.log(errorMsg);
        }
    });
}
function populate_user_history(data) {
    var tableBody = $("#appointmentsTableBody");
    tableBody.empty(); 
    var row = `
        <tr>
            <td>${data.appointment_id}</td>
            <td>${data.doctor_id}</td>
            <td>${data.patient_name}</td>
            <td>${data.gender}</td>
            <td>${data.age}</td>
            <td>${data.date_of_appointment}</td>
            <td>${data.slot_of_appointment}</td>
            <td>${data.mode_of_payment}</td>
            <td>${data.contact_number}</td>
            <td>${data.reason_for_visit}</td>
            <td>${data.pre_existing_conditions}</td>
            <td>${data.current_medications}</td>
            <td>${data.allergies}</td>
        </tr>
    `;
    tableBody.append(row);
}

function post_appointment_booking_data(request_data) {
    console.log("Sending AJAX Request:", request_data); 

    $.ajax({
        url: '/post_appointment_booking_data',
        type: "POST",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify(request_data),
        beforeSend: function () {
            console.log("Before Send - Data:", request_data);
        },
        success: function (data, status, xhr) {
            console.log("Response Data:", data);
            window.location.href = "/Profile";
        },
        error: function (jqXhr, textStatus, errorMsg) {
            console.log("Error Occurred:", errorMsg);
            console.log("Full Response:", jqXhr);
        }
    });
}

