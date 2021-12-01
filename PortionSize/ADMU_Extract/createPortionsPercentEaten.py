import pandas as pd
import ast

afterPhotosTheLeftOvers = pd.read_excel('../data/raw_extract/furtherExtracted/AfterPhotoLeftovers Event-TheLeftovers.xlsx')
FoodPhotoEventDF = pd.read_excel('../data/raw_extract/Food-Photo Event.xlsx')

afterPhotosTheLeftOvers['FoodID'] = afterPhotosTheLeftOvers['Food'].map(str) + \
                                    '_' + afterPhotosTheLeftOvers['AboutSubjectID'].map(str) + \
                                    '_' + afterPhotosTheLeftOvers['ID'].map(str)
afterPhotosTheLeftOvers['FoodID1'] = afterPhotosTheLeftOvers['FoodID']
afterPhotosTheLeftOvers.set_index('FoodID1', inplace=True)

foodPhotoPortsionDf = pd.DataFrame()
cols = FoodPhotoEventDF.columns
hasLeftovers = afterPhotosTheLeftOvers['FoodID']
for x, meal in enumerate(FoodPhotoEventDF['Portions']):
    foodDict = ast.literal_eval(FoodPhotoEventDF.iloc[x]['Portions'])
    for food in foodDict:
        tempDf = pd.json_normalize(food)
        for col in cols:
            tempDf[col] = FoodPhotoEventDF.iloc[x][col]
        tempDf['FoodID'] = tempDf['Food'].map(str) + \
                           '_' + tempDf['AboutSubjectID'].map(str) + \
                           '_' + tempDf['ID'].map(str)
        if tempDf['FoodID'].isin(afterPhotosTheLeftOvers['FoodID'])[0]:
            try:
                tempDf['PercentEaten'] = afterPhotosTheLeftOvers.loc[tempDf['FoodID']]['PercentEaten'].values[0]
            except ValueError:
                tempDf['PercentEaten'] = 'Duplicate'
        else:
            tempDf['PercentEaten'] = 1.00
        print(tempDf['PercentEaten'])
        foodPhotoPortsionDf = foodPhotoPortsionDf.append(tempDf)

foodPhotoPortsionDf.to_excel('../data/raw_extract/furtherExtracted/FoodPhoto Event-PortionsPercentEaten.xlsx')
