# Réponses
## Step 1: Discorver the Data
- *How many columns does products.csv have? Which ones start with _ (internal columns)?*

product.csv a 21 colonnes
Celles commençant par “_” sont les suivantes: _internal_cost_usd, _supplier_id, _warehouse_location, _internal_cost_code   

- *How many columns does users.csv have? Can you spot PII (passwords, IPs)?*

users.csv a 28 colonnes
Les PII correspondent aux colonnes _hashed_password et _last_ip


- *In orders.csv, what are the possible values for status?*

Les valeurs possible pour la colonne status sont les suivantes: ['delivered', 'shipped', 'returned', 'chargeback', 'cancelled', 'processing']

- *In order_line_items.csv, does line_total_usd ≈ unit_price_usd × quantity?*

df["prix_tous_produits"] = df["unit_price_usd"] * df["quantity"]
df["diff"] = df["line_total_usd"] - df["prix_tous_produits"]
print(df[["line_total_usd", "unit_price_usd", "quantity", "prix_tous_produits", "diff"]])

La différence est nulle sur toutes les lignes

- *In reviews.jsonl, which columns start with _? What do _moderation_score and _sentiment_raw look like?*

Les colonnes qui commencent par “_” sont les suivantes: _moderation_score, _sentiment_raw, _toxicity_score, _language_detected, _review_source

_moderation_score et _sentiment_raw sont des float allant de 0 à 1.

- *In the clickstream Parquet file, what does the event_type column contain? What _-columns exist?*

La colonne event_type contient uniquement la valeur “pageview”.

Les colonnes qui commencent par “_” sont les suivantes: _ga_client_id, _gtm_container_id, _dom_interactive_ms, _dom_complete_ms, _ttfb_ms, _connection_type, _js_heap_size_mb, _consent_string