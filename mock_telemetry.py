import numpy as np
import pandas as pd

OUTPUT_PATH = "telemetry_history.csv"
ROW_COUNT = 2000
DAYS_BACK = 365

BOROUGH_ZIPS = {
    "Manhattan": ["10001", "10025", "10128"],
    "Brooklyn": ["11201", "11215", "11238"],
    "Queens": ["11101", "11354", "11375"],
    "Bronx": ["10451", "10462", "10469"],
    "Staten Island": ["10301", "10304", "10314"],
}
CLASSES = ["Pigeon", "Squirrel", "Rat"]
BASE_WEIGHTS = [0.50, 0.35, 0.15]
SUMMER_WEIGHTS = [0.40, 0.25, 0.35]
SUMMER_MONTHS = {6, 7, 8}


def build_dataframe(now, rng):
    seconds_back = rng.integers(0, DAYS_BACK * 86400, size=ROW_COUNT)
    timestamps = pd.to_datetime(now) - pd.to_timedelta(seconds_back, unit="s")

    boroughs = rng.choice(list(BOROUGH_ZIPS), size=ROW_COUNT)
    zip_codes = [rng.choice(BOROUGH_ZIPS[b]) for b in boroughs]

    is_summer = np.isin(timestamps.month, list(SUMMER_MONTHS))
    classes = np.empty(ROW_COUNT, dtype=object)
    classes[is_summer] = rng.choice(CLASSES, size=is_summer.sum(), p=SUMMER_WEIGHTS)
    classes[~is_summer] = rng.choice(CLASSES, size=(~is_summer).sum(), p=BASE_WEIGHTS)

    df = pd.DataFrame({
        "Timestamp": timestamps.strftime("%Y-%m-%d %H:%M:%S"),
        "Borough": boroughs,
        "Zip_Code": zip_codes,
        "Class_Detected": classes,
        "Inference_Latency_ms": np.round(rng.uniform(15, 45, size=ROW_COUNT), 2),
        "Estimated_Compute_Watts": np.round(rng.uniform(10, 30, size=ROW_COUNT), 2),
    })
    return df.sort_values("Timestamp").reset_index(drop=True)


def main():
    rng = np.random.default_rng()
    df = build_dataframe(pd.Timestamp.now(), rng)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"[TELEMETRY] wrote {len(df)} rows -> {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
