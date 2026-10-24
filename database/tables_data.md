# Project Database Tables & Records

## 1. Table: `auth_user` (User Accounts)

| ID | Username | Email | Role | Active Status | Date Registered |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `admin` | abhishekzure34@gmail.com | Admin (Staff) | Active | 2026-10-18 13:41 |
| 3 | `abhizure` | abhishekzure21@gmail.com | Regular User | Active | 2026-10-18 14:28 |
| 4 | `normaluser` | normal@example.com | Regular User | Inactive | 2026-10-18 16:42 |
| 5 | `test_buyer` | buyer@test.com | Regular User | Inactive | 2026-10-18 16:56 |
| 6 | `test_admin` | admin@test.com | Regular User | Inactive | 2026-10-18 16:56 |


## 2. Table: `predictor_prediction` (House Price Valuations)

| ID | User | City | Tier | BHK | Super Area | Carpet Area | Floor | Furnishing | Metro Dist | Crime Index | Predicted Market Price | Date |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 27 | `abhizure` | Pune | Mid | 2 BHK | 1,000 sqft | 800 sqft | 3/10 | Semi-Furnished | 2.0 km | 30.0 | **₹ 7,526,773** | 2026-10-21 07:39 |
| 26 | `abhizure` | Pune | Premium | 5 BHK | 2,500 sqft | 2,200 sqft | 25/35 | Fully-Furnished | 2.0 km | 30.0 | **₹ 20,281,946** | 2026-10-21 05:44 |
| 25 | `abhizure` | Pune | Mid | 2 BHK | 1,000 sqft | 800 sqft | 3/10 | Semi-Furnished | 2.0 km | 30.0 | **₹ 7,526,773** | 2026-10-21 05:03 |
| 24 | `abhizure` | Nagpur | Budget | 1 BHK | 1,000 sqft | 800 sqft | 3/10 | Semi-Furnished | 2.0 km | 30.0 | **₹ 4,172,458** | 2026-10-21 04:28 |
| 23 | `abhizure` | Nagpur | Budget | 1 BHK | 1,000 sqft | 800 sqft | 3/10 | Semi-Furnished | 2.0 km | 30.0 | **₹ 4,172,458** | 2026-10-21 04:28 |
| 22 | `abhizure` | Nagpur | Budget | 1 BHK | 1,000 sqft | 800 sqft | 3/10 | Semi-Furnished | 2.0 km | 30.0 | **₹ 4,172,458** | 2026-10-21 04:28 |
| 21 | `abhizure` | Pune | Mid | 1 BHK | 1,000 sqft | 200 sqft | 2/10 | Unfurnished | 2.0 km | 30.0 | **₹ 8,584,562** | 2026-10-20 18:08 |
| 20 | `abhizure` | Pune | Mid | 2 BHK | 800 sqft | 100 sqft | 3/10 | Unfurnished | 10.0 km | 30.0 | **₹ 6,391,663** | 2026-10-20 17:18 |
| 19 | `abhizure` | Pune | Mid | 2 BHK | 2,000 sqft | 100 sqft | 3/10 | Unfurnished | 10.0 km | 30.0 | **₹ 16,580,827** | 2026-10-20 17:17 |
| 18 | `abhizure` | Pune | Mid | 2 BHK | 1,000 sqft | 100 sqft | 3/10 | Unfurnished | 10.0 km | 30.0 | **₹ 7,895,489** | 2026-10-20 17:17 |
| 17 | `abhizure` | Pune | Mid | 2 BHK | 1,000 sqft | 800 sqft | 3/10 | Unfurnished | 10.0 km | 30.0 | **₹ 7,940,959** | 2026-10-20 17:16 |
| 16 | `abhizure` | Pune | Mid | 2 BHK | 1,000 sqft | 800 sqft | 3/10 | Unfurnished | 10.0 km | 30.0 | **₹ 8,532,152** | 2026-10-20 17:16 |
| 15 | `abhizure` | Pune | Mid | 2 BHK | 1,000 sqft | 800 sqft | 3/10 | Unfurnished | 10.0 km | 30.0 | **₹ 8,531,621** | 2026-10-20 17:16 |
| 14 | `abhizure` | Pune | Mid | 2 BHK | 1,000 sqft | 800 sqft | 3/10 | Semi-Furnished | 10.0 km | 30.0 | **₹ 8,662,234** | 2026-10-20 17:16 |
| 13 | `abhizure` | Pune | Mid | 2 BHK | 1,000 sqft | 800 sqft | 3/10 | Semi-Furnished | 2.0 km | 30.0 | **₹ 8,791,033** | 2026-10-20 17:16 |
| 12 | `abhizure` | Pune | Mid | 2 BHK | 1,000 sqft | 800 sqft | 3/10 | Semi-Furnished | 2.0 km | 30.0 | **₹ 8,805,850** | 2026-10-20 17:15 |
| 11 | `abhizure` | Pune | Premium | 2 BHK | 1,000 sqft | 800 sqft | 3/10 | Semi-Furnished | 2.0 km | 30.0 | **₹ 10,638,867** | 2026-10-20 16:23 |
| 10 | `abhizure` | Bangalore | Premium | 2 BHK | 1,000 sqft | 800 sqft | 3/10 | Semi-Furnished | 2.0 km | 30.0 | **₹ 11,955,135** | 2026-10-20 16:23 |
| 9 | `abhizure` | Mumbai | Premium | 2 BHK | 1,000 sqft | 800 sqft | 3/10 | Semi-Furnished | 2.0 km | 30.0 | **₹ 19,552,570** | 2026-10-20 16:23 |
| 8 | `abhizure` | Mumbai | Mid | 2 BHK | 1,000 sqft | 800 sqft | 3/10 | Semi-Furnished | 2.0 km | 30.0 | **₹ 15,422,325** | 2026-10-20 16:22 |
| 7 | `abhizure` | Mumbai | Budget | 2 BHK | 1,000 sqft | 800 sqft | 3/10 | Semi-Furnished | 2.0 km | 30.0 | **₹ 12,412,182** | 2026-10-20 16:22 |
| 6 | `abhizure` | Pune | Budget | 2 BHK | 1,000 sqft | 800 sqft | 3/10 | Semi-Furnished | 2.0 km | 30.0 | **₹ 6,380,829** | 2026-10-20 16:22 |
| 5 | `abhizure` | Pune | Budget | 2 BHK | 1,000 sqft | 800 sqft | 3/10 | Semi-Furnished | 2.0 km | 30.0 | **₹ 6,380,829** | 2026-10-20 16:22 |
| 4 | `abhizure` | Pune | Budget | 2 BHK | 1,500 sqft | 100 sqft | 3/10 | Unfurnished | 10.0 km | 30.0 | **₹ 9,447,914** | 2026-10-19 20:29 |
| 3 | `abhizure` | Pune | Mid | 2 BHK | 1,500 sqft | 100 sqft | 3/10 | Unfurnished | 10.0 km | 30.0 | **₹ 12,979,959** | 2026-10-19 20:29 |
