import pandas as pd
import scipy.stats as stats

train = pd.read_csv("train.csv")

train['MSSubClass'].value_counts(dropna=False)

catvars1 = [
    'MSSubClass', 'MSZoning', 'Street', 'Alley', 'LotShape', 'LandContour',
    'Utilities', 'LotConfig', 'LandSlope', 'Neighborhood', 'Condition1',
    'Condition2', 'BldgType', 'HouseStyle', 'RoofMatl', 'Exterior1st',
    'Exterior2nd', 'MasVnrType', 'Foundation', 'Heating', 'HeatingQC',
    'CentralAir', 'Electrical', 'Functional', 'GarageType', 'GarageFinish',
    'PavedDrive', 'MiscFeature', 'MoSold', 'SaleType', 'SaleCondition'
]

# Continuous variable with such a low number of levels that it is practically categorical
contlowoptions = [
    'BsmtFullBath', 'BsmtHalfBath', 'FullBath', 'HalfBath', 'KitchenAbvGr',
    'Fireplaces', 'YrSold'
]

# Variables on a Likert-like scale
scalevars = [
    'ExterQual', 'ExterCond', 'BsmtQual', 'BsmtCond', 'BsmtExposure',
    'BsmtFinType1', 'BsmtFinType2', 'KitchenQual', 'FireplaceQu', 'GarageCars',
    'GarageQual', 'GarageCond', 'PoolQC', 'Fence'
]

contvars1 = [
    'LotFrontage', 'LotArea', 'OverallQual', 'OverallCond', 'YearBuilt',
    'YearRemodAdd', 'MasVnrArea', 'BsmtFinSF1', 'BsmtFinSF2', 'BsmtUnfSF',
    'TotalBsmtSF', '1stFlrSF', '2ndFlrSF', 'LowQualFinSF', 'GrLivArea',
    'BedroomAbvGr', 'TotRmsAbvGrd', 'GarageYrBlt', 'GarageArea', 'WoodDeckSF',
    'OpenPorchSF', 'EnclosedPorch', '3SsnPorch', 'ScreenPorch', 'PoolArea',
    'MiscVal'
]

for var in train.columns:
    if train[var].isnull().sum() > 0:
            print var + ": " + str(train[var].isnull().sum())

for var in contvars1:
    if train[var].isnull().sum() > 0:
            print var + ": " + str(train[var].isnull().sum())

for var in contlowoptions:
    print train[var].value_counts(dropna=False)

# Data Cleaning
def impute_continuous(data, vars):
    for col in vars:
        data[col] = data[col].fillna(data[col].median())

def impute_categorical(data, vars):
    for col in vars:
        data[col] = data[col].fillna(data[col].value_counts().index[0])

def categorical_to_binary(data, vars):
    for col in vars:
        dummies = pd.get_dummies(data[col])
        corrs = [abs(stats.pearsonr(dummies[col2], train['SalePrice'])[0]) for col2 in dummies]
        excl_col = dummies.columns[corrs.index(min(corrs))]
        dum_col = [col2 for col2 in dummies.columns if col2 != excl_col]
        data = data.join(dummies[dum_col])
        return data

train['seq_month'] = (train['YrSold'] - 2006) * 12 + train['MoSold']
