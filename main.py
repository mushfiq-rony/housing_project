# Md Mushfiqur Rahman
# Purpose: Read in 3 csv files with sample data, clean the data, push cleaned data to sql database table


import pandas as pd
# import from other python files
from files import *
from functions import *
# import mysql info
import pymysql.cursors
from creds import *

# import files
print("Beginning import")
# use pandas to read files
housing = pd.read_csv(housingFile)
income = pd.read_csv(incomeFile)
zip = pd.read_csv(zipFile)

# FILE 1 - HOUSING FILE DATA
print("Cleaning Housing File data")

# guid column - clean by deleting rows with corrupt data
regex = "^[A-Z]{4}$"
corrupt1 = housing['guid'].str.contains(regex)
# ~ implies keep all rows except those with corrupt data
housing = housing[~corrupt1]

# remaining columns - clean by replacing corrupt data with random numbers in specified ranges
cleanRandom(housing, 'housing_median_age', 10, 51)
cleanRandom(housing, 'total_rooms', 1000, 2001)
cleanRandom(housing, 'total_bedrooms', 1000, 2001)
cleanRandom(housing, 'population', 5000, 10001)
cleanRandom(housing, 'households', 500, 2501)
cleanRandom(housing, 'median_house_value', 100001, 250001)

print(f"{len(housing)} records imported into the database")


#################################################################
# FILE 2 - INCOME FILE DATA
print("Cleaning Income File data")

# guid column - clean by deleting rows with corrupt data
corrupt2 = income['guid'].str.contains(regex)
income = income[~corrupt2]

# median_income column - clean by replacing corrupt data with random numbers in specified range
cleanRandom(income, 'median_income', 100000, 750001)

print(f"{len(income)} records imported into the database")


###################################################################
# FILE 3 - ZIP FILE DATA
print("Cleaning ZIP File data")

# guid column - clean by deleting rows with corrupt data
corrupt3 = zip['guid'].str.contains(regex)
zip = zip[~corrupt3]

# zip_code column - clean by replacing with 1st number of same city state zip + 0000
corruptData = re.compile("^[A-Z]{4}$")
# create empty list & dictionary
badZips = []
goodZips = dict()
# look through each row for corrupt data
for index, row in zip.iterrows():
    if corruptData.match(row['zip_code']):
        # if zipcode matches regex, add indices to list
        badZips.append(index)
    else:
        # add all the good zipcodes to the dictionary
        goodZips[f"{row.city}{row.state}"] = f"{row.zip_code[0]}0000"

# for each index with corrupt data
for index in badZips:
    # get the city and state from this record
    city = zip.iloc[index]['city']
    state = zip.iloc[index]['state']
    # combine city & state so we can use them to search our dictionary
    cityStateKey = f"{city}{state}"
    # new zip codes for each corrupt zip
    newZipCode = goodZips[cityStateKey]
    # replace each corrupt zipcode with a new clean zipcode
    zip.loc[index, 'zip_code'] = newZipCode

# replace zip_code column for all files
housing['zip_code'] = zip['zip_code'].values
income['zip_code'] = zip['zip_code'].values

print(f"{len(zip)} records imported into the database")

# merge 3 files so we can import one database into sql
# outer merge since we want all columns with none repeating
merge_housing_income = pd.merge(housing, income, how='outer')
merged_all = pd.merge(merge_housing_income, zip, how='outer')

#merged_all.to_csv('output.csv', index=False)
######################################################################
# IMPORT FILE RECORDS INTO SQL DATABASE
try:
    myConnection = pymysql.connect(host=hostname,
                                   user=username,
                                   password=password,
                                   db=database,
                                   charset='utf8mb4',
                                   cursorclass=pymysql.cursors.DictCursor)

except Exception as e:
    print(f"An error has occurred.  Exiting: {e}")
    print()
    exit()

try:
    with myConnection.cursor() as cursor:

        # our sql statement using placeholders for each column of data
        sqlInsert = """
                insert
                into
                housing(guid, zip_code, city, state, county, median_age, total_rooms,
                        total_bedrooms, population, households, median_income, median_house_value)
                values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """
        # insert values for each row into each column
        for index, row in merged_all.iterrows():
            cursor.execute(sqlInsert, (f"{row.guid}", f"{row.zip_code}",
                                        f"{row.city}", f"{row.state}", f"{row.county}",
                                        f"{row.housing_median_age}", f"{row.total_rooms}",
                                        f"{row.total_bedrooms}", f"{row.population}",
                                        f"{row.households}", f"{row.median_income}",
                                        f"{row.median_house_value}"))

        # commit the file to the database
        myConnection.commit()

# if there is an exception, show what that is
except Exception as e:
    print(f"An error has occurred.  Exiting: {e}")
    print()

print(f"Import Completed")
print(f"\nBeginning validation\n")

try:
    with myConnection.cursor() as cursor:
        totalRooms = input("Total Rooms: ")
        # our roomSql summation statement
        roomSql = """select
                    sum(total_bedrooms) as bedrooms 
                    from 
                    housing
                    where
                    total_bedrooms > %s 
                    """
        # user input is value for roomSql
        cursor.execute(roomSql, f"{totalRooms}")
        # get the resulting sum from sql
        sumResult = cursor.fetchall()
        print(f"For locations with more than {totalRooms} rooms, "
              f"there are a total of {sumResult[0]['bedrooms']} bedrooms.")

        zipMedianIncome = input("\nZIP Code: ")
        # our incomeSql averaging statement
        incomeSql = """select
                    format(round(avg(median_income)),0) as zipCode
                    from 
                    housing
                    where
                    zip_code = %s 
                    """

        # user input is value for incomeSql
        cursor.execute(incomeSql, f"{zipMedianIncome}")
        # get the resulting avg of median income from sql
        incomeResult = cursor.fetchall()
        print(f"The median household income for ZIP code {zipMedianIncome} is {incomeResult[0]['zipCode']}.")

# if there is an exception, show what that is
except Exception as e:
    print(f"An error has occurred.  Exiting: {e}")
    print()
finally:
    myConnection.close()

print(f"\nProgram exiting.")

