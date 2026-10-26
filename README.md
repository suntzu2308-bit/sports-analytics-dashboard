# Sports Analytics Dashboard

A reproducible **Python + SQLite sports analytics portfolio demonstration** using fabricated match results. This project showcases data quality checks, team KPI aggregation, SQL reporting, and generation of a static SVG chart. It is **not yet an interactive dashboard**.

## Run locally
Requirements: Python 3.10+; standard library only.

```bash
python src/analyze.py
python -m unittest discover -s tests -v
```

Run commands from the repository root. The analysis writes `output/team_kpis.csv` and `output/kpi_chart.svg` (the output directory is created automatically).

## Key performance indicators
- Games and wins per team
- Win percentage
- Average points scored and allowed
- Aggregate point differential

The same calculations are expressed in `sql/kpis.sql` for a SQLite table named `games`. Import `data/games.csv` into that table to execute the SQL.

## Structure
- `data/games.csv` — synthetic, invented team scores
- `src/analyze.py` — CSV validation, KPI calculations and SVG export
- `sql/kpis.sql` — SQL aggregation
- `tests/test_analyze.py` — basic automated tests
- `output/` — generated outputs (not committed)

## Data quality and limitations
The pipeline checks missing fields, duplicate IDs, dates, self-matchups and nonnegative integer scores. This small synthetic sample is **not evidence of real team performance**. It does not include schedule adjustment, uncertainty intervals, predictive validation or an interactive dashboard. Tied games do not count as wins. Future development: add a Streamlit dashboard, larger licensed datasets, CI, and SQL/Python parity tests.

## License
MIT. No private data, API credentials, or proprietary sports models are included.
