import pandas as pd
import datetime

forgotMealsDf = pd.read_excel(io="data/ADMU Extract - 11420.ods", sheet_name="Forgot Meal - Portions", engine="odf")
summariesDf = pd.read_excel(io="data/ADMU Extract - 11420.ods", sheet_name="Summaries", engine="odf")
fnddsDf = pd.read_excel(io="data/ADMU Extract - 11420.ods", sheet_name="FnddsGlance", engine="odf")

ids = forgotMealsDf['ForgotMealID']
filt1 = summariesDf['EventID'].isin(ids)
anaSummariesDf = summariesDf[filt1]
filt2 = summariesDf['EventID'].isin(["TrainingMeal"])
anaSummariesDf = anaSummariesDf[~filt2]

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

