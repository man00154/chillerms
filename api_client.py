import random

def get_chiller_parameters(chiller_id):
    return {
        "supply_temp": round(random.uniform(18, 24), 2),
        "return_temp": round(random.uniform(23, 30), 2),
        "power_kw": round(random.uniform(50, 300), 2),
        "flow_m3hr": round(random.uniform(120, 260), 2),
        "compressor_1": random.choice([0, 50]),
        "compressor_2": random.choice([0, 50])
    }

def get_hvac_data():
    return {
        "ahu_temp": round(random.uniform(20, 26), 2),
        "pahu_temp": round(random.uniform(20, 27), 2),
        "tfa_temp": round(random.uniform(20, 25), 2),
        "ahu_rh": round(random.uniform(40, 60), 2),
        "pahu_rh": round(random.uniform(38, 55), 2),
        "tfa_rh": round(random.uniform(35, 50), 2)
    }
