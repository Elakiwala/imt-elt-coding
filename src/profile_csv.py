import boto3, os
from io import StringIO
import pandas as pd
from dotenv import load_dotenv
from io import StringIO
from io import BytesIO
import pyarrow.parquet as pq


load_dotenv()

s3 = boto3.client("s3",
    region_name="eu-west-3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

# --- CSV: Read products.csv ---
response = s3.get_object(Bucket="kickz-empire-data", Key="raw/order_line_items/order_line_items.csv")
df = pd.read_csv(StringIO(response["Body"].read().decode("utf-8")))

print(df.shape)        # rows × columns
print(df.dtypes)       # column types

df["prix_tous_produits"] = df["unit_price_usd"] * df["quantity"]
df["diff"] = df["line_total_usd"] - df["prix_tous_produits"]
print(df[["line_total_usd", "unit_price_usd", "quantity", "prix_tous_produits", "diff"]].head(10))
res = (df["diff"].abs() < 0.01).all() 

print("Toutes les lignes correspondent:", res)


"""print(df.head())       # first rows
print(df.describe())   # statistics"""


"""#--- JSONL: Read reviews.jsonl ---
response = s3.get_object(Bucket="kickz-empire-data", Key="raw/reviews/reviews.jsonl")
jsonl_content = response["Body"].read().decode("utf-8")

# pd.read_json() with lines=True reads one JSON object per line
df_reviews = pd.read_json(StringIO(jsonl_content), lines=True)"""

"""print(df_reviews.shape)
print(df_reviews.dtypes)
print(df_reviews.head())
"""
"""print(df_reviews[["_moderation_score", "_sentiment_raw"]].head(10))
#print(df_reviews[["_moderation_score", "_sentiment_raw"]].dtypes)
print("Moderation scores:", df_reviews["_moderation_score"].unique())
print("Sentiment raw:", df_reviews["_sentiment_raw"].unique())
#print(df_reviews["_moderation_score"].describe())
print(df_reviews["_sentiment_raw"].value_counts())"""

"""
# --- Parquet: Read a single partition file ---
response = s3.get_object(
    Bucket="kickz-empire-data",
    Key="raw/clickstream/dt=2026-02-05/part-00001.snappy.parquet"
)
table = pq.read_table(BytesIO(response["Body"].read()))
df_click = table.to_pandas()

print(df_click.shape)
print(df_click.dtypes)
print(df_click.head())

print(df_click["event_type"].unique())
print(df_click["event_type"].value_counts())
print(df_click["event_type"])
"""