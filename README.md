# Sports Analytics Dashboard

**[Launch the live dashboard](https://sports-analytics-dash.streamlit.app)** · [View source code](https://github.com/suntzu2308-bit/sports-analytics-dashboard)

An interactive **Streamlit + Python** portfolio dashboard using **fabricated match results**. Explore team performance through KPI cards, team and date filters, win-percentage and scoring charts, a date-filtered game log, and CSV export. Includes a reproducible standard-library KPI pipeline, SQLite query example, and automated tests.

## Business question
How can an analyst compare team performance consistently across a selected date window without exposing a proprietary forecasting model?

## Demonstrated deliverable
An interactive performance dashboard backed by validated synthetic match records, reproducible Python aggregation, SQLite KPI calculations, and downloadable results. It supports transparent comparisons rather than predictive claims.

## Engineering verification
**7 automated tests** cover data quality, expected KPI calculations, and SQLite-to-Python result parity. GitHub Actions executes tests and the example pipeline on pushes and pull requests.

## Run the interactive dashboard locally

Requires Python 3.10+:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Streamlit will display a local URL (usually http://localhost:8501).

## Run the reproducible pipeline and tests

```bash
python src/analyze.py
python -m unittest discover -s tests -v
```

The pipeline writes `output/team_kpis.csv` and `output/kpi_chart.svg`. GitHub Actions runs the unit tests, pipeline and dashboard syntax check on pushes and pull requests.

## What the dashboard measures
- Games, wins, win percentage, average points scored and allowed, aggregate point differential
- Date-window filters and team comparison
- Downloadable filtered KPI table

**Filtering note:** date filtering determines which games enter the aggregates; team selection determines which teams are displayed. Games against unselected opponents still count in the selected teams' statistics.

## Repository map
- `app.py` — interactive Streamlit dashboard
- `requirements.txt` — dashboard dependencies
- `data/games.csv` — synthetic games
- `src/analyze.py` — CSV validation, aggregation and SVG export
- `sql/kpis.sql` — SQLite aggregation query
- `tests/test_analyze.py` and `tests/test_sql_parity.py` — KPI and SQLite parity tests
- `.github/workflows/tests.yml` — continuous integration

## Data provenance and limitations

Every score and team is fabricated. The eight-game sample is intended for interface and pipeline demonstration, **not prediction or real-world sports conclusions**. It does not include uncertainty intervals, schedule adjustment, out-of-sample validation or proprietary handicapping logic. Ties do not count as wins. SQLite/Python KPI parity is tested on the synthetic fixture; this does not constitute production-data validation. The app is deployed to Streamlit Community Cloud.

## License

MIT. No private data, API credentials or proprietary models are included.
