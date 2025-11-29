import requests

BASE = "http://223.31.216.236/ODataConnector/rest/RealtimeData?PointName="

def get_point(tag):
    try:
        url = BASE + tag
        r = requests.get(url, timeout=5)
        return r.json()[0]["Value"]
    except:
        return None

def get_chiller_live(ch_no):
    t = f"ac:T5/TR/CHILLER/T5-TR-CHILLER-{ch_no}"
    return {
        "ambient": get_point(t + "/AMBIENT_TEMP"),
        "inlet": get_point(t + "/INLET_TEMP"),
        "outlet": get_point(t + "/OUTLET_TEMP"),
        "power": get_point(t + "/POWER_CONSUMPTION"),
        "flow": get_point(t + "/WATER_FLOW"),
        "comp1": get_point(t + "/COMP1_ACTIVE_LOAD"),
        "comp2": get_point(t + "/COMP2_ACTIVE_LOAD"),
        "setpoint": get_point(t + "/TEMP_SETPOINT")
    }
