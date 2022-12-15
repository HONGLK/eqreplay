import json
from datetime import datetime
import sys
sys.path.insert(0, '.\\Source\\')
from EQ_Animation import Animation

a = Animation(['C:\\Git\\eqreplay\\Data\\2022_10_31\\CWB-EEW111029301.txt', 'C:\\Git\\eqreplay\\Data\\2022_10_31\\Trans_16_48_36.520_Site.json', 'C:\\Git\\eqreplay\\Data\\2022_10_31\\Trans_16_48_47.924_Alarm.json'])

a.draw()
print(a.root_path)