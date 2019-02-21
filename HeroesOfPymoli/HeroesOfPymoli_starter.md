
### Heroes Of Pymoli Data Analysis
* Of the 1163 active players, the vast majority are male (84%). There also exists, a smaller, but notable proportion of female players (14%).

* Our peak age demographic falls between 20-24 (44.8%) with secondary groups falling between 15-19 (18.60%) and 25-29 (13.4%).  
-----

### Note
* Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.


```python
# Dependencies and Setup
import pandas as pd
import numpy as np

# File to Load (Remember to Change These)
file_to_load = "Resources/purchase_data.csv"

# Read Purchasing File and store into Pandas data frame
purchase_data = pd.read_csv(file_to_load)
```

## Describe data


```python
purchase_data.describe()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Purchase ID</th>
      <th>Age</th>
      <th>Item ID</th>
      <th>Price</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>780.000000</td>
      <td>780.000000</td>
      <td>780.000000</td>
      <td>780.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>389.500000</td>
      <td>22.714103</td>
      <td>92.114103</td>
      <td>3.050987</td>
    </tr>
    <tr>
      <th>std</th>
      <td>225.310896</td>
      <td>6.659444</td>
      <td>52.775943</td>
      <td>1.169549</td>
    </tr>
    <tr>
      <th>min</th>
      <td>0.000000</td>
      <td>7.000000</td>
      <td>0.000000</td>
      <td>1.000000</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>194.750000</td>
      <td>20.000000</td>
      <td>48.000000</td>
      <td>1.980000</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>389.500000</td>
      <td>22.000000</td>
      <td>93.000000</td>
      <td>3.150000</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>584.250000</td>
      <td>25.000000</td>
      <td>139.000000</td>
      <td>4.080000</td>
    </tr>
    <tr>
      <th>max</th>
      <td>779.000000</td>
      <td>45.000000</td>
      <td>183.000000</td>
      <td>4.990000</td>
    </tr>
  </tbody>
</table>
</div>



## Player Count

* Display the total number of players



```python
nd_arr_names = purchase_data.SN.unique()

tot_players_count_dict = {'Total Players': len(nd_arr_names)}

total_unique_player_count = pd.DataFrame(tot_players_count_dict, index = tot_players_count_dict.keys())

total_unique_player_count
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Total Players</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Total Players</th>
      <td>576</td>
    </tr>
  </tbody>
</table>
</div>



## Purchasing Analysis (Total)

* Run basic calculations to obtain number of unique items, average price, etc.


* Create a summary data frame to hold the results


* Optional: give the displayed data cleaner formatting


* Display the summary data frame



```python
# Get Demographic data with SN and Product data with Item ID
demographic_data = purchase_data[['SN', 'Age', 'Gender']]
demographic_data = demographic_data.rename(columns={'SN': 'serial', 'Age': 'age', 'Gender': 'gender'})
demographic_data = demographic_data.drop_duplicates()
demographic_data.style.format({'price': '{:,.2f}'.format})
purchased_product_data = purchase_data[['Item ID', 'Item Name', 'Price']].copy()
purchased_product_data = purchased_product_data.rename(columns={'Item ID': 'item_id', 'Item Name': 'item_name', 'Price': 'price'})
purchased_product_data.set_index('item_id')
purchased_product_data = purchased_product_data.drop_duplicates()

summary = {'Number of Unique Items': [purchased_product_data.item_id.count()], 
           'Average Price': ['${:,.2f}'.format(purchased_product_data.price.mean())], 
           'Number of Puchases': [purchase_data.SN.count()], 
           'Total Revenue': ['${:,.2f}'.format(purchase_data.Price.sum())], 
           'Average Age of Customers': ['{:,.2f}'.format(demographic_data.age.mean())]}
summary = pd.DataFrame(summary, columns = summary.keys())

# import io
# str_io = io.StringIO()
# summary.to_html(buf=str_io, classes='table table-striped')
# html_str = str_io.getvalue()
# print(html_str)

summary
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Number of Unique Items</th>
      <th>Average Price</th>
      <th>Number of Puchases</th>
      <th>Total Revenue</th>
      <th>Average Age of Customers</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>183</td>
      <td>$3.04</td>
      <td>780</td>
      <td>$2,379.77</td>
      <td>22.74</td>
    </tr>
  </tbody>
</table>
</div>



## Gender Demographics

* Percentage and Count of Male Players


* Percentage and Count of Female Players


* Percentage and Count of Other / Non-Disclosed





```python
total_customer_count = demographic_data.serial.count()
male_customer_count = sum(demographic_data['gender'] == 'Male')
female_customer_count = sum(demographic_data['gender'] == 'Female')
oth_gen_customer_count = sum(demographic_data['gender'] == 'Other / Non-Disclosed')
demographic_summary = { 'Total Count': [male_customer_count, female_customer_count, oth_gen_customer_count], 
                        'Percentage of Players': ['{:,.2f}%'.format(100 * male_customer_count/total_customer_count), 
                                                  '{:,.2f}%'.format(100 * female_customer_count/total_customer_count), 
                                                  '{:,.2f}%'.format(100 * oth_gen_customer_count/total_customer_count)]
                       }
