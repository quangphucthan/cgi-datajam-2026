from pathlib import Path
import sys
import pandas as pd

sys.path.append(str(Path(__file__).resolve().parents[1]))
from services.data_loader import load_csv


# time filter
def filter_since(df: pd.DataFrame, cutoff: str = "2023-01-01") -> pd.DataFrame:
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    return df[df["Date"] >= cutoff].copy()


def drop_invalid_ctas_rows(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    ctas_numeric = pd.to_numeric(df["CTAS"], errors="coerce")
    is_emergency_ctas_measure = df["Measure Name"].eq("Emergency Visits CTAS")
    invalid_ctas = ctas_numeric.isna()
    return df[~(is_emergency_ctas_measure & invalid_ctas)].copy()


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

    # drop rows with measure name = "Emergency Visits CTAS" and CTAS = "Blank" or any non numeric value
    before_count = len(df)
    df = drop_invalid_ctas_rows(df)
    print(
        "Dropped invalid Emergency Visits CTAS rows: "
        f"{before_count} -> {len(df)} rows"
    )

    # output a processed dataset to processed folder
    output_path = Path(__file__).resolve().parents[1] / "data" / "processed" / "Hospital_Service_Volumes_processed.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Saved processed dataset: {output_path}")

if __name__ == "__main__":
    main()
