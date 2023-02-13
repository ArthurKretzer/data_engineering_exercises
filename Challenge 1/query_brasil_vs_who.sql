WITH setup as (
    SELECT "date", 
        home_team, 
        away_team,
        home_score,
        away_score,
        CASE
            WHEN home_score = away_score THEN 'draw'
            WHEN home_score > away_score THEN 'home team'
            WHEN away_score > home_score THEN 'away team'
        END AS winner
    
    FROM "Results"
    
    WHERE home_team = 'Brazil' or away_team = 'Brazil'
),

aux as (
SELECT *,
    'Brazil' as team_1,
    CASE WHEN home_team = 'Brazil' then away_team ELSE home_team END as team_2
FROM setup
)

SELECT team_2 as adversário,
    count(*) as jogos

FROM aux

GROUP BY 1

ORDER BY 2 desc

LIMIT 20