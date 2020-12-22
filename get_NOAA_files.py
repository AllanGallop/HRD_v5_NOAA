import wget, requests, json, pandas as pd
from shutil import copyfile

## Pads out strings to correct lengths
def padValue(value,width):
    return '{value: >{width}}'.format(value=str(value), width=width)


## Get the 30-Day Solar Data
content = wget.download("ftp://ftp.swpc.noaa.gov/pub/indices/DSD.txt",out="output/Last30DaysDailySolarData.txt")


## Fetch the Recent Solar Indices
content = requests.get("https://services.swpc.noaa.gov/json/solar-cycle/observed-solar-cycle-indices.json")
js = json.loads(content.content)
df = pd.DataFrame(js, columns= ['time-tag', 'ssn','smoothed_ssn','observed_swpc_ssn','smoothed_swpc_ssn','f10.7','smoothed_f10.7'])
df = df.join(pd.DataFrame(df.pop('time-tag').str.split('-').tolist(),index=df.index, columns=['year','month']),how="left")
df['ratio'] = 0
df['ap'] = 0
df = df.reindex(columns=['year', 'month','ssn','ssn','ratio','smoothed_ssn','observed_swpc_ssn','smoothed_swpc_ssn','f10.7','smoothed_f10.7','ap','ap'])
outfile = open("output/RecentSolarIndices.txt","w+")

for row in df.values.tolist():
    outfile.write( padValue(row[0],4) + padValue(row[1],3) + padValue(row[2],8) + padValue(row[3],8) + padValue(row[4],6) + padValue(row[5],8) + padValue(row[6],6) + padValue(row[7],9) + padValue(row[8],9) + padValue(row[9],10) + padValue(row[10],9) +'\n')

outfile.close()

## Clear out the last request, response and file
del content
del js
del outfile


## Fetch the Predicted Sunspots
content = requests.get("https://services.swpc.noaa.gov/json/solar-cycle/predicted-solar-cycle.json")
js = json.loads(content.content)
df = pd.DataFrame(js, columns= ['time-tag', 'predicted_ssn','high_ssn','low_ssn','predicted_f10.7','high_f10.7','low_f10.7'])
df = df.join(pd.DataFrame(df.pop('time-tag').str.split('-').tolist(),index=df.index, columns=['year','month']),how="left")
df = df.reindex(columns=['year', 'month', 'predicted_ssn','high_ssn','low_ssn','predicted_f10.7','high_f10.7','low_f10.7'])
outfile = open("output/SunspotPredictDefault.txt","w+")

for row in df.values.tolist():
    outfile.write( padValue(row[0],4) + padValue(row[1],3) + padValue(row[2],12) + padValue(row[3],8) + padValue(row[4],8) + padValue(row[5],11) + padValue(row[6],8) + padValue(row[7],8) +'\n')

outfile.close()

## Copy the default to high and low
copyfile("output/SunspotPredictDefault.txt","output/SunspotPredictHigh.txt")
copyfile("output/SunspotPredictDefault.txt","output/SunspotPredictLow.txt")