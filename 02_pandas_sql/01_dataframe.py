import os

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

r = requests.get(
    "https://api.github.com/orgs/odoo/repos",
    params={"per_page": 100},
    headers={"Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}"},
    timeout=10,
)
r.raise_for_status()

df = pd.DataFrame(r.json())

print("Filas y columnas:", df.shape)
print()

df = df[["name", "language", "stargazers_count", "forks_count", "created_at", "archived"]]

df = df.sort_values(by="stargazers_count", ascending=False)
df = df.reset_index(drop=True)

print(df.head())
print()
print(df.dtypes)
print(df["created_at"].dtype)
print(df["archived"].dtype)
print(df["stargazers_count"].dtype)
 