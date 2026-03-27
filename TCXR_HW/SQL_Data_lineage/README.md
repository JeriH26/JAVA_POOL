# TCXR Homework 1: SQL and Data Lineage

**Estimated Time:** 30-60 minutes

You are employed at company XYZ, where raw product data across warehouses and stores must be made useful for stakeholders, typically internal leaders at the director level and above. This is the raw data you were provided with:

## Raw Data

This is the data and schema given. Each row in this table corresponds to a product that has been manufactured and sold.

| Column | Data Type | Description |
| --- | --- | --- |
| `product_id (PK)` | `INT` | Unique integer corresponding to each product |
| `product_name` | `String` | Name of product (Note that two bicycles will have different `product_ids`, but the same `product_name`) |
| `warehouse` | `String` | Warehouse product was manufactured in |
| `store` | `String` | Store product was sold in |
| `price` | `FLOAT` | Selling price of product |
| `cost` | `FLOAT` | Manufacturing cost of product |
| `date_sold` | `datetime` | Selling date of product |
| `date_manufactured` | `datetime` | Manufacturing date of product |

The analyst reported that they believed the product name was no longer required due to id being sufficient so they dropped it. They also knew the product price was in Japanese Yen currency so they changed the price schema to reflect that for efficiency. They noticed that the warehouse had a single letter and 7 digit integer that followed it (e.g. `W8475839`, `L5749302`, etc.). To save space, they made a column for the warehouse letter and split the number into a new column.

Here is the new schema:

| Column | Data Type | Description |
| --- | --- | --- |
| `product_id (PK)` | `INT` | Unique integer corresponding to each product |
| `warehouse_letter` | `Char` | Warehouse prepended letter product was manufactured in |
| `warehouse_num_id` | `INT` | Warehouse integer product was manufactured in |
| `store` | `String` | Store product was sold in |
| `price` | `FLOAT` | Selling price of product |
| `cost` | `FLOAT` | Manufacturing cost of product |
| `date_sold` | `DATE` | Selling date of product |
| `date_manufactured` | `DATE` | Manufacturing date of product |

## Task

Your task is to review the analyst's work as follows (approximately 45 minutes):

If you cannot answer a question, simply state that and move on to the next one.

1. What are some potential issues of the analyst's changes? How could this affect both incoming data and downstream consumers?
2. Did the analyst perform any changes not seen in their report? What are the potential consequences of those change(s)?
3. We need the warehouse columns to be appended back together. Create an SQL query that combines the two columns to the previous output.
4. How would you better track the lineage of this data and ensure the analyst's assumptions and expectations align with the stakeholder's requirements?

## Answer (assisted by Github Copilot)

### 1. Potential issues with the analyst's changes

| Change | Problem | Impact |
| --- | --- | --- |
| Dropped `product_name` | `product_id` is just a number — stakeholders can't read it | Reports and dashboards lose human-readable context; downstream consumers may need a separate join just to get the name back |
| `price` "relabeled" as JPY | The column type didn't change; no currency field was added | Future data in a different currency would look identical; consumers may assume wrong units and produce incorrect financial totals |
| `warehouse` split into letter + number | Assumes format is always exactly 1 letter + 7 digits | If future warehouse codes differ (e.g. two letters, or leading zeros), the split logic breaks or silently produces wrong values |
| `warehouse_num_id` stored as `INT` | Integers drop leading zeros (e.g. `0123456` → `123456`) | Reconstructing the original warehouse code later produces the wrong identifier |

### 2. Changes not clearly disclosed in the analyst's report

Yes. The analyst changed `date_sold` and `date_manufactured` from `datetime` to `DATE`, but this was not mentioned in the report.

**Impact of datetime → DATE conversion:**

| Issue | Example |
| --- | --- |
| **Sales sequencing** | Two sales on the same day: 10:00 AM and 3:00 PM. Originally distinguishable by timestamp, now both show the same date with no order information. |
| **Latency measurement** | Manufactured: Jan 1 at 9:00 PM. Sold: Jan 2 at 8:00 AM. Originally: 11 hours latency. Now: only "1 day difference" with no precision. |
| **Deduplication risk** | Systems using timestamps to prevent duplicate imports may now process the same day's multiple transactions twice or more. |
| **Business logic failure** | Rules like "ship within 24 hours" can be precisely verified with timestamps, but not with dates alone. |

**Additional undisclosed change: `price` currency ambiguity**

The analyst claimed to change the schema to reflect Japanese Yen, but:

- The column name (`price`) and data type (`FLOAT`) did not change
- No `currency` field was added to explicitly label the unit
- No documentation shows whether values were actually **converted** (e.g., USD × 130 = JPY) or only **relabeled**

**Risk:** Downstream systems may assume the wrong currency unit, leading to incorrect financial calculations and cross-table inconsistencies. For example, if other tables still use USD prices, merging the data without conversion metadata could produce wildly incorrect aggregations.

### 3. SQL query to combine warehouse columns back together

If the warehouse code is exactly one letter followed by the numeric identifier, a simple reconstruction would be:

```sql
SELECT
	product_id,
	CONCAT(warehouse_letter, warehouse_num_id) AS warehouse,
	store,
	price,
	cost,
	date_sold,
	date_manufactured
FROM transformed_products;
```

If the numeric portion must always be 7 digits, then zero-padding should be used to avoid losing formatting when `warehouse_num_id` is stored as an integer:

```sql
SELECT
	product_id,
	CONCAT(warehouse_letter, LPAD(CAST(warehouse_num_id AS CHAR), 7, '0')) AS warehouse,
	store,
	price,
	cost,
	date_sold,
	date_manufactured
FROM transformed_products;
```

The second version is safer because it preserves the expected warehouse format.

### 4. Better ways to track lineage and align with stakeholder requirements

**Step 1 — Document every change**

For each schema modification, record:

| Field | Example |
| --- | --- |
| What changed | `warehouse` split into `warehouse_letter` + `warehouse_num_id` |
| Why | To save storage space |
| Who approved | Analyst name + stakeholder sign-off |
| When | Date of change |
| Impact | Downstream queries must reconstruct the column to use it |

**Step 2 — Maintain a source-to-target lineage map**

A simple table showing what happened to each column:

| Original Column | Change | New Column(s) | Information Lost? |
| --- | --- | --- | --- |
| `product_name` | Dropped | — | Yes — human-readable name gone |
| `warehouse` | Split | `warehouse_letter`, `warehouse_num_id` | Possibly — leading zeros at risk |
| `date_sold` | Type narrowed | `date_sold (DATE)` | Yes — time of day lost |
| `date_manufactured` | Type narrowed | `date_manufactured (DATE)` | Yes — time of day lost |
| `price` | Relabeled as JPY | `price` | Unclear — no conversion record |

**Step 3 — Get stakeholder sign-off before dropping or changing fields**

Before removing `product_name` or changing `datetime` to `DATE`, ask:
- Do any dashboards or reports use this field?
- Does any downstream system depend on the time component?
- Has the business confirmed this change is safe?

**Step 4 — Add automated checks in the pipeline**

| Check | Purpose |
| --- | --- |
| Row count before vs. after | Detect accidental data loss |
| Schema diff alert | Flag any unexpected type changes |
| Warehouse format validation | Ensure value matches pattern `[A-Z][0-9]{7}` |
| Null checks on key columns | Catch missing data early |
| Timestamp truncation warning | Alert when `datetime` is cast to `date` |