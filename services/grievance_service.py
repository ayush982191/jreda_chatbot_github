import uuid
import requests
from datetime import datetime, timedelta
import json
import random
from datetime import datetime, timezone
 
SHEETDB_URL = "https://sheetdb.io/api/v1/s1f7oc6clafd4"
 
with open("Data/JREDA_sla_config.json") as f:
    SLA_CONFIG = json.load(f)
 
 
def generate_grievance_id():
    return "GRV" + str(random.randint(1000000000000000, 9999999999999999))
 
 
def get_sla_hours(category):
    for item in SLA_CONFIG:
        if item["category"].lower() in category.lower():
            return item["sla_hours"]
    return 72
 
 
 
 
 
def store_grievance(data, farmer_context):
 
    grievance_id = generate_grievance_id()
    created = datetime.now()
 
    category = data.get("Category", "General")
    issue_summary = data.get("Issue Summary", "")
 
    sla_hours = get_sla_hours(category)
    expected = created + timedelta(hours=sla_hours)
 
    sheet_record = {
        "grievance_id": grievance_id,
        "mobile_number": farmer_context.get("mobile_number"),
        "farmer_id": farmer_context.get("farmer_id"),
        "pump_id": farmer_context.get("pump_id"),
        "category": category,
        "current_status": "Pending",
        "created_date": created.strftime("%d %B %Y %I:%M %p"),
        "assigned_vendor": farmer_context.get("vendor"),
        "expected_resolution_date": expected.strftime("%d/%m/%Y"),
        "issue_summary": issue_summary,
        "updated_date": datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
    }
   
    try:
        requests.post(
            SHEETDB_URL,
            json={"data": [sheet_record]},
            timeout=10
        )
    except Exception as e:
        print("SheetDB Error:", str(e))
 
    return sheet_record
 