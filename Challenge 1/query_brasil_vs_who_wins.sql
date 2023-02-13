WITH brasil_results as (
    SELECT "date", 
        home_team, 
        away_team,
        home_score,
        away_score,
        CASE
            WHEN home_score = away_score THEN 'draw'
            WHEN home_score > away_score THEN 'home team'
            WHEN away_score > home_score THEN 'away team'
        END AS winner,
        'Brazil' AS team_1,
        CASE
            WHEN home_team = 'Brazil' THEN away_team
            WHEN away_team = 'Brazil' THEN home_team
        END AS team_2,
        CASE
            WHEN (home_score = away_score) THEN 'draw'
            WHEN (home_score > away_score) AND (home_team = 'Brazil') THEN 'win'
            WHEN (home_score > away_score) AND (home_team != 'Brazil') THEN 'loss'
            WHEN (away_score > home_score) AND (away_team = 'Brazil') THEN 'win'
            WHEN (away_score > home_score) AND (away_team != 'Brazil') THEN 'loss'
        END AS brasil_win
    
    FROM "Results"
    
    WHERE home_team = 'Brazil' or away_team = 'Brazil'
    )

-- SELECT * FROM brasil_results

SELECT team_2 as adversário,
    sum(case when brasil_win = 'win' then 1 else 0 end) as wins,
    sum(case when brasil_win = 'draw' then 1 else 0 end) as draws,
    sum(case when brasil_win = 'loss' then 1 else 0 end) as losses,
    count(*) as total_matches
    
FROM brasil_results
GROUP BY adversário
ORDER BY total_matches desc
LIMIT 20
