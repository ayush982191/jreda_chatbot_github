# import uuid
# import requests
# from datetime import datetime, timedelta
# import json
# import random

# SHEETDB_URL = "https://sheetdb.io/api/v1/uj1y32yara8fx"

# with open("Data/JREDA_sla_config.json") as f:
#     SLA_CONFIG = json.load(f)


# def generate_grievance_id():
#     return "GRV" + str(random.randint(1000000000000000, 9999999999999999))


# def get_sla_hours(category):
#     for item in SLA_CONFIG:
#         if item["category"].lower() in category.lower():
#             return item["sla_hours"]
#     return 72


# def store_grievance(data, farmer_context):

#     grievance_id = generate_grievance_id()
#     unique_id = str(uuid.uuid4())[:8]
#     created = datetime.now()

#     category = data.get("Category", "General")
#     issue_summary = data.get("Issue Summary", "")

#     sla_hours = get_sla_hours(category)
#     expected = created + timedelta(hours=sla_hours)

#     record = {
#         "Grievance ID": grievance_id,
#         "ID": unique_id,
#         "Farmer Name": farmer_context.get("farmer_name"),
#         "Farmer ID": farmer_context.get("farmer_id"),
#         "Mobile Number": farmer_context.get("mobile_number"),
#         "Pump ID": farmer_context.get("pump_id"),
#         "District": farmer_context.get("district"),
#         "Block": farmer_context.get("block"),
#         "Category": category,
#         "Status": "pending",
#         "Created Date": created.strftime("%d %B %Y %I:%M %p"),
#         "Assigned Vendor": farmer_context.get("vendor"),
#         "Expected Resolution": expected.strftime("%d/%m/%Y"),
#         "Issue Summary": issue_summary
#     }

#     try:
#         requests.post(
#             SHEETDB_URL,
#             json={"data": [record]},
#             timeout=10
#         )
#     except Exception as e:
#         print("SheetDB Error:", str(e))

#     return record

import uuid
import requests
from datetime import datetime, timedelta
import json
import random

SHEETDB_URL = "https://sheetdb.io/api/v1/uj1y32yara8fx"

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
    unique_id = str(uuid.uuid4())[:8]
    created = datetime.now()

    category = data.get("Category", "General")
    issue_summary = data.get("Issue Summary", "")

    sla_hours = get_sla_hours(category)
    expected = created + timedelta(hours=sla_hours)

    record = {
        "Grievance ID": grievance_id,
        "ID": unique_id,
        "Farmer Name": farmer_context.get("farmer_name"),
        "Farmer ID": farmer_context.get("farmer_id"),
        "Mobile Number": farmer_context.get("mobile_number"),
        "Pump ID": farmer_context.get("pump_id"),
        "District": farmer_context.get("district"),
        "Block": farmer_context.get("block"),
        "Category": category,
        "Status": "pending",
        "Created Date": created.strftime("%d %B %Y %I:%M %p"),
        "Assigned Vendor": farmer_context.get("vendor"),
        "Expected Resolution": expected.strftime("%d/%m/%Y"),
        "Issue Summary": issue_summary
    }

    try:
        requests.post(
            SHEETDB_URL,
            json={"data": [record]},
            timeout=10
        )
    except Exception as e:
        print("SheetDB Error:", str(e))

    return record