
### Import Statements

import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from pathlib import Path

data_file = Path(__file__).with_name('June-2021-Provo-River-Streamflow-Rates (1).csv')
array2 = np.genfromtxt(data_file, delimiter=',', dtype=str, skip_header=1)
x=array2[:,0]
y_1=array2[:,1].astype(float)
y_2=array2[:,2].astype(float)
y_3=array2[:,3].astype(float)
y_4=array2[:,4].astype(float)
y_5=array2[:,5].astype(float)
array2

x_dates = [datetime.strptime(date, '%Y-%m-%d %H:%M:%S') for date in x]

plt.plot(x_dates, y_1, color='red', label='Site 10163000')
plt.plot(x_dates, y_2, color='blue', label='Site 10155200')
plt.plot(x_dates, y_3, color='green', label='Site 10155500')
plt.plot(x_dates, y_4, color='orange', label='Site 10154200')
plt.plot(x_dates, y_5, color='purple', label='Site 10155000')
plt.xlabel('Date')
plt.ylabel('Flowrate (cfs)')
plt.title('Provo River Streamflow Data (2021)')

plt.gcf().autofmt_xdate()
plt.legend(title='Site Numbers')
plt.show()