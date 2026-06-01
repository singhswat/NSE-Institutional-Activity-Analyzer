# NSE Institutional Activity Analyzer

A Python MVP application to collect NSE end-of-day data, store it in Supabase, and calculate accumulation/distribution signals for NSE stocks.

## What this MVP does

- Loads NSE-style end-of-day stock data
- Loads delivery quantity and delivery percentage when available
- Stores data in Supabase PostgreSQL
- Calculates:
  - 20-day average volume
  - Volume ratio
  - Accumulation score
  - Distribution score
  - Signal classification
- Exposes FastAPI endpoints for dashboard use

## What this MVP does not do

- It does not use live market feeds
- It does not claim exact buy/sell quantity
- It does not automate trading
- It does not give financial advice

The purpose is to avoid misleading "buy quantity/sell quantity" traps and instead classify likely accumulation or distribution using EOD data.

---

## Project Structure

```text
app/
  collectors/       NSE data loaders
  processors/       Scoring and signal logic
  database/         Supabase client
  api/              FastAPI app
  jobs/             Daily import job
sql/                Supabase SQL schema
sample_data/        Demo CSV files
tests/              Regression tests
```

---

## Setup

### 1. Create Supabase Project

Create a Supabase project and copy:

- Project URL
- Service role key

### 2. Run SQL Schema

Open Supabase SQL Editor and run:

```sql
sql/schema.sql
```

### 3. Create `.env`

Copy:

```bash
cp .env.example .env
```

Update:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
```

### 4. Install Python Packages

```bash
pip install -r requirements.txt
```

### 5. Run Sample Import

```bash
python -m app.jobs.daily_import --sample
```

To import a legacy or current NSE equity bhavcopy-style CSV instead:

```bash
python -m app.jobs.daily_import --file path/to/bhavcopy.csv
```

### 6. Start API

```bash
uvicorn app.api.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

---

## Tests

```bash
pip install -r requirements-dev.txt
pytest
```

---

## Main API Endpoints

```text
GET /health
GET /signals/latest
GET /signals/accumulation
GET /signals/distribution
GET /stocks/{symbol}/history
```

---

## Scoring Logic

### Accumulation Score

Positive factors:

- Price up
- Volume ratio high
- Delivery percentage high
- Close near high

### Distribution Score

Negative factors:

- Price down
- Volume ratio high
- Delivery percentage high
- Close near low

The application avoids saying:

```text
Buy quantity = X
Sell quantity = Y
```

because EOD data cannot prove this.

Instead it says:

```text
Likely Accumulation
Likely Distribution
Neutral
Watchlist
```

---

## Next Steps

Recommended next build items:

1. Add automated NSE report downloads
2. Add NSE delivery report parser
3. Add F&O OI data
4. Add sector-level dashboard
5. Add WhatsApp or Telegram alerts
6. Add AI-generated daily commentary
