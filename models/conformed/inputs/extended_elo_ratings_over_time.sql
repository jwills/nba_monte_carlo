WITH cte_avg_elo AS (
   SELECT AVG(elo_rating) AS elo_rating
   FROM {{ ref('latest_elo_by_team' ) }}
)
SELECT 
   RL.*, 
   CASE WHEN visiting_team_elo_rating > home_team_elo_rating 
      THEN visiting_team ELSE home_team END AS favored_team,
   CASE WHEN visiting_team_elo_rating > elo_rating THEN 1 ELSE 0 END AS visiting_team_above_avg,
   CASE WHEN home_team_elo_rating > elo_rating THEN 1 ELSE 0 END AS home_team_above_avg
FROM  {{ ref('elo_ratings_over_time') }} RL
LEFT JOIN cte_avg_elo A ON 1=1