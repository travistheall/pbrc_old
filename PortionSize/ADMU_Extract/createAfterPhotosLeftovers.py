import json
import pandas as pd

FoodPhotoEventDF = pd.read_excel('../data/raw_extract/Food-Photo Event.xlsx')
AfterPhotoEventLeftOversDF = pd.read_excel('../data/raw_extract/AfterPhotoLeftovers Event.xlsx')

afterPhotosTheLeftOvers = pd.DataFrame()

AfterPhotoEventLeftOversDF['PhotoCreationDate1'] = AfterPhotoEventLeftOversDF['PhotoCreationDate']
AfterPhotoEventLeftOversDF.set_index('PhotoCreationDate1')

FoodPhotoEventDF['PhotoCreationDate1'] = FoodPhotoEventDF['PhotoCreationDate']
FoodPhotoEventDF = FoodPhotoEventDF.set_index('PhotoCreationDate1')
cols = ['AboutSubjectID', 'ID', 'MealDescription', 'MealWhatMeal', 'PhotoCreationDate']

for x, meal in enumerate(AfterPhotoEventLeftOversDF['TheLeftovers']):
    foodDict = json.loads(AfterPhotoEventLeftOversDF.iloc[x]['TheLeftovers'].replace("'", '"'))
    for food in foodDict:
        tempDf = pd.json_normalize(food)
        for col in cols:
            tempDf[col] = FoodPhotoEventDF.loc[AfterPhotoEventLeftOversDF.iloc[x]['PhotoCreationDate']][col]
        afterPhotosTheLeftOvers = afterPhotosTheLeftOvers.append(tempDf)

afterPhotosTheLeftOvers.to_excel('../data/raw_extract/furtherExtracted/AfterPhotoLeftovers Event-TheLeftovers.xlsx')
