import pandas as pd
from sklearn.model_selection import train_test_split
import os

CLASSES = ["classical", "hiphop", "metal"]

# Collect data
labels = []
paths = []

for c in CLASSES:
    for track in os.listdir(c+"/"):
        labels.append(c)
        paths.append("../audio_data/gtzan_mini/"+c+"/"+track)

# Store as dataframes
df = pd.DataFrame({"path": paths, "label": labels})

# Train-test Split
df_train, df_test = train_test_split(df, test_size=0.1)

# Export
df_train.to_csv("gtzan_mini_train.csv", index=False)
df_test.to_csv("gtzan_mini_test.csv", index=False)