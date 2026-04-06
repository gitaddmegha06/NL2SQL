import sqlite3
import random 
from datetime import date, timedelta



FIRST_NAMES = [
    'Aarav', 'Vivaan', 'Aditya', 'Arjun', 'Sai', 
    'Ananya', 'Diya', 'Ishita', 'Priya', 'Neha',
    'Rahul', 'Karan', 'Rohit', 'Vikram', 'Sanjay',
    'Pooja', 'Sneha', 'Kavita', 'Meera', 'Shreya'
]

LAST_NAMES = [
    'Sharma', 'Verma', 'Gupta', 'Patel', 'Singh',
    'Kumar', 'Reddy', 'Nair', 'Iyer', 'Mehta',
    'Joshi', 'Chopra', 'Bansal', 'Yadav', 'Desai'
]

CITIES = [
    'Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Ahmedabad',
    'Chennai', 'Kolkata', 'Pune', 'Jaipur', 'Surat',
    'Lucknow', 'Chandigarh', 'Indore', 'Bhopal', 'Nagpur'
]

SPECIALIZATIONS = [
    'General Physician',
    'Cardiology',
    'Dermatology',
    'Orthopedics',
    'Pediatrics',
    'Gynecology',
    'Neurology',
    'ENT',
    'Oncology',
    'Gastroenterology'
]

DEPARTMENTS = [
    'General Medicine',
    'Cardiology Department',
    'Orthopedic Department',
    'Pediatrics Department',
    'Emergency & Trauma',
    'Radiology',
    'ICU',
    'Outpatient Department (OPD)',
    'Surgery',
    'Pathology Lab'
]
conn = sqlite3.connect('clinic.db')
cursor = conn.cursor()


cursor.executescript("""
CREATE TABLE IF NOT EXISTS patients(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    dob DATE,
    gender TEXT,
    city TEXT,
    registered_date DATE
    );

CREATE TABLE IF NOT EXISTS doctors(
     id INTEGER PRIMARY KEY AUTOINCREMENT,
     name TEXT,
     specialization TEXT,
     department TEXT,
     phone TEXT
     );
    
CREATE TABLE IF NOT EXISTS appointments(
     id INTEGER PRIMARY KEY AUTOINCREMENT,
     patient_id INTEGER REFERENCES patients(id),
     doctor_id INTEGER REFERENCES doctors(id),
     appointment_date DATE,
     status TEXT,
     notes TEXT);


CREATE TABLE IF NOT EXISTS treatments(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    appointment_id INTEGER REFERENCES appointments(id),
    treatment_name TEXT,
    cost REAL,
    duration_minutes INTEGER );

CREATE TABLE IF NOT EXISTS invoices(
    id INTEGER PRIMARY KEY,
    patient_id INTEGER REFERENCES patients(id),
    invoice_date DATE,
    total_amount REAL,
    paid_amount REAL,
    status TEXT
    )
    """)

conn.commit()

print("Generating sample data....")

print("Populating Doctors table")
for _ in range(15):
    name = f"Dr. {random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
    specialization = random.choice(SPECIALIZATIONS)
    dept = random.choice(DEPARTMENTS)
    phone = f"+91{random.randint(70000,99999)}-{random.randint(10000,99999)}"
    cursor.execute("INSERT INTO doctors(name, specialization, department, phone) VALUES (?,?,?,?)"
    ,(name, specialization, dept, phone))

print("Populating Patients table")
for _ in range(200):
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    days_ago = random.randint(365*4, 365*70)
    dob = (date.today() - timedelta(days=days_ago)).isoformat()

    gender = random.choice(['Male','Female'])
    city = random.choice(CITIES)
    registered_date = (date.today() - timedelta(days=random.randint(1, 365))).isoformat()
    cursor.execute("INSERT INTO patients(first_name, last_name, dob, gender, city, registered_date) VALUES(?,?,?,?,?,?)",
    (first_name, last_name, dob, gender, city, registered_date))

print("Populating Appointments Table")
for _ in range(50):
    patient_id = random.randint(1, 200)
    doctor_id = random.randint(1, 15)
    days_ahead = random.randint(-30, 30)
    appointment_date = (date.today() + timedelta(days=days_ahead)).isoformat()
    status = random.choice(['Completed', 'Scheduled', 'Cancelled'])
    notes = "Routine checkup"
    cursor.execute("INSERT INTO appointments(patient_id, doctor_id, appointment_date, status, notes) VALUES(?,?,?,?,?)",
    (patient_id, doctor_id, appointment_date, status, notes))

conn.commit()
conn.close()

print("tables created successfully")