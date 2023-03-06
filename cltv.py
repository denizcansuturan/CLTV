############################################
# CUSTOMER LIFETIME VALUE
############################################

# 1. Data preparation
# 2. Average Order Value (average_order_value = total_price / total_transaction)
# 3. Purchase Frequency (total_transaction / total_number_of_customers)
# 4. Repeat Rate & Churn Rate (birden fazla alışveriş yapan müşteri sayısı / tüm müşteriler)
# 5. Profit Margin (profit_margin =  total_price * 0.10)
# 6. Customer Value (customer_value = average_order_value * purchase_frequency)
# 7. Customer Lifetime Value (CLTV = (customer_value / churn_rate) x profit_margin)
# 8. Segmentation
# 9. Functionalization

##################################################
# 1. Data Preparation
##################################################

# Business Problem
# https://archive.ics.uci.edu/ml/datasets/Online+Retail+II

# An e-commerce company divides its customers into segments and
# wants to define marketing strategies according to these segments.

# Dataset includes the sales of a UK based online store
# from 01/12/2009 to 09/12/2011.


import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

df_ = pd.read_excel("D:/MIUUL/CRM/crmAnalytics/rfm/online_retail_II.xlsx", sheet_name="Year 2010-2011")
df = df_.copy()
# if something goes wrong we do not need to read the data again
# working on the copy right now.

df.shape

df.head()

df.isnull().sum()
# null values are checked and missing customer ids are dropped
# since without knowing the customer, we do not know whose CLTV that we are calculating is

df = df[~df["Invoice"].str.contains("C", na=False)]
# in dataset story it is mentioned that invoices starting with C are cancelled ones
# no need for them to stay
# ~ means everything except this:

df.describe().T
# to check if there is something out of the ordinary
# after adjustments, it must be run to control again

df = df[(df['Quantity'] > 0)]
# negative values for quantity found in describe, they should be eliminated
# since there can not be negative quantity of a product

df.dropna(inplace=True)
# to eliminate missing customer ids info and missing description info

df["TotalPrice"] = df["Quantity"] * df["Price"]
# same products is ordered multiple times in the same invoice
# TotalPrice is needed for a product type
df.head()

cltv_c = df.groupby('Customer ID').agg({'Invoice': lambda x: x.nunique(),
                                        'Quantity': lambda x: x.sum(),
                                        'TotalPrice': lambda x: x.sum()})

# analysis is customer based so dataset is groupby the id,
# necessary columns (metrics for cltv )are calculated
# and saved as a new dataframe cltv_c

cltv_c.columns = ['total_transaction', 'total_unit', 'total_price']
# columns are renamed

cltv_c.head()

##################################################
# 2. Average Order Value (average_order_value = total_price / total_transaction)
##################################################

cltv_c.head()
cltv_c["average_order_value"] = cltv_c["total_price"] / cltv_c["total_transaction"]
# necessary columns exist, easily calculated and added as a new column

##################################################
# 3. Purchase Frequency (total_transaction / total_number_of_customers)
##################################################

cltv_c.head()
cltv_c.shape[0]
# shape function returns a tuple with row and column number of a dataframe
# by indexing we obtained the raw number of the cltv_c dataframe
# which is the exactly the total number of customers

cltv_c["purchase_frequency"] = cltv_c["total_transaction"] / cltv_c.shape[0]
# purchase frequency calculated and added

##################################################
# 4. Churn Rate & Repeat Rate (Number of customers who made a purchase more than once / Total Number of Customers)
##################################################

repeat_rate = cltv_c[cltv_c["total_transaction"] > 1].shape[0] / cltv_c.shape[0]
# same idea, just a condition added in cltv_c and again row number is taken
# as number of customers
# total_transaction is the number of unique invoices
# retention rate, customers we consider ourselves.

churn_rate = 1 - repeat_rate
# by definiton, if a customer did not order more than once
# it is accepted that it is a customer churn

##################################################
# 5. Profit Margin (profit_margin =  total_price * 0.10)
##################################################

