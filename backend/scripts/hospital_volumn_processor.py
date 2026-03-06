from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from services.data_loader import load_csv

df = load_csv("Hospital_Service_Volumes_20260306.csv")

if df.empty:
    print("Loaded file, but it contains 0 rows.")
else:
    print(f"Loaded OK: {len(df)} rows, {len(df.columns)} columns")
    print("Columns:", list(df.columns))

