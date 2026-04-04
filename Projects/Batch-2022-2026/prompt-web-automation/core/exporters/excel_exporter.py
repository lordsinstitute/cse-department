"""Export extracted data to Excel/CSV using pandas."""

import os
from datetime import datetime
import pandas as pd
from config import Config


def export_to_excel(data, filename=None, export_dir=None):
    """Export list of dicts to an Excel file.

    Args:
        data: List of dicts (each dict is a row)
        filename: Optional filename (auto-generated if not provided)
        export_dir: Directory to save (defaults to Config.EXPORT_DIR)

    Returns:
        Full path to the saved file
    """
    if not data:
        raise ValueError("No data to export.")

    export_dir = export_dir or Config.EXPORT_DIR
    os.makedirs(export_dir, exist_ok=True)

    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"scraped_data_{timestamp}.xlsx"

    if not filename.endswith(".xlsx"):
        filename += ".xlsx"

    filepath = os.path.join(export_dir, filename)
    df = pd.DataFrame(data)
    df.to_excel(filepath, index=False, engine="openpyxl")

    return filepath


def export_to_csv(data, filename=None, export_dir=None):
    """Export list of dicts to a CSV file.

    Args:
        data: List of dicts (each dict is a row)
        filename: Optional filename (auto-generated if not provided)
        export_dir: Directory to save (defaults to Config.EXPORT_DIR)

    Returns:
        Full path to the saved file
    """
    if not data:
        raise ValueError("No data to export.")

    export_dir = export_dir or Config.EXPORT_DIR
    os.makedirs(export_dir, exist_ok=True)

    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"scraped_data_{timestamp}.csv"

    if not filename.endswith(".csv"):
        filename += ".csv"

    filepath = os.path.join(export_dir, filename)
    df = pd.DataFrame(data)
    df.to_csv(filepath, index=False)

    return filepath
