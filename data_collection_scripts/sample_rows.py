import pandas as pd
import argparse


parser = argparse.ArgumentParser(description="sampler")
parser.add_argument("--filename", type=str)
parser.add_argument("--nonenglish", action="store_true")
parser.add_argument("--output", type=str)
args = parser.parse_args()

df = pd.read_csv(args.filename, low_memory=False)

if args.nonenglish:
    try:
        df = df[df['detected_language'] != 'en']
    except:
        df = df[df['overall'] != 'en']

sampled_df = df.sample(n=100, random_state=1)  # Set random_state for reproducibility

# Output the sampled DataFrame to a CSV file
sampled_df.to_csv(args.output, index=False)
