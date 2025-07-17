from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def load_index(request: Request):
    logs = ""
    try:
        with open("access_log.txt", "r") as f:
            logs = f.read()
    except FileNotFoundError:
        logs = "No access logs found"
    return templates.TemplateResponse("index.html", {"request": request, "access_logs": logs})

@app.post("/log-access")
async def log_access(request: Request):
    data = await request.json()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] IP: {request.client.host}, Agent: {data.get('agent')}, Platform: {data.get('platform')}, Location: {data.get('location')}\n"
    with open("access_log.txt", "a") as f:
        f.write(log_entry)
    return {"status": "logged"}

@app.get("/get-access-log-json")
async def get_access_log_json():
    logs = []
    try:
        with open("access_log.txt", "r") as f:
            for line in f:
                parts = line.strip().split(", ")
                entry = {
                    "timestamp": parts[0].split("]")[0].strip("["),
                    "ip": parts[0].split(":")[-1].strip(),
                    "agent": parts[1].replace("Agent: ", ""),
                    "platform": parts[2].replace("Platform: ", ""),
                    "location": parts[3].replace("Location: ", "")
                }
                logs.append(entry)
    except FileNotFoundError:
        pass
    return logs

@app.get("/download-access-log", response_class=PlainTextResponse)
async def download_access_log():
    try:
        with open("access_log.txt", "r") as f:
            return f.read()
    except FileNotFoundError:
        return "No access logs found"

@app.get("/analytics", response_class=HTMLResponse)
async def show_analytics(request: Request):
    return templates.TemplateResponse("analytics.html", {"request": request})



app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/find", response_class=HTMLResponse)
async def find_coordinates(request: Request, location: str = Form(...)):
    # Dummy coordinates for now
    lat, long = 31.6340, 74.8723
    return templates.TemplateResponse("index.html", {
        "request": request,
        "lat": lat,
        "long": long,
        "location": location
    })



# # FastAPI app entry point
# import csv
# from fastapi.responses import FileResponse, JSONResponse

# @app.get("/analytics", response_class=HTMLResponse)
# async def show_analytics(request: Request):
#     return templates.TemplateResponse("analytics.html", {"request": request})

# @app.get("/get-access-log-json")
# async def get_access_log_json():
#     logs = []
#     try:
#         with open("access_log.txt", "r") as f:
#             for line in f:
#                 parts = line.strip().split(", ")
#                 entry = {
#                     "timestamp": parts[0].split("]")[0].strip("["),
#                     "ip": parts[0].split(":")[-1].strip(),
#                     "agent": parts[1].replace("Agent: ", ""),
#                     "platform": parts[2].replace("Platform: ", ""),
#                     "location": parts[3].replace("Location: ", "")
#                 }
#                 logs.append(entry)
#     except FileNotFoundError:
#         pass
#     return JSONResponse(logs)

# @app.get("/download-access-log")
# async def download_access_log():
#     csv_file = "access_log.csv"
#     try:
#         with open("access_log.txt", "r") as infile, open(csv_file, "w", newline="") as outfile:
#             writer = csv.writer(outfile)
#             writer.writerow(["Timestamp", "IP", "User Agent", "Platform", "Location"])
#             for line in infile:
#                 parts = line.strip().split(", ")
#                 writer.writerow([
#                     parts[0].split("]")[0].strip("["),
#                     parts[0].split(":")[-1].strip(),
#                     parts[1].replace("Agent: ", ""),
#                     parts[2].replace("Platform: ", ""),
#                     parts[3].replace("Location: ", "")
#                 ])
#         return FileResponse(csv_file, media_type="text/csv", filename="access_log.csv")
#     except FileNotFoundError:
#         return {"error": "Log file not found"}


# @app.get("/", response_class=HTMLResponse)
# async def load_index(request: Request):
#     logs = ""
#     try:
#         with open("access_log.txt", "r") as f:
#             logs = f.read()
#     except FileNotFoundError:
#         logs = "No access logs found."

#     return templates.TemplateResponse("index.html", {
#         "request": request,
#         "access_logs": logs
#     })
    
#     @app.post("/log-access")
# async def log_access(request: Request):
#     data = await request.json()
#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     log_entry = (
#         f"[{timestamp}] IP: {request.client.host}, "
#         f"Agent: {data.get('agent')}, "
#         f"Platform: {data.get('platform')}, "
#         f"Location: {data.get('location')}\n"
#     )
#     with open("access_log.txt", "a") as f:
#         f.write(log_entry)
#     return {"status": "logged"}

