from typing import Dict, List
from datetime import datetime
from langchain_core.tools import tool
import sqlite3

DB_PATH = "hospital.db"

# In-memory database for POC
APPOINTMENTS_DB = []

SLOTS_DB = {
    "2026-03-10": ["10:00 AM", "11:00 AM", "02:00 PM", "04:00 PM"],
    "2026-03-11": ["09:00 AM", "01:00 PM", "03:00 PM"]
}


@tool
def check_slot_availability(date: str) -> List[str]:
    """Check available appointment slots for a given date."""
    return SLOTS_DB.get(date, ["09:00 AM", "10:00 AM", "02:00 PM"])


@tool
def book_appointment(patient_name: str, phone: str, problem: str, time: str, date: str) -> Dict:
    """Book an appointment and save it."""
    
    appointment = {
        "id": len(APPOINTMENTS_DB) + 1,
        "patient_name": patient_name,
        "phone": phone,
        "problem": problem,
        "time": time,
        "date": date,
        "status": "Confirmed",
        "doctor": "Dr. Smith (General Physician)"
    }

    APPOINTMENTS_DB.append(appointment)

    return appointment


def get_all_appointments() -> List[Dict]:
    return APPOINTMENTS_DB


def delete_appointment(appointment_id: int) -> bool:
    global APPOINTMENTS_DB
    initial_len = len(APPOINTMENTS_DB)
    APPOINTMENTS_DB = [a for a in APPOINTMENTS_DB if a["id"] != appointment_id]
    return len(APPOINTMENTS_DB) < initial_len

def save_appointment(data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    phone = data["phoneNumber"]

    # check if appointment exists
    cursor.execute(
        "SELECT id FROM appointments WHERE phoneNumber=?",
        (phone,)
    )

    existing = cursor.fetchone()

    if existing:
        cursor.execute("""
            UPDATE appointments
            SET patientName=?, problem=?, time=?, date=?, status=?, doctor=?
            WHERE phoneNumber=?
        """, (
            data["patientName"],
            data["problem"],
            data["time"],
            data["date"],
            data.get("status","Confirmed"),
            data.get("doctor","Dr. Smith"),
            phone
        ))

    else:
        cursor.execute("""
            INSERT INTO appointments
            (patientName, phoneNumber, problem, time, date, status, doctor)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            data["patientName"],
            data["phoneNumber"],
            data["problem"],
            data["time"],
            data["date"],
            data.get("status","Confirmed"),
            data.get("doctor","Dr. Smith")
        ))

    conn.commit()
    conn.close()