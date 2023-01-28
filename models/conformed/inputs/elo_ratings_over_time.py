import pandas as pd

def calc_elo_diff(game_result: int, home_elo: float, visiting_elo: float) -> float:
    return 25.0 * (( game_result ) - (1.0 / (10.0 ** (-(visiting_elo - home_elo - 70) / 400.0) + 1.0)))

def model(dbt, sess):
    # get the existing elo ratings for the teams
    team_ratings = dbt.ref("prep_team_ratings").df()
    original_elo = dict(zip(team_ratings["team"], team_ratings["elo_rating"].astype(float)))
    working_elo = original_elo.copy()

    # loop over the historical game data and update the elo ratings as we go
    nba_elo_latest = (dbt.ref("prep_nba_elo_latest")
        .project("game_id, visiting_team, home_team, winning_team, game_result")
        .order("game_id")
    )
    nba_elo_latest.execute()
    columns = ["game_id", "visiting_team", "visiting_team_elo_rating", "home_team", "home_team_elo_rating", "winning_team", "elo_change"]
    rows = []
    for (game_id, vteam, hteam, winner, game_result) in nba_elo_latest.fetchall():
        helo, velo = working_elo[hteam], working_elo[vteam]
        elo_change =  calc_elo_diff(game_result, helo, velo)
        rows.append((game_id, vteam, velo, hteam, helo, winner, elo_change))
        working_elo[hteam] -= elo_change
        working_elo[vteam] += elo_change

    return pd.DataFrame(columns=columns, data=rows)