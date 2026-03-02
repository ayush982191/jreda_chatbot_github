# from services.gemini_service import generate_response


# def handle_device_status(farmer_context, language):

#     if not farmer_context:
#         return "Farmer device data not available."

#     prompt = f"""
# You are JREDA Government AI Assistant.

# Reply strictly in {language}.
# Use formal and professional tone.
# Do NOT invent information.
# Use ONLY the device data provided below.
# Do NOT use markdown symbols like **.
# Use clear headings and numbered points where appropriate.

# Device Data:
# Farmer Name: {farmer_context.get("farmer_name")}
# Pump ID: {farmer_context.get("pump_id")}
# District: {farmer_context.get("district")}
# Block: {farmer_context.get("block")}
# Vendor: {farmer_context.get("vendor")}
# Pump Capacity (HP): {farmer_context.get("pump_capacity_hp")}
# Warranty Status: {farmer_context.get("warranty_status")}
# Pump Status: {farmer_context.get("pump_status")}
# Voltage: {farmer_context.get("voltage")}
# Power Status: {farmer_context.get("power_status")}
# Last Communication Time: {farmer_context.get("last_communication_time")}
# Alarm Status: {farmer_context.get("alarm_status")}
# Fault Code: {farmer_context.get("fault_code")}

# Explain the solar pump device status clearly in structured format.
# If pump is stopped or fault exists, explain possible reason based only on the provided data.
# """

#     try:
#         reply = generate_response(prompt)
#         return reply.strip() if reply else "No device status available."
#     except Exception as e:
#         print("Device Status Error:", str(e))
#         return "Unable to fetch device status at the moment."

from services.gemini_service import generate_response, language_lock as language_lock_prompt


def handle_device_status(farmer_context, language):

    if not farmer_context:
        return "Farmer device data not available."

    prompt = f"""
You are JREDA Government AI Assistant.

{language_lock_prompt(language)}

IMPORTANT:
Use ONLY the device data provided.
Do NOT invent new information.
Do NOT provide raw technical dump.
Do NOT list all fields mechanically.

Device Data:
Farmer Name: {farmer_context.get("farmer_name")}
Pump ID: {farmer_context.get("pump_id")}
District: {farmer_context.get("district")}
Block: {farmer_context.get("block")}
Vendor: {farmer_context.get("vendor")}
Pump Capacity (HP): {farmer_context.get("pump_capacity_hp")}
Warranty Status: {farmer_context.get("warranty_status")}
Pump Status: {farmer_context.get("pump_status")}
Voltage: {farmer_context.get("voltage")}
Power Status: {farmer_context.get("power_status")}
Last Communication Time: {farmer_context.get("last_communication_time")}
Alarm Status: {farmer_context.get("alarm_status")}
Fault Code: {farmer_context.get("fault_code")}

INSTRUCTIONS:

1. Start with a proper greeting using farmer name.

2. Provide a complete but concise summary including:
   - Pump Status
   - Power Status
   - Voltage value
   - Warranty Status

3. If fault code exists:
   - Clearly explain what it indicates.
   - Mention likely cause based only on provided data.

4. Provide clear recommended action steps.

IMPORTANT:
- Response must contain at least 3–4 meaningful paragraphs.
- Do NOT reduce explanation.
- Maintain same level of clarity and detail in all languages.
- Do NOT oversimplify Hindi or Bengali output.
- Keep professional tone.

5. Keep response short, professional, and easy to understand.

Structure:

Greeting line

Current Status Summary

Possible Reason (if any)

Recommended Action
"""

    try:
        reply = generate_response(prompt)
        return reply.strip() if reply else "No device status available."
    except Exception as e:
        print("Device Status Error:", str(e))
        return "Unable to fetch device status at the moment."