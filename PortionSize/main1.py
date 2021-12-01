import pandas as pd

df = pd.read_excel(io="ADMU Extract.xlsx", sheet_name="Summaries")
df['ID'] = df['SubjectID'] + '_' + df['Date']
ids = df['ID'].unique()
daySum = pd.DataFrame(columns=df.columns)
for id in ids:
    tempDf = df.where(cond=df["ID"] == id).dropna()
    maxTempDf = tempDf.where(cond=tempDf['Time'] == tempDf['Time'].max()).dropna()
    daySum = daySum.append(other=maxTempDf)

daySum.to_excel('Day Summary.xlsx')

df = pd.read_excel(io="ADMU Extract - WOFormulas.xlsx", sheet_name="Per Food")
ids = df['NewID'].unique()

sumCols = ['StdServingAddedSugar', 'StdServingAlcohol', 'StdServingDairy',
           'StdServingFruit', 'StdServingGrains', 'StdServingGramWt', 'StdServingKCals', 'StdServingProtein',
           'StdServingSatFat', 'StdServingVegetable', 'TemplateAddedSugar', 'TemplateAlcohol', 'TemplateDairy',
           'TemplateFruit', 'TemplateGrains', 'TemplateGramWt', 'TemplateKCals', 'TemplateProtein', 'TemplateSatFat',
           'TemplateVegetable']
noSumCols = ['Participant', 'Date', 'Time', 'DateAsString', 'Meal']
allCols = ['Participant', 'Date', 'Time', 'DateAsString', 'Meal', 'StdServingAddedSugar', 'StdServingAlcohol', 'StdServingDairy',
           'StdServingFruit', 'StdServingGrains', 'StdServingGramWt', 'StdServingKCals', 'StdServingProtein',
           'StdServingSatFat', 'StdServingVegetable', 'TemplateAddedSugar', 'TemplateAlcohol', 'TemplateDairy',
           'TemplateFruit', 'TemplateGrains', 'TemplateGramWt', 'TemplateKCals', 'TemplateProtein', 'TemplateSatFat',
           'TemplateVegetable']
mealSumDf = pd.DataFrame(columns=allCols)
for id in ids:
    tempDf = df.where(cond=df["NewID"] == id).dropna()
    infoDf = tempDf[noSumCols].iloc[0]
    singleMealSummedDf = infoDf.append(tempDf[sumCols].sum())
    mealSumDf = mealSumDf.append(other=singleMealSummedDf, ignore_index=True)

mealSumDf.to_excel('Per Meal.xlsx')
