from fastapi import FastAPI, HTTPException, Body, Request, File, UploadFile, Path, Query
from fastapi.middleware.cors import CORSMiddleware
from Crypto.Cipher import DES
from supabase import create_client, Client
# from tables import ip_table, pc1_table,shift_schedule,pc2_table,e_box_table,s_boxes,p_box_table,ip_inverse_table
from DESFunctions import *
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



def check_ip_exists(ip_address, supabase):
    query = supabase.table("RemotePoints").select("Points").eq("Points", ip_address).execute()
    return query.data != []

def save_to_database(ip_address, des_point, supabase):
    # Prepare data for insertion
    data = {"Points": ip_address, "DESPoint": des_point}
    response = supabase.table("RemotePoints").insert(data).execute()
    print(response)
    if response: 
     return {'success': True, 'data': response}
        
    

@app.post("/encrypt_ip/{ipAddress}")
async def encrypt_ip(ipAddress: str):
    # Check if IP already exists in the database
    if check_ip_exists(ipAddress, supabase):
        print(f"{ipAddress} is already exsists ")
        return {"message": "IP address already exists in the database"}

    # Encrypt the IP and save to database if not existing
    # encrypted_ip = encrypt_des(ipAddress, DES_KEY)
    encrypted_ip = encryption(ipAddress)
    print("++++++++++++++encrypted ip Adresss",encrypted_ip)
    
    
    response = save_to_database(ipAddress, encrypted_ip, supabase)
    
    if response:
        print(f"{encrypted_ip} saved to database")
        return {"message": "IP encrypted and stored successfully", "DESPoint": encrypted_ip}


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



   