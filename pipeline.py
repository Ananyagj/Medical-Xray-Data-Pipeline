import os
import shutil
import logging
import sqlite3
import pandas as pd
from PIL import Image

RAW_FOLDER = "raw_data"
LANDING_FOLDER = "landing"
QUARANTINE_FOLDER = "quarantine"
SILVER_FOLDER = "silver"
GOLD_FOLDER = "gold"

os.makedirs(LANDING_FOLDER, exist_ok=True)
os.makedirs(QUARANTINE_FOLDER, exist_ok=True)
os.makedirs(SILVER_FOLDER, exist_ok=True)
os.makedirs(GOLD_FOLDER, exist_ok=True)

# Clear old processed files before each run
for folder in [LANDING_FOLDER, SILVER_FOLDER, GOLD_FOLDER]:
    for file in os.listdir(folder):
        os.remove(os.path.join(folder, file))

logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Pipeline started")

data = []
copied = valid = invalid = 0

for file in os.listdir(RAW_FOLDER):
    source = os.path.join(RAW_FOLDER, file)
    landing = os.path.join(LANDING_FOLDER, file)

    if os.path.isfile(source):
        shutil.copy2(source, landing)
        copied += 1

        try:
            img = Image.open(landing)
            width, height = img.size

            category = "PNEUMONIA" if "person" in file.lower() else "NORMAL"

            # Silver image (256x256)
            silver_img = img.resize((256, 256))
            silver_path = os.path.join(SILVER_FOLDER, file)
            silver_img.save(silver_path)

            # Gold image (224x224 - ML ready)
            gold_img = img.resize((224, 224))
            gold_img.save(os.path.join(GOLD_FOLDER, file))

            data.append({
                "filename": file,
                "category": category,
                "width": width,
                "height": height,
                "format": img.format
            })

            valid += 1

        except:
            shutil.move(landing, os.path.join(QUARANTINE_FOLDER, file))
            invalid += 1

df = pd.DataFrame(data)
df.to_csv("metadata.csv", index=False)
# Save metadata to SQLite
conn = sqlite3.connect("metadata.db")
df.to_sql("xray_metadata", conn, if_exists="replace", index=False)
conn.close()

print(f"Copied: {copied}")
print(f"Valid: {valid}")
print(f"Invalid: {invalid}")
print("Silver images created")
print("Gold images created")
logging.info(f"Copied: {copied}")
logging.info(f"Valid: {valid}")
logging.info(f"Invalid: {invalid}")
logging.info("Pipeline completed successfully")