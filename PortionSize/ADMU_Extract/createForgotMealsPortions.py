import pandas as pd
import ast

ForgotMealsDF = pd.read_excel('../data/raw_extract/ForgotMeal Event.xlsx')
forgotMealPortionsDf = pd.DataFrame(columns=['AboutSubjectID', 'ID', 'MealDescription', 'MealWhatMeal', 'DateAsString'])
cols = ForgotMealsDF.columns
for x, meal in enumerate(ForgotMealsDF['Portions']):
    foodDict = ast.literal_eval(ForgotMealsDF.iloc[x]['Portions'])
    for food in foodDict:
        tempDf = pd.json_normalize(food)
        for col in cols:
            tempDf[col] = ForgotMealsDF.iloc[x][col]
        forgotMealPortionsDf = forgotMealPortionsDf.append(tempDf)

forgotMealPortionsDf.to_excel('../data/raw_extract/furtherExtracted/ForgotMeal Event-Portions.xlsx')
