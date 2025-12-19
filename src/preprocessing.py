
"""
Purpose

Read raw CSV plate files
Combine multiple plates
Aggregate replicate wells 
"""

"""
preprocessing.py
----------------
Functions to load and preprocess immunoassay plate data.
"""

from pathlib import Path
import pandas as pd


def read_plate(filepath: str) -> pd.DataFrame:
    """
    Load a single plate CSV file and add a Plate column.
    """
    df = pd.read_csv(filepath)
    df.columns = [c.strip() for c in df.columns]

    required = {"Well", "Type", "Sample_ID", "Concentration", "Signal"}
    if not required.issubset(df.columns):
        raise ValueError(f"Missing required columns in {filepath}")

    df["Plate"] = Path(filepath).stem
    return df

"""
def process_raw_folder(folder: str = "data/raw") -> pd.DataFrame:
    
    #Load all plate CSVs in data/raw.
    
    files = list(Path(folder).glob("*.csv"))
    if not files:
        raise FileNotFoundError("No CSV files found in data/raw")

    dfs = [read_plate(f) for f in files]
    return pd.concat(dfs, ignore_index=True)

def process_raw_folder(folder="data/raw") -> pd.DataFrame:
    
    Load all plate CSVs in data/raw (relative to project root).
    
    folder = Path(folder).resolve()
    files = list(folder.glob("*.csv"))

    if not files:
        raise FileNotFoundError(f"No CSV files found in {folder}")

    dfs = [read_plate(f) for f in files]
    return pd.concat(dfs, ignore_index=True)
"""
from pathlib import Path
import pandas as pd


def process_raw_folder(folder="data/raw") -> pd.DataFrame:
    """
    Load all plate CSVs relative to project root.
    """
    # src/preprocessing.py → project root is one level up
    project_root = Path(__file__).resolve().parents[1]

    folder_path = project_root / folder
    files = list(folder_path.glob("*.csv"))

    if not files:
        raise FileNotFoundError(f"No CSV files found in {folder_path}")

    dfs = [read_plate(f) for f in files]
    return pd.concat(dfs, ignore_index=True)


def aggregate_replicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate replicate wells per sample.
    """
    agg = (
        df.groupby(["Plate", "Type", "Sample_ID"], as_index=False)
        .agg(
            Concentration=("Concentration", "mean"),
            Signal_mean=("Signal", "mean"),
            Signal_std=("Signal", "std"),
            N=("Signal", "count"),
        )
    )
    return agg


def save_processed(df: pd.DataFrame, outfile="data/processed/qc_summary.csv"):
    """
    Save processed data to disk.
    """
    Path(outfile).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(outfile, index=False)
    print(f"Saved processed data → {outfile}")
