# lab.py
#chatgpt is used to generate some test cases to test out all the function 

from pathlib import Path
import io
import pandas as pd
import numpy as np


# ---------------------------------------------------------------------
# QUESTION 0
# ---------------------------------------------------------------------


def consecutive_ints(ints):
    if len(ints) == 0:
        return False
    
    for i in range(len(ints) - 1):
        if abs(ints[i] - ints[i + 1]) == 1:
            return True
        
    return False


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def median_vs_mean(nums):
    #return True if median is less than or equal to mean
    nums.sort() #chatgpt is used to learn .sort() function
 
    median = 0
    if len(nums) % 2 == 0:
        #median is mean of the middle two element
        median = (nums[len(nums) // 2 - 1] + nums[len(nums) // 2]) / 2
    else:
        #median is the middle element of the array
        median = nums[len(nums) // 2]

    mean = 0
    for i in range(len(nums)):
        mean = mean + nums[i]

    mean = mean / len(nums)

    if median <= mean:
        return True
    else:
        return False

# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def same_diff_ints(ints):
    #return true if the elements' value difference is similar to the indexes difference 
    if (len(ints) == 0): return False

    for i in range(len(ints)):
        for j in range(len(ints)):
            if i == j: continue
            if abs(i - j) == abs(ints[i] - ints[j]):
                return True
            
    return False


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def n_prefixes(s, n):
    str = ''
    for i in reversed(range(n + 1)):
        j = 0
        while j < i:
            str += s[j]
            j += 1

    return str



# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------

# chatgpt and python educational website is used to lead more about numpy.floor() and .zfill()
def exploded_numbers(ints, n):
    width = int(np.floor(np.log10(max(ints) + n) + 1)) 
    str_list  = []

    for i in range(len(ints)):
        exploded_str = ""
        for j in reversed(range(n + 1)):
            string = str(ints[i] - j).zfill(width) + ' '
            exploded_str += string
        
        for k in range(1, n + 1):
            string = str(ints [i] + k).zfill(width) 
            if (k != n):
                string += ' '
            exploded_str += string

        str_list.append(exploded_str)

    return str_list



# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def add_root(A):

    # create squaroot value array to be added to array A
    sqrt_array = np.arange(0, len(A), 1)
    sqrt_array = np.sqrt(sqrt_array)

    # print(A + sqrt_array)
    return (A + sqrt_array)



def where_square(A):
    sqrt_A = np.sqrt(A)

    # print(sqrt_A == np.floor(sqrt_A))
    return (sqrt_A == np.floor(sqrt_A))



# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def growth_rates(A):
    initial_price = A[0]

    growth_rate_list = (A - initial_price) / initial_price

    # print(np.round(growth_rate_list, 2))
    return np.round(growth_rate_list, 2)

def with_leftover(A):
    available_cash = np.full(len(A), 20)
    leftover_cash = available_cash % A #find the daily cash leftover after buying as many stock as possible  
    cummalative_leftover_cash = np.cumsum(leftover_cash) #find the cumalative cash from the leftover
    purchase_with_leftover = cummalative_leftover_cash / A

    if max(purchase_with_leftover) >= 1:
        # print(np.argmax(purchase_with_leftover >= 1))
        return np.argmax(purchase_with_leftover >= 1)
    else:
        return -1



# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def salary_stats(salary):
    num_players = salary["Player"].shape[0]
    num_teams = salary["Team"].nunique() #chatgpt is used to learn about .nunique() function
    total_salary = salary["Salary"].sum()

    highest_salary_series = salary.nlargest(1, "Salary")
    highest_salary = highest_salary_series["Player"].iloc[0]

    avg_los = salary.loc[salary["Team"] == "Los Angeles Lakers", "Salary"].mean().round(2)

    fifth_low = salary.nsmallest(5, "Salary").iloc[-1]
    fifth_lowest = fifth_low["Player"] + ', ' + fifth_low["Team"]

    players = salary["Player"]
    player_lastname = players.str.split().apply(lambda x: x[1]) #chatgpt is used to learn about .split and .apply(lambdax: x[1]) function
    duplicates = player_lastname.duplicated().any() #chatgpt is used to learn about .duplicated function

    highest_salary_player = salary .nlargest(1, "Salary") 
    highest_salary_team = highest_salary_player["Team"].iloc[0]
    highest_salary
    total_highest = salary.loc[salary["Team"] == highest_salary_team, "Salary"].sum()

    series = pd.Series([num_players, num_teams, total_salary, highest_salary, avg_los, fifth_lowest, duplicates, total_highest], index = ["num_players", "num_teams", "total_salary", "highest_salary", "avg_los", "fifth_lowest", "duplicates", "total_highest"])
    # print (series)
    return series



    


