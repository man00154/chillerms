import random

def simulate_chiller_readings(setpoint: float):
    """
    Simulate live readings for a chiller based on its setpoint.
    Everything here is synthetic, safe, and for demo only.
    """
    # Temps
    supply = round(setpoint + random.uniform(-1.0, 0.4), 2)
    inlet  = round(setpoint + random.uniform(2.0, 4.0), 2)
    outlet = round(setpoint + random.uniform(-0.4, 1.0), 2)
    ambient = round(random.uniform(28, 36), 2)

    # Loads
    comp1 = random.choice([0, 25, 50, 75, 100])
    comp2 = random.choice([0, 25, 50, 75, 100])

    # Power & flow
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

def simulate_toggle_status(status: str) -> str:
    """
    Simple ON/OFF toggler.
    """
    return "OFF" if status == "ON" else "ON"