demographic_summary = pd.DataFrame(demographic_summary, 
                                   index = {'Male','Female','Other / Non-Disclosed'}, 
                                   columns = demographic_summary.keys())

demographic_summary
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Total Count</th>
      <th>Percentage of Players</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Male</th>
      <td>484</td>
      <td>84.03%</td>
    </tr>
    <tr>
      <th>Other / Non-Disclosed</th>
      <td>81</td>
      <td>14.06%</td>
    </tr>
    <tr>
      <th>Female</th>
      <td>11</td>
      <td>1.91%</td>
    </tr>
  </tbody>
</table>
</div>




## Purchasing Analysis (Gender)

* Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. by gender




* Create a summary data frame to hold the results


* Optional: give the displayed data cleaner formatting


* Display the summary data frame


```python
total_purchase_count = purchase_data['Purchase ID'].count()
male_purchase_count = sum(purchase_data['Gender'] == 'Male')
female_purchase_count = sum(purchase_data['Gender'] == 'Female')
oth_gen_purchase_count = sum(purchase_data['Gender'] == 'Other / Non-Disclosed')

male_purchase_data = purchase_data.loc[purchase_data['Gender'] == 'Male', 'Price']
female_purchase_data = purchase_data[purchase_data['Gender'] == 'Female']['Price']
oth_gen_str = 'Other / Non-Disclosed'
oth_gen_purchase_data = purchase_data.query('Gender==@oth_gen_str')['Price']

purchase_analysis_summary = {'Purchase Count': [male_purchase_count, 
                                                female_purchase_count, 
                                                oth_gen_purchase_count], 
                             'Average Purchase Price': ['${:,.2f}'.format(male_purchase_data.mean()), 
                                                        '${:,.2f}'.format(female_purchase_data.mean()), 
                                                        '${:,.2f}'.format(oth_gen_purchase_data.mean())], 
                             'Total Purchase Value': ['${:,.2f}'.format(male_purchase_data.sum()), 
                                                      '${:,.2f}'.format(female_purchase_data.sum()), 
                                                      '${:,.2f}'.format(oth_gen_purchase_data.sum())],
                             'Avg Total Purchase per Person': ['${:,.2f}'.format(male_purchase_data.sum()/len(purchase_data.loc[purchase_data['Gender'] == 'Male', 'SN'].unique())), 
                                                               '${:,.2f}'.format(female_purchase_data.sum()/len(purchase_data.loc[purchase_data['Gender'] == 'Female', 'SN'].unique())), 
                                                               '${:,.2f}'.format(oth_gen_purchase_data.sum()/len(purchase_data.loc[purchase_data['Gender'] == 'Other / Non-Disclosed', 'SN'].unique()))]    
                            }
purchase_analysis_summary_df = pd.DataFrame(purchase_analysis_summary, 
                                   index = ['Male','Female','Other / Non-Disclosed'], 
                                   columns = purchase_analysis_summary.keys())

purchase_analysis_summary_df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Purchase Count</th>
      <th>Average Purchase Price</th>
      <th>Total Purchase Value</th>
      <th>Avg Total Purchase per Person</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Male</th>
      <td>652</td>
      <td>$3.02</td>
      <td>$1,967.64</td>
      <td>$4.07</td>
    </tr>
    <tr>
      <th>Female</th>
      <td>113</td>
      <td>$3.20</td>
      <td>$361.94</td>
      <td>$4.47</td>
    </tr>
    <tr>
      <th>Other / Non-Disclosed</th>
      <td>15</td>
      <td>$3.35</td>
      <td>$50.19</td>
      <td>$4.56</td>
    </tr>
  </tbody>
</table>
</div>



## Age Demographics

* Establish bins for ages


* Categorize the existing players using the age bins. Hint: use pd.cut()


* Calculate the numbers and percentages by age group


* Create a summary data frame to hold the results


* Optional: round the percentage column to two decimal points


* Display Age Demographics Table



```python
bins = [0, 9, 14, 19, 24, 29, 34, 39, 100]
bin_names = ['<10', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40+']
age_wise_data = purchase_data.loc[purchase_data['Age']].copy()
age_wise_data['age_category'] = pd.cut(age_wise_data['Age'], bins, labels = bin_names)
age_wise_data = pd.DataFrame({'Percentage of Players' : age_wise_data.groupby(['age_category']).size()}).reset_index()
age_wise_data['Percentage of Players'] = age_wise_data['Percentage of Players'].apply(lambda x: '{:,.2f}%'.format(100 * x / len(purchase_data)))
age_wise_data
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>age_category</th>
      <th>Percentage of Players</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>&lt;10</td>
      <td>3.97%</td>
    </tr>
    <tr>
      <th>1</th>
      <td>10-14</td>
      <td>3.97%</td>
    </tr>
    <tr>
      <th>2</th>
      <td>15-19</td>
      <td>5.77%</td>
    </tr>
    <tr>
      <th>3</th>
      <td>20-24</td>
      <td>47.05%</td>
    </tr>
    <tr>
      <th>4</th>
      <td>25-29</td>
      <td>7.56%</td>
    </tr>
    <tr>
      <th>5</th>
      <td>30-34</td>
      <td>12.18%</td>
    </tr>
    <tr>
      <th>6</th>
      <td>35-39</td>
      <td>10.90%</td>
    </tr>
    <tr>
      <th>7</th>
      <td>40+</td>
      <td>8.59%</td>
    </tr>
  </tbody>
</table>
</div>



## Purchasing Analysis (Age)

* Bin the purchase_data data frame by age


* Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. in the table below


* Create a summary data frame to hold the results


* Optional: give the displayed data cleaner formatting


* Display the summary data frame


```python
bins = [0, 9, 14, 19, 24, 29, 34, 39, 100]
bin_names = ['<10', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40+']
age_wise_purchase_data = purchase_data[['Age', 'SN', 'Price']].copy()
age_wise_purchase_data['age_category'] = pd.cut(age_wise_purchase_data['Age'], bins, labels = bin_names)

age_count = pd.DataFrame(age_wise_purchase_data.groupby('age_category')['SN'].count())
tot_pur_price = pd.DataFrame(age_wise_purchase_data.groupby('age_category')['Price'].sum())
avg_pur_price = pd.DataFrame(age_wise_purchase_data.groupby('age_category')['Price'].mean())
uniq_cust_count = pd.DataFrame(age_wise_purchase_data.drop_duplicates('SN').groupby('age_category')['SN'].count())

age_data_summary = age_count.merge(tot_pur_price, on = 'age_category', 
                                  how = 'inner').merge(avg_pur_price, on = 'age_category', 
                                  how = 'inner').merge(uniq_cust_count, on = 'age_category', 
                                  how = 'inner')

age_data_summary.rename(columns = {'SN_x': 'Purchase Count', 
                                  'Price_x': 'Total Purchase Value', 
                                  'Price_y': 'Average Purchase Price', 
                                  'SN_y':'Number of Unique purchasers'}, inplace = True)

age_data_summary['Avg Total Purchase per Person'] = age_data_summary['Total Purchase Value']/age_data_summary['Number of Unique purchasers']

age_data_summary['Total Purchase Value'] = age_data_summary['Total Purchase Value'].apply(lambda x: '{:,.2f}%'.format(x))
age_data_summary['Average Purchase Price'] = age_data_summary['Average Purchase Price'].apply(lambda x: '{:,.2f}%'.format(x))
age_data_summary['Avg Total Purchase per Person'] = age_data_summary['Avg Total Purchase per Person'].apply(lambda x: '{:,.2f}%'.format(x))

age_data_summary
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Purchase Count</th>
      <th>Total Purchase Value</th>
      <th>Average Purchase Price</th>
      <th>Number of Unique purchasers</th>
      <th>Avg Total Purchase per Person</th>
    </tr>
    <tr>
      <th>age_category</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>&lt;10</th>
      <td>23</td>
      <td>77.13%</td>
      <td>3.35%</td>
      <td>17</td>
      <td>4.54%</td>
    </tr>
    <tr>
      <th>10-14</th>
      <td>28</td>
      <td>82.78%</td>
      <td>2.96%</td>
      <td>22</td>
      <td>3.76%</td>
    </tr>
    <tr>
      <th>15-19</th>
      <td>136</td>
      <td>412.89%</td>
      <td>3.04%</td>
      <td>107</td>
      <td>3.86%</td>
    </tr>
    <tr>
      <th>20-24</th>
      <td>365</td>
      <td>1,114.06%</td>
      <td>3.05%</td>
      <td>258</td>
      <td>4.32%</td>
    </tr>
    <tr>
      <th>25-29</th>
      <td>101</td>
      <td>293.00%</td>
      <td>2.90%</td>
      <td>77</td>
      <td>3.81%</td>
    </tr>
    <tr>
      <th>30-34</th>
      <td>73</td>
      <td>214.00%</td>
      <td>2.93%</td>
      <td>52</td>
      <td>4.12%</td>
    </tr>
    <tr>
      <th>35-39</th>
      <td>41</td>
      <td>147.67%</td>
      <td>3.60%</td>
      <td>31</td>
      <td>4.76%</td>
    </tr>
    <tr>
      <th>40+</th>
      <td>13</td>
      <td>38.24%</td>
      <td>2.94%</td>
      <td>12</td>
      <td>3.19%</td>
    </tr>
  </tbody>
</table>
</div>



## Top Spenders

* Run basic calculations to obtain the results in the table below


* Create a summary data frame to hold the results


* Sort the total purchase value column in descending order


* Optional: give the displayed data cleaner formatting


* Display a preview of the summary data frame




```python
total_puchase_count_per_player = pd.DataFrame(purchase_data.groupby('SN')['Price'].count())
total_puchase_amt_per_player = pd.DataFrame(purchase_data.groupby('SN')['Price'].sum())
mean_puchase_amt_per_player = pd.DataFrame(purchase_data.groupby('SN')['Price'].mean())

player_wise_purchase_data = total_puchase_count_per_player.merge(total_puchase_amt_per_player, 
                              on = 'SN', how = 'inner').merge(mean_puchase_amt_per_player, 
                              on = 'SN', how = 'inner')

player_wise_purchase_data.rename(columns = {'Price_x': 'Purchase Count', 
                                            'Price_y': 'Total Purchase Amount', 
                                            'Price': 'Average Purchase Amount'}, inplace = True)

player_wise_purchase_data['Average Purchase Amount'] = player_wise_purchase_data['Average Purchase Amount'].apply(lambda x: '${:,.2f}'.format(x))
player_wise_purchase_data['Total Purchase Amount'] = player_wise_purchase_data['Total Purchase Amount'].apply(lambda x: '${:,.2f}'.format(x))

player_wise_purchase_data.sort_values(['Total Purchase Amount'], ascending = [False], inplace = True)

player_wise_purchase_data.head(20)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Purchase Count</th>
      <th>Total Purchase Amount</th>
      <th>Average Purchase Amount</th>
    </tr>
    <tr>
      <th>SN</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Haillyrgue51</th>
      <td>3</td>
      <td>$9.50</td>
      <td>$3.17</td>
    </tr>
    <tr>
      <th>Phistym51</th>
      <td>2</td>
      <td>$9.50</td>
      <td>$4.75</td>
    </tr>
    <tr>
      <th>Lamil79</th>
      <td>2</td>
      <td>$9.29</td>
      <td>$4.64</td>
    </tr>
    <tr>
      <th>Aina42</th>
      <td>3</td>
      <td>$9.22</td>
      <td>$3.07</td>
    </tr>
    <tr>
      <th>Saesrideu94</th>
      <td>2</td>
      <td>$9.18</td>
      <td>$4.59</td>
    </tr>
    <tr>
      <th>Arin32</th>
      <td>2</td>
      <td>$9.09</td>
      <td>$4.54</td>
    </tr>
    <tr>
      <th>Rarallo90</th>
      <td>3</td>
      <td>$9.05</td>
      <td>$3.02</td>
    </tr>
    <tr>
      <th>Baelollodeu94</th>
      <td>2</td>
      <td>$9.03</td>
      <td>$4.51</td>
    </tr>
    <tr>
      <th>Aelin32</th>
      <td>3</td>
      <td>$8.98</td>
      <td>$2.99</td>
    </tr>
    <tr>
      <th>Lisopela58</th>
      <td>3</td>
      <td>$8.86</td>
      <td>$2.95</td>
    </tr>
    <tr>
      <th>Saedaiphos46</th>
      <td>3</td>
      <td>$8.83</td>
      <td>$2.94</td>
    </tr>
    <tr>
      <th>Chanastnya43</th>
      <td>3</td>
      <td>$8.82</td>
      <td>$2.94</td>
    </tr>
    <tr>
      <th>Reunasu60</th>
      <td>2</td>
      <td>$8.82</td>
      <td>$4.41</td>
    </tr>
    <tr>
      <th>Raesty92</th>
      <td>3</td>
      <td>$8.73</td>
      <td>$2.91</td>
    </tr>
    <tr>
      <th>Sundadar27</th>
      <td>2</td>
      <td>$8.71</td>
      <td>$4.35</td>
    </tr>
    <tr>
      <th>Aerithllora36</th>
      <td>2</td>
      <td>$8.64</td>
      <td>$4.32</td>
    </tr>
    <tr>
      <th>Hada39</th>
      <td>3</td>
      <td>$8.57</td>
      <td>$2.86</td>
    </tr>
    <tr>
      <th>Chamilsala65</th>
      <td>2</td>
      <td>$8.55</td>
      <td>$4.28</td>
    </tr>
    <tr>
      <th>Silaera56</th>
      <td>3</td>
      <td>$8.48</td>
      <td>$2.83</td>
    </tr>
    <tr>
      <th>Frichocesta66</th>
      <td>2</td>
      <td>$8.37</td>
      <td>$4.19</td>
    </tr>
  </tbody>
</table>
</div>



## Most Popular Items

* Retrieve the Item ID, Item Name, and Item Price columns


* Group by Item ID and Item Name. Perform calculations to obtain purchase count, item price, and total purchase value


* Create a summary data frame to hold the results


* Sort the purchase count column in descending order


* Optional: give the displayed data cleaner formatting


* Display a preview of the summary data frame




```python
purchased_product_data = purchase_data[['Item ID', 'Item Name', 'Price']].copy()
purchased_product_data.set_index('Item ID')
item_name = pd.DataFrame(purchased_product_data.groupby('Item ID')['Item Name'].unique())
item_price = pd.DataFrame(purchased_product_data.groupby('Item ID')['Price'].unique())
total_puchase_count_per_item = pd.DataFrame(purchased_product_data.groupby('Item ID')['Price'].count())
total_puchase_amt_per_item = pd.DataFrame(purchased_product_data.groupby('Item ID')['Price'].sum())
mean_puchase_amt_per_item = pd.DataFrame(purchased_product_data.groupby('Item ID')['Price'].mean())

item_purchase_summary = item_name.merge(total_puchase_count_per_item, 
                            on = 'Item ID', how = 'inner').merge(total_puchase_amt_per_item, 
                            on = 'Item ID', how = 'inner').merge(mean_puchase_amt_per_item, 
                            on = 'Item ID', how = 'inner')

item_purchase_summary.rename(columns = {'Price_x': 'Items Sold', 
                                        'Price_y': 'Total Sales in $', 
                                        'Price': 'Average Sales in $'}, inplace = True)

item_purchase_summary_sorted = item_purchase_summary.sort_values(['Items Sold'], ascending = [False])

item_purchase_summary_sorted['Total Sales in $'] = item_purchase_summary_sorted['Total Sales in $'].apply(lambda x: '${:,.2f}'.format(x))
item_purchase_summary_sorted['Average Sales in $'] = item_purchase_summary_sorted['Average Sales in $'].apply(lambda x: '${:,.2f}'.format(x))

item_purchase_summary_sorted.head(20)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Item Name</th>
      <th>Items Sold</th>
      <th>Total Sales in $</th>
      <th>Average Sales in $</th>
    </tr>
    <tr>
      <th>Item ID</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>178</th>
      <td>[Oathbreaker, Last Hope of the Breaking Storm]</td>
      <td>12</td>
      <td>$50.76</td>
      <td>$4.23</td>
    </tr>
    <tr>
      <th>145</th>
      <td>[Fiery Glass Crusader]</td>
      <td>9</td>
      <td>$41.22</td>
      <td>$4.58</td>
    </tr>
    <tr>
      <th>108</th>
      <td>[Extraction, Quickblade Of Trembling Hands]</td>
      <td>9</td>
      <td>$31.77</td>
      <td>$3.53</td>
    </tr>
    <tr>
      <th>82</th>
      <td>[Nirvana]</td>
      <td>9</td>
      <td>$44.10</td>
      <td>$4.90</td>
    </tr>
    <tr>
      <th>19</th>
      <td>[Pursuit, Cudgel of Necromancy]</td>
      <td>8</td>
      <td>$8.16</td>
      <td>$1.02</td>
    </tr>
    <tr>
      <th>103</th>
      <td>[Singed Scalpel]</td>
      <td>8</td>
      <td>$34.80</td>
      <td>$4.35</td>
    </tr>
    <tr>
      <th>75</th>
      <td>[Brutality Ivory Warmace]</td>
      <td>8</td>
      <td>$19.36</td>
      <td>$2.42</td>
    </tr>
    <tr>
      <th>72</th>
      <td>[Winter's Bite]</td>
      <td>8</td>
      <td>$30.16</td>
      <td>$3.77</td>
    </tr>
    <tr>
      <th>60</th>
      <td>[Wolf]</td>
      <td>8</td>
      <td>$28.32</td>
      <td>$3.54</td>
    </tr>
    <tr>
      <th>59</th>
      <td>[Lightning, Etcher of the King]</td>
      <td>8</td>
      <td>$33.84</td>
      <td>$4.23</td>
    </tr>
    <tr>
      <th>37</th>
      <td>[Shadow Strike, Glory of Ending Hope]</td>
      <td>8</td>
      <td>$25.28</td>
      <td>$3.16</td>
    </tr>
    <tr>
      <th>34</th>
      <td>[Retribution Axe]</td>
      <td>8</td>
      <td>$17.76</td>
      <td>$2.22</td>
    </tr>
    <tr>
      <th>92</th>
      <td>[Final Critic]</td>
      <td>8</td>
      <td>$39.04</td>
      <td>$4.88</td>
    </tr>
    <tr>
      <th>53</th>
      <td>[Vengeance Cleaver]</td>
      <td>7</td>
      <td>$14.35</td>
      <td>$2.05</td>
    </tr>
    <tr>
      <th>110</th>
      <td>[Suspension]</td>
      <td>7</td>
      <td>$10.08</td>
      <td>$1.44</td>
    </tr>
    <tr>
      <th>7</th>
      <td>[Thorn, Satchel of Dark Souls]</td>
      <td>7</td>
      <td>$9.31</td>
      <td>$1.33</td>
    </tr>
    <tr>
      <th>71</th>
      <td>[Demise]</td>
      <td>7</td>
      <td>$11.27</td>
      <td>$1.61</td>
    </tr>
    <tr>
      <th>117</th>
      <td>[Heartstriker, Legacy of the Light]</td>
      <td>7</td>
      <td>$12.53</td>
      <td>$1.79</td>
    </tr>
    <tr>
      <th>159</th>
      <td>[Oathbreaker, Spellblade of Trials]</td>
      <td>7</td>
      <td>$21.56</td>
      <td>$3.08</td>
    </tr>
    <tr>
      <th>85</th>
      <td>[Malificent Bag]</td>
      <td>7</td>
      <td>$12.25</td>
      <td>$1.75</td>
    </tr>
  </tbody>
</table>
</div>




```python

```

## Most Profitable Items

* Sort the above table by total purchase value in descending order


* Optional: give the displayed data cleaner formatting


* Display a preview of the data frame




```python
item_purchase_summary_sorted_by_sales_amt = item_purchase_summary.sort_values(['Total Sales in $', 'Items Sold'], ascending = [False, False])

item_purchase_summary_sorted_by_sales_amt['Total Sales in $'] = item_purchase_summary_sorted_by_sales_amt['Total Sales in $'].map('${:,.2f}'.format)
item_purchase_summary_sorted_by_sales_amt['Average Sales in $'] = item_purchase_summary_sorted_by_sales_amt['Average Sales in $'].map('${:,.2f}'.format)


item_purchase_summary_sorted_by_sales_amt.head(10)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Item Name</th>
      <th>Items Sold</th>
      <th>Total Sales in $</th>
      <th>Average Sales in $</th>
    </tr>
    <tr>
      <th>Item ID</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>178</th>
      <td>[Oathbreaker, Last Hope of the Breaking Storm]</td>
      <td>12</td>
      <td>$50.76</td>
      <td>$4.23</td>
    </tr>
    <tr>
      <th>82</th>
      <td>[Nirvana]</td>
      <td>9</td>
      <td>$44.10</td>
      <td>$4.90</td>
    </tr>
    <tr>
      <th>145</th>
      <td>[Fiery Glass Crusader]</td>
      <td>9</td>
      <td>$41.22</td>
      <td>$4.58</td>
    </tr>
    <tr>
      <th>92</th>
      <td>[Final Critic]</td>
      <td>8</td>
      <td>$39.04</td>
      <td>$4.88</td>
    </tr>
    <tr>
      <th>103</th>
      <td>[Singed Scalpel]</td>
      <td>8</td>
      <td>$34.80</td>
      <td>$4.35</td>
    </tr>
    <tr>
      <th>59</th>
      <td>[Lightning, Etcher of the King]</td>
      <td>8</td>
      <td>$33.84</td>
      <td>$4.23</td>
    </tr>
    <tr>
      <th>108</th>
      <td>[Extraction, Quickblade Of Trembling Hands]</td>
      <td>9</td>
      <td>$31.77</td>
      <td>$3.53</td>
    </tr>
    <tr>
      <th>78</th>
      <td>[Glimmer, Ender of the Moon]</td>
      <td>7</td>
      <td>$30.80</td>
      <td>$4.40</td>
    </tr>
    <tr>
      <th>72</th>
      <td>[Winter's Bite]</td>
      <td>8</td>
      <td>$30.16</td>
      <td>$3.77</td>
    </tr>
    <tr>
      <th>60</th>
      <td>[Wolf]</td>
      <td>8</td>
      <td>$28.32</td>
      <td>$3.54</td>
    </tr>
  </tbody>
</table>
</div>




```python

```
