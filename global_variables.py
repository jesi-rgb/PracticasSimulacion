import pandas as pd

# modomuerte, speed, riskaversion, deathtime
rabbit_df = pd.DataFrame(columns=['Death_cause', 'Speed', 'Risk Aversion', 'Age'])
lynx_df = pd.DataFrame(columns=['Death_cause', 'Speed', 'Risk Aversion', 'Age'])

rabbit_dict = dict()
rabbit_cont = 0
rabbit_id = 1

lynx_dict = dict()
lynx_cont = 0
lynx_id = 1

speed_mean = 0
risk_mean = 0

