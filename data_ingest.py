from pybaseball import statcast
import pandas as pd

df = statcast(start_dt='2025-03-27', end_dt='2025-07-27')

columns = [
    'game_pk', 'game_date', 'home_team', 'away_team',
    'type', 'zone', 'plate_x', 'plate_z', 'sz_top', 'sz_bot',
    'delta_home_win_exp', 'inning', 'inning_topbot'
]

filtered_df = df[columns]

# View basic info
print(filtered_df.shape)
print(filtered_df.head())

# Export
filtered_df.to_csv('pitch_data_2025-03-27_to_2025-07-27.csv', index=False)