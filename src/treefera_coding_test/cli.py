import argparse
import os
import pandas as pd

from treefera_coding_test.models.v1 import v1

def parse_args():
    parser = argparse.ArgumentParser(description="Treefera Coding Test")
    parser.add_argument("--crop", default="fr_de_wheat", help="Crop to analyse")
    parser.add_argument("--season", default=2024, help="Season to analyse")
    parser.add_argument("--as-of", required=True, help="Use data up to this date (YYYY-MM-DD)")
    parser.add_argument("--version", default="v1", help="Model version label")
    parser.add_argument("--artefact-dir", default=os.getenv("ARTEFACT_DIR", "artefacts"))
    return parser.parse_args()


def save_artefacts(metadata, artefact_dir):
    os.makedirs(artefact_dir, exist_ok=True)
    metadata_path = os.path.join(artefact_dir, "metadata.json")
    pd.Series(metadata).to_json(metadata_path)
    print(f"Saved metadata to {metadata_path}")


def save_output(yield_forecast, out_path):
    df = yield_forecast.to_dataframe(name="yield_pred").reset_index()
    df.to_csv(out_path, index=False)
    print(f"Saved yield forecast to {out_path}")

def main():

    # Define the available model versions and their corresponding functions
    MODELS = {"v1": v1}    

    # Get command-line arguments
    args = parse_args()
    as_of = pd.Timestamp(args.as_of)
    season = args.season
    crop = args.crop
    model_version = args.version

    artefact_dir = args.artefact_dir
    # Define the output path for the yield forecast CSV file
    out_path = os.path.join(artefact_dir, f"{crop}_forecast_{model_version}.csv")

    # Save metadata about the run, including the model version, as_of date, crop, and season
    metadata = {
        "version": model_version,
        "as_of": as_of.date().isoformat(), 
        "crop": crop,
        "season": season,
    }

    save_artefacts(metadata, artefact_dir)

    yield_forecast = MODELS[model_version](crop=crop, season=season, as_of_date=as_of)

    save_output(yield_forecast, out_path)

    return yield_forecast

if __name__ == "__main__":
    main()