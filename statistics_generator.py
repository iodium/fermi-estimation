import sqlite3

import pandas as pd

stats_data = {
    'question_id':  [],
    'min': [],
    'max': [],
    'hit': [],
    'width': [],
    'score': []
}

stats_df = pd.DataFrame(stats_data)

with sqlite3.connect('stats.db') as conn:
    stats_df.to_sql('submissions', con=conn, if_exists='replace', index=False)

print("Database created successfully!")
print(f"Created {len(stats_df)} submission records")