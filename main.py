import pandas as pd
import numpy as np

def load_data(csv_path):
    print("Loading data...")
    data = pd.read_csv(csv_path)

    # Only keep pitches that were called balls or strikes
    called_pitches = data[data['type'].isin(['B', 'S'])].copy()

    print(f"Loaded {len(called_pitches)} called pitches from {called_pitches['game_pk'].nunique()} games")
    return called_pitches

def identify_missed_calls(df, method='zone'):
    if method == 'zone':
        should_be_strike = df['zone'].between(1, 9)
    elif method == 'precise':
        in_horizontal_bounds = df['plate_x'].between(-0.83, 0.83)
        in_vertical_bounds = (df['plate_z'] >= df['sz_bot']) & (df['plate_z'] <= df['sz_top'])
        should_be_strike = in_horizontal_bounds & in_vertical_bounds
    else:
        raise ValueError("method must be 'zone' or 'precise'")

    was_called_strike = df['type'] == 'S'

    df['should_be_strike'] = should_be_strike
    df['called_strike'] = was_called_strike

    df['call_type'] = 'correct'
    df.loc[should_be_strike & ~was_called_strike, 'call_type'] = 'missed_strike'
    df.loc[~should_be_strike & was_called_strike, 'call_type'] = 'missed_ball'

    return df

# Analyze total impact of missed calls per game
def analyze_call_impact(df):
    missed_calls = df[df['call_type'].isin(['missed_strike', 'missed_ball'])].copy()
    missed_calls['win_exp_impact'] = missed_calls['delta_home_win_exp'].abs()
    game_impact = missed_calls.groupby('game_pk')['win_exp_impact'].sum().reset_index()
    game_impact.rename(columns={'win_exp_impact': 'total_missed_call_impact'}, inplace=True)
    return game_impact

# Find top N games most impacted by missed calls
def find_most_impacted_games(game_impact_df, top_n=10):
    return game_impact_df.sort_values(by='total_missed_call_impact', ascending=False).head(top_n)


if __name__ == "__main__":
    csv_path = "pitch_data_2025-03-27_to_2025-07-27.csv"

    pitch_data = load_data(csv_path)
    labeled_data = identify_missed_calls(pitch_data, method='zone')
    impact_summary = analyze_call_impact(labeled_data)
    top_games = find_most_impacted_games(impact_summary)

    print(top_games)
