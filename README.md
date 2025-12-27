Appointment Booking API – README

This is a RESTful Appointment Booking API built with Django Rest Framework.
It supports user authentication, appointment booking, viewing, and rescheduling.

🔐 Authentication

The API uses Token Authentication.

Once logged in, all protected endpoints require:

Authorization: Token <your_access_token>

1️⃣ Register User
Endpoint
POST /api/register/

Request Body
{
  "username": "nicole@example.com",
  "email": "nicole@example.com",
  "password": "strongpass"
}

Successful Response (201)
{
  "id": 7,
  "username": "nicole@example.com",
  "email": "nicole@example.com"
}


📌 Password is securely hashed by Django.

2️⃣ Login User
Endpoint
POST /api/login/

Request Body
{
  "username": "nicole@example.com",
  "password": "strongpass"
}

Successful Response (200)
{
  "token": "cbcb5e4ca1a1d0d48b00e3a1c841a129e89d7a53",
  "username": "nicole@example.com"
}


🔑 Save this token — it is required for all protected requests.

3️⃣ Create (Book) Appointment
Endpoint
POST /api/appointments/

Headers
Authorization: Token cbcb5e4ca1a1d0d48b00e3a1c841a129e89d7a53
Content-Type: application/json

Request Body
{
  "slot": 5,
  "notes": "Initial consultation"
}

Successful Response (201)
{
  "id": 12,
  "slot": {
    "id": 5,
    "start_time": "10:00",
    "end_time": "10:30",
    "provider": "Dr. Smith"
  },
  "user": "nicole@example.com",
  "notes": "Initial consultation",
  "status": "booked"
}


📌 The authenticated user is automatically attached using the token.

4️⃣ View My Appointments
Endpoint
GET /api/appointments/

Headers
Authorization: Token cbcb5e4ca1a1d0d48b00e3a1c841a129e89d7a53

Successful Response (200)
[
  {
    "id": 12,
    "slot": {
      "id": 5,
      "start_time": "10:00",
      "end_time": "10:30"
    },
    "notes": "Initial consultation",
    "status": "booked"
  }
]


📌 Users can only see their own appointments.

5️⃣ Reschedule Appointment
Endpoint
PATCH /api/appointments/12/reschedule/

Headers
Authorization: Token cbcb5e4ca1a1d0d48b00e3a1c841a129e89d7a53
Content-Type: application/json

Request Body
{
  "new_slot": 8
}

Successful Response (200)
{
  "message": "Appointment rescheduled successfully",
  "appointment_id": 12,
  "old_slot": 5,
  "new_slot": 8
}


📌 Old slot is unlocked and new slot is locked using database transactions.

6️⃣ Logout User
Endpoint
POST /api/logout/

Headers
Authorization: Token cbcb5e4ca1a1d0d48b00e3a1c841a129e89d7a53

Successful Response (200)
{
  "message": "Logged out successfully"
}


📌 Token is deleted and cannot be reused.