import random

# ----------------------------------------------------
# Generate simulated chiller parameters
# ----------------------------------------------------
def simulate_chiller_readings(setpoint: float):
    # Basic simulated temps relative to setpoint
    supply = round(setpoint + random.uniform(-0.8, 0.4), 2)
    inlet = round(setpoint + random.uniform(2.0, 4.0), 2)
    outlet = round(setpoint + random.uniform(-0.5, 1.0), 2)
    ambient = round(random.uniform(28, 35), 2)

    # Load
    comp1 = random.choice([0, 25, 50, 75, 100])
    comp2 = random.choice([0, 25, 50, 75, 100])

    # Electrical & flow
    power = round(80 + (comp1 + comp2) * 1.8, 2)
    flow = round(random.uniform(100, 230), 2)

    return {
        "supply_temp": supply,
        "inlet_temp": inlet,
        "outlet_temp": outlet,
        "ambient_temp": ambient,
        "comp1": comp1,
        "comp2": comp2,
        "power_kw": power,
        "water_flow": flow,
    }


# ----------------------------------------------------
# Toggle ON/OFF status
# ----------------------------------------------------
def simulate_toggle_status(status: str):
    return "OFF" if status == "ON" else "ON"
