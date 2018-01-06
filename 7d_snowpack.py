# coding: utf-8

# In[84]:

import glob, os
import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

path = r'/home/pi/weather/results/snowdepth'
all_files = glob.glob(os.path.join(path, "*.csv"))

days = mdates.DayLocator()   # every year
hours = mdates.HourLocator()  # every month
daysFmt = mdates.DateFormatter('%Y-%m-%d')

df_from_each_file = (pd.read_csv(f, header=None, infer_datetime_format=True,
                                 parse_dates={'Measurement Time':[0]}) for f in all_files)
df = pd.concat(df_from_each_file, ignore_index=True)
df['depth'] = (1635 - df[1])*(0.393700787401)/10

fig, ax = plt.subplots(figsize=(8,4), dpi=150)
ax.plot(df['Measurement Time'], df['depth'])
ax.xaxis.set_major_locator(days)
ax.xaxis.set_major_formatter(daysFmt)
ax.xaxis.set_minor_locator(hours)

now = datetime.now()
datemin = now-timedelta(days=7)
datemax = now
ax.set_xlim(datemin, datemax)
ax.set_ylim(0, 60)

ax.format_xdata = mdates.DateFormatter('%Y-%m-%d %H:%M:%S')
#ax.format_ydata = df['depth']
ax.grid(True)
fig.autofmt_xdate()

plt.title('7 day change in snowpack')
plt.ylabel('Inches of snowpack')
plt.savefig('/var/www/herman/hermanthebear/static/img/plots/snowdepth/depth7d.png')
