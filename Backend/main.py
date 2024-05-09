from fastapi import FastAPI, HTTPException, Body, Request, File, UploadFile, Path, Query
from fastapi.middleware.cors import CORSMiddleware
from Crypto.Cipher import DES
from supabase import create_client, Client
import random

# app object
app = FastAPI()

# CORS Middleware Setup
origins = ['http://localhost:3000']
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

  # Supabase setup
url = "https://aeuxgeirpiptxcdognmo.supabase.co"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFldXhnZWlycGlwdHhjZG9nbm1vIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTUxNzkzNDYsImV4cCI6MjAzMDc1NTM0Nn0.8Le0boVM6uhto0SrZUWjTiX97uL3RI8c5nU-Ukm-iXY"
supabase: Client = create_client(url, token)


DES_KEY = b'\x01\x02\x03\x04\x05\x06\x07\x08'

def pad(text):
    # Pad text to ensure it is a multiple of 8 bytes
    while len(text) % 8 != 0:
        text += ' '
    return text

def encrypt_des(ip_address, key):
    padded_ip = pad(ip_address)
    cipher = DES.new(key, DES.MODE_ECB)
    encrypted_ip = cipher.encrypt(padded_ip.encode())
    return encrypted_ip

def check_ip_exists(ip_address, supabase):
    query = supabase.table("RemotePoints").select("Points").eq("Points", ip_address).execute()
    return query.data != []

def save_to_database(ip_address, des_point, supabase):
    # Prepare data for insertion
    data = {"Points": ip_address, "DESPoint": des_point.hex()}
    response = supabase.table("RemotePoints").insert(data).execute()
    print(response)
    if response: 
     return {'success': True, 'data': response}
        
    

@app.post("/encrypt_ip/{ipAddress}")
async def encrypt_ip(ipAddress: str):
    # Check if IP already exists in the database
    if check_ip_exists(ipAddress, supabase):
        return {"message": "IP address already exists in the database"}

    # Encrypt the IP and save to database if not existing
    encrypted_ip = encrypt_des(ipAddress, DES_KEY)
    response = save_to_database(ipAddress, encrypted_ip, supabase)

    if response:
    	return {"message": "IP encrypted and stored successfully", "DESPoint": response}


# find the DesPoint in the database using the DesPoint from the route
@app.get("/findDesPoint/{desPoint}")
async def find_des_point(desPoint: str):
    # Query the database to find the DESPoint
    query = supabase.table("RemotePoints").select("DESPoint").eq("DESPoint", desPoint).execute()

    # If the DESPoint exists in the database, grant access
    if query.data:
        return {"message": "Access Granted successfully"}

    # If the DESPoint does not exist in the database, deny access
    return {"message": "Invalid Access Code ! Please try again"}


@app.get("/")
async def read_root():
    return {"Hello": "World"}



   