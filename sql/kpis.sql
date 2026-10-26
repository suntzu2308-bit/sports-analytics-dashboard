-- SQLite: load data/games.csv into a table named games.
-- Each game contributes one record for each participating team.
WITH team_games AS (
 SELECT home_team AS team, home_score AS scored, away_score AS allowed FROM games
 UNION ALL
 SELECT away_team AS team, away_score AS scored, home_score AS allowed FROM games
)
SELECT team, COUNT(*) AS games,
 SUM(CASE WHEN scored > allowed THEN 1 ELSE 0 END) AS wins,
 ROUND(1.0 * SUM(CASE WHEN scored > allowed THEN 1 ELSE 0 END) / COUNT(*), 3) AS win_pct,
 ROUND(AVG(scored), 2) AS avg_scored,
 ROUND(AVG(allowed), 2) AS avg_allowed,
 SUM(scored - allowed) AS point_diff
FROM team_games GROUP BY team ORDER BY win_pct DESC, team;