cltv_c['profit_margin'] = cltv_c['total_price'] * 0.10
# 0.10 is a constant that is needed to be calculated by the company
# profit_margin is added, it is profit after all the expenses

##################################################
# 6. Customer Value (customer_value = average_order_value * purchase_frequency)
##################################################

cltv_c['customer_value'] = cltv_c['average_order_value'] * cltv_c["purchase_frequency"]
# these customer values are needed to be corrected by churn rate and profit margin

##################################################
# 7. Customer Lifetime Value (CLTV = (customer_value / churn_rate) x profit_margin)
##################################################

cltv_c["cltv"] = (cltv_c["customer_value"] / churn_rate) * cltv_c["profit_margin"]
# while churn_rate is a constant, profit margin is customer-based

cltv_c.sort_values(by="cltv", ascending=False).head()
# customers are sorted according to their final lifetime values

##################################################
# 8. Creating segments
##################################################

cltv_c.sort_values(by="cltv", ascending=False).tail()
# to observe the worst cases

cltv_c["segment"] = pd.qcut(cltv_c["cltv"], 4, labels=["D", "C", "B", "A"])
# it is decided to create 4 groups namely A, B, C, D
# new column segment is added
# qcut function from pandas groups a column given the number of groups and labels
# however, by default, qcut sorts the values ascending
# since the bigger the CLTV, the better; labels have to be written backwards

cltv_c.sort_values(by="cltv", ascending=False).head()
# expected to have A segment on the head

cltv_c.sort_values(by="cltv", ascending=False).tail()
# expected to have D segment on the tail

cltv_c.groupby("segment").agg({"count", "mean", "sum"})
# to analyze the segments on the basis of all variables
# for example, A segment customers made 10.4 transaction on average

cltv_c.to_csv("cltc_c.csv")
# csv file is created

##################################################
# Functionalization
##################################################

def create_cltv_c(dataframe, profit=0.10):

    # Data preparation
    dataframe = dataframe[~dataframe["Invoice"].str.contains("C", na=False)]
    dataframe = dataframe[(dataframe['Quantity'] > 0)]
    dataframe.dropna(inplace=True)
    dataframe["TotalPrice"] = dataframe["Quantity"] * dataframe["Price"]
    cltv_c = dataframe.groupby('Customer ID').agg({'Invoice': lambda x: x.nunique(),
                                                   'Quantity': lambda x: x.sum(),
                                                   'TotalPrice': lambda x: x.sum()})
    cltv_c.columns = ['total_transaction', 'total_unit', 'total_price']
    # avg_order_value
    cltv_c['avg_order_value'] = cltv_c['total_price'] / cltv_c['total_transaction']
    # purchase_frequency
    cltv_c["purchase_frequency"] = cltv_c['total_transaction'] / cltv_c.shape[0]
    # repeat rate & churn rate
    repeat_rate = cltv_c[cltv_c.total_transaction > 1].shape[0] / cltv_c.shape[0]
    churn_rate = 1 - repeat_rate
    # profit_margin
    cltv_c['profit_margin'] = cltv_c['total_price'] * profit
    # Customer Value
    cltv_c['customer_value'] = (cltv_c['avg_order_value'] * cltv_c["purchase_frequency"])
    # Customer Lifetime Value
    cltv_c['cltv'] = (cltv_c['customer_value'] / churn_rate) * cltv_c['profit_margin']
    # Segment
    cltv_c["segment"] = pd.qcut(cltv_c["cltv"], 4, labels=["D", "C", "B", "A"])

    return cltv_c

# Whole process is defined in a function so that we can perform all the
# above on the year 2009–2010 too within seconds.
# Profit is defined by the company, so an option is added to
# control the profit value.

df2_ = pd.read_excel("D:/MIUUL/CRM/crmAnalytics/rfm/online_retail_II.xlsx", sheet_name="Year 2009-2010")
df2 = df2_.copy()

clv = create_cltv_c(df2)

























