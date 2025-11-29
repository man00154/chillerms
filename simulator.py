import random

def simulate_chiller_readings(setpoint):
    supply = round(setpoint + random.uniform(-1.0, 0.4), 2)
    inlet  = round(setpoint + random.uniform(2, 4), 2)
    outlet = round(setpoint + random.uniform(-0.4, 1.0), 2)
    ambient = round(random.uniform(28, 36), 2)

    comp1 = random.choice([0, 25, 50, 75, 100])
    comp2 = random.choice([0, 25, 50, 75, 100])

    power = round(80 + (comp1 + comp2) * 1.8, 2)
    water = round(random.uniform(120, 260), 2)

    return {
        "supply_temp": supply,
        "inlet_temp": inlet,
        "outlet_temp": outlet,
        "ambient_temp": ambient,
        "comp1": comp1,
        "comp2": comp2,
        "power_kw": power,
        "water_flow": water,
    }

def simulate_toggle_status(s):
    return "OFF" if s == "ON" else "ON"
