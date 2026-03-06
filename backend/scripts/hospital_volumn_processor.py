from pathlib import Path
import sys
import pandas as pd

sys.path.append(str(Path(__file__).resolve().parents[1]))
from services.data_loader import load_csv


def filter_since(df: pd.DataFrame, cutoff: str = "2023-01-01") -> pd.DataFrame:
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    return df[df["Date"] >= cutoff].copy()


def main() -> None:
    df = load_csv("Hospital_Service_Volumes_20260306.csv")

    if df.empty:
        print("Loaded file, but it contains 0 rows.")
        return

    print(f"Loaded OK: {len(df)} rows, {len(df.columns)} columns")
    print("Columns:", list(df.columns))

    # drop rows during covid
    before_count = len(df)
    df = filter_since(df, "2023-01-01")
    print(f"Filtered Date >= 2023-01-01: {before_count} -> {len(df)} rows")


if __name__ == "__main__":
    main()
