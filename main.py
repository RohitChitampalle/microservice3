from fastapi import FastAPI
import requests

app = FastAPI()

bookings = {}

@app.get("/")
def home():
    return {"message": "Booking Service Running"}

@app.post("/booking/create")
def create_booking(data: dict):
    partner = requests.get(f"http://localhost:3001/partners/{data['partner_id']}").json()
    
    if partner["kyc_status"] != "APPROVED":
        return {"error": "Partner KYC not approved"}

    bookings[data["id"]] = data
    bookings[data["id"]]["status"] = "CREATED"
    return bookings[data["id"]]

@app.post("/booking/start/{id}")
def start_booking(id: str):
    bookings[id]["status"] = "STARTED"
    return bookings[id]

@app.post("/booking/complete/{id}")
def complete_booking(id: str):
    bookings[id]["status"] = "COMPLETED"
    
    requests.post("http://localhost:8080/payment/process", json={
        "booking_id": id
    })
    
    return bookings[id]