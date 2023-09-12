#%%
#line above allows a run cell in vscode to view different plots like notebook
import pandas as pd#
from datetime import datetime
import matplotlib.pyplot as plt
from sklearn.linear_model import Ridge
weather = pd.read_csv('london_weather.csv',index_col='date')
print(weather)
#reads and prints python file into terminal
null_pct = weather.apply(pd.isnull).sum()/weather.shape[0]
print(null_pct)
#Finding the amount of null(non existent) values in my data set

valid_columns = weather.columns[null_pct < .05]#
print(valid_columns)
#All columns with null percentage above 5% get kept

weather = weather[valid_columns].copy()
weather.columns = weather.columns.str.lower()
#reassign weather variable to valid columns only
#removing invalid and changing to lower case


print(weather.dtypes)# initially used to find and extract data types
print(weather.index)# not easy format to use


weather.index = pd.to_datetime(weather.index, format='%Y%m%d')
#changes to a suitable format
#print(weather.index.year) tested by viewing the year
count = weather.index.year.value_counts().sort_index()
print(count)#refers to number of days in each year

plt.plot(weather["max_temp"])
#plots the max temperature for the last 40 years
weather["target"] = weather.shift(-1)["max_temp"]
#create a new row called target temperature and set it as the following day
weather = weather.ffill()
#any NAN values get filled with nearest value to clean data
print(weather.corr()) #See if any values have correlation

rr = Ridge(alpha=.1)
predictors = weather.columns[~weather.columns.isin(
    ["global_radiation","sunshine","cloud_cover"])]
#Removing irrelevent data with least correlation
#Test a model on data we already have (backtest)
def backtest(weather,  predictors,model=rr, start=3650,step=90):
    all_predictions = []
    #function takes 5 arguments 3 preset
    for i in range(start, weather.shape[0],step):
        train = weather.iloc[:i,:] #all rows in our data up to row i
        test = weather.iloc[i:(i+step),:]# test on next 90 days
        
        model.fit(train[predictors], train["target"])
        
        preds = model.predict(test[predictors])
        
        #below this is nice to havs
        preds = pd.Series(preds, index=test.index)
        
        combined = pd.concat([test["target"],preds],axis=1)
        combined.columns = ["actual", "prediction"]
        combined["diff"]= (combined["prediction"]- combined["actual"]).abs()
        #find the difference of target data and model prediction
        
        all_predictions.append(combined)
    return pd.concat(all_predictions)

predictions = backtest(weather, predictors)
print(predictions)
#upto now is a successfull backtest on max temperature in london