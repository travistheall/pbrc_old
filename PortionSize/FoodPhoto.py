import pandas as pd
import datetime
photoMealsDf = pd.read_excel(io="data/ODS/ADMU Extract - 11420.ods", sheet_name="Food Photo - Portions", engine="odf")
fnddsDf = pd.read_excel(io="data/ODS/ADMU Extract - 11420.ods", sheet_name="FnddsGlance", engine="odf")

filt1 = photoMealsDf['Meal'].isin(["LabMeal", "TrainingMeal"])
anaPhotoMealsDf = photoMealsDf[~filt1]

participantInfoDf = anaPhotoMealsDf[anaPhotoMealsDf.columns[:19]].drop(columns=['PercentEaten'])
percentConsumed = anaPhotoMealsDf['PercentEaten'].transpose()
photoMealsDfColumnsToAnalyzeDf = anaPhotoMealsDf[anaPhotoMealsDf.columns[19:]]
photoMealsDfResult = photoMealsDfColumnsToAnalyzeDf.mul(percentConsumed, axis=0)
anaPhotoMealsDf = pd.concat([participantInfoDf, photoMealsDfResult], axis=1)

filt2 = fnddsDf['Food code'].isin(anaPhotoMealsDf['FoodCode'])
foodsConsumedDf = fnddsDf[filt2].drop_duplicates()
foodsConsumedDf = foodsConsumedDf.set_index(['Food code'])

hundredGramsDf = foodsConsumedDf.loc[anaPhotoMealsDf['FoodCode']]
anaHundredGramsDf = hundredGramsDf[hundredGramsDf.columns[3:]]
oneGramDf = anaPhotoMealsDf['TemplateGramWt'].div(100)
fnddsVals = anaHundredGramsDf.mul(oneGramDf.values, axis=0)
final = pd.concat([anaPhotoMealsDf.reset_index(), fnddsVals.reset_index()], axis=1)

date = datetime.date.today()
filename = f'FoodPhotoData-{date}.xlsx'
final.to_excel(filename)
