import pandas as pd

def load_book1():
    return pd.read_excel("data/Book1.xlsx")

def load_temp_rh():
    return pd.read_excel("data/TR_TEMP_RH.xlsx")

def simulate_chiller(ch_no):
    df = load_book1()
    row = df.iloc[ch_no % len(df)]
    return {
        "supply_temp": float(row["TEMP"]),
        "return_temp": float(row["RETURN_TEMP"]),
        "flow": float(row["FLOW"]),
        "load": float(row["LOAD"])
    }
