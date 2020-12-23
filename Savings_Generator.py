import numpy as np
import pandas as pd
import time   
from datetime import datetime
from datetime import date
import time    
import string
import xlsxwriter

# expense tracker - cc_stm 
def converter(x):
    if '$' in x:
        x = x.replace('$', '')
    if '(' in x:
        x = '-' + x.strip('()')
    return float(x) * -1.0

df = pd.read_csv(
    r'/Users/deannaweisel/Desktop/2020expenses.csv', 
    delimiter = ',', 
    converters = { 'Expenses': converter },
    parse_dates = ['Post Date']) #converts to dates

df['Month'] = df['Post Date'].dt.month
df['Year'] = df['Post Date'].dt.year

# defines pay period
""" def get_pp(post_date: datetime, close_day: int) -> string:
    if (post_date.day <= close_day):
        return f"{post_date.year}-{post_date.month}"
    elif (post_date.month == 12):
        return f"{post_date.year + 1}-{1}"
    else:
        return f"{post_date.year}-{post_date.month + 1}" """

def get_close(post_date: datetime, close_day: int) -> datetime:
    if (post_date.day <= close_day):
        return date(post_date.year, post_date.month, close_day)
    elif (post_date.month == 12):
        return date(post_date.year + 1, 1, close_day)
    else:
        return date(post_date.year, post_date.month + 1, close_day)

close = []

# defines close date of statement
for index, row in df.iterrows():
    close.append(get_close(row['Post Date'], 21))

df["Close"] = close

# defines current statement close 
today = date.today()
current_stm = get_close(today, 21) 
#print(current_stm) # 2020-12-21

# filter to exclude current period  of cc stm 
cc_stm = df[df["Close"] < current_stm]

# cc_stm sum of expenses by close date; cc_stm per period 
cc_due = (cc_stm.groupby("Close")['Expenses'].sum())
current_cc_due = cc_due.tail(1)[0]  # most cc stm total due amount

# define budget parameters of current month
salary = []
buffer = [] 
rent = []
student_loans = []
savingsacc_1 = []
savingsacc_2 = []

auto_savings = savingsacc_1 + savingsacc_2
expenses = rent + student_loans

def current_budget(begining_balance, salary, num_pp, cc_pd, remaining_cc_balance, monthly_exp, utlities, monthly_savings):
    
    budget = pd.Series() 

    # 0) Adding current balance
    budget = budget.append(pd.Series(begining_balance, index=["Beginning Balance"])) 

    # 1) Adding monthly salary 
    budget = budget.append(pd.Series([salary * num_pp], index=["Monthly Salary"])) 

    # 2) Adding remaining credit card
    cc_balance = 0
    if (not cc_pd): 
        cc_balance = remaining_cc_balance
    budget = budget.append(pd.Series(cc_balance, index=["CC Balance"]))

    # 3) monthly expenses  
    budget = budget.append(pd.Series(monthly_exp, index=["Monthly Expenses"]))  

    # 4) monthly expenses  
    budget = budget.append(pd.Series(utlities, index=["Utlities"]))

    # 5) automated savings amt
    budget = budget.append(pd.Series(monthly_savings, index=["Monthly Savings"])) 
    
    # 6) automated savings amt 
    budget = budget.append(pd.Series(buffer, index=["Buffer Amount"]))

    # 7) Sum list to get savings
    remaining_bal = budget[0] + budget[1] - budget[2] - budget[3] - budget[4] - budget[5] - budget[6]
    
    return budget.append((pd.Series(remaining_bal, index=["Saving Amount"])))

# Input
begining_balance = float(input("Current bank account balance? "))
num_pp = float(input("Number of reamining pay periods this month? "))
utlities = float(input("Amount for utlities? "))
cc_pd_inp = input("Prior cc stm paid? (Y/N) ")

# Input validations/transformations
if (cc_pd_inp.lower() == "n"):
    cc_pd = False
else:
    cc_pd = True

savings = current_budget(begining_balance, salary, num_pp, cc_pd, current_cc_due, expenses, utlities, auto_savings)
print(savings)

#writer = savings.to_excel(r'/Users/deannaweisel/Desktop/savings.xlsx', sheet_name='savings',index=True, index_label='Monthly Budget')
today_day = datetime.today().strftime('%Y-%m-%d')
today_month = datetime.today().strftime('%Y-%m')

workbook = xlsxwriter.Workbook('savings_tracker.xlsx')
worksheet = workbook.add_worksheet(today_month)

# Add a bold format to use to highlight cells.
bold = workbook.add_format({'bold': True})
negative = workbook.add_format({'num_format':  '-'})

worksheet.set_column('A:A', 30)
worksheet.set_column('B:B', 20)

amount_format = workbook.add_format({'num_format': '$#,##0.00'})

worksheet_date = workbook.add_format({'num_format': 'yyyy-m-d'})
worksheet.write('A13', today_day, worksheet_date)       # 28-2-2013

# write headers
worksheet.write('A1', 'Budget', bold)
worksheet.write('B1', 'Amount', bold)
# write  rows for Monthly Expenses 
worksheet.write('A2', 'Beginning Balance', bold)
worksheet.write('A3', 'Monthly Salary', bold)

worksheet.write('A4', 'CC Balance', bold)
worksheet.write('A5', 'Monthly Expenses', bold)
worksheet.write('A6', 'Utlitities', bold)
worksheet.write('A7', 'Monthly Savings', bold)
worksheet.write('A8', 'Buffer Amount', bold)

worksheet.write('A9', 'Saving Amount', bold)

row = 1 
col = 0 

for amount in (savings):
    #worksheet.write(row, col,     item)
    worksheet.write(row, col + 1, amount)
    worksheet.write(row, col + 1, amount, amount_format)
    
    row += 1

workbook.close()
