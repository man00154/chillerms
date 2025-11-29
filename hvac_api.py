def get_ahu_live(unit):
    return {
        "supply_temp": 22.5,
        "return_temp": 27.3,
        "humidity": 48.0,
        "fan_speed": 80
    }

def get_pahu_live(unit):
    return {
        "cooling_valve": 75,
        "supply_temp": 23.0,
        "return_temp": 28.5
    }

def get_tfa_live(unit):
    return {
        "status": "NORMAL",
        "mode": "AUTO"
    }
