
import os
import csv


def file_to_list(file_path): 
    data_list = []
    with open(file_path, 'r', newline = '') as ctx: 
        csvReader = csv.reader(ctx, delimiter = ',')
        for row in csvReader:
            if csvReader.line_num == 1:
                continue
            else: 
               data_list.append(row) 
    return data_list


def calculate_total_months(data): 
    
    '''
        Set is used to calculate the number of months.
        Set will discard duplicates and hence, 
        even if the data had duplicates, 
        it will not be added to the set and 
        we will get the exact number of months in the data
    '''
    month_year_set = set([])
    for item in data: 
        month = item[0].split('-')[0]
        year = item[0].split('-')[1]
        month_year = '{}{}'.format(month, year)
        month_year_set.add(month_year)
    return len(month_year_set)
    

def is_number(s):
    for index in range(len(s)): 
        if s[index].isdigit() == False: 
            return False
 
    return True


def calculate_periodic_profits(data, month_dict): 
    
    '''
        If there is additional entry for same year_month combination, 
        then sum the profit with previous profits
        Add year and month as key and 
        profit as value in a dictionary
        Add year as key and 
        yearly profit as value in a dictionary
    '''
    periodic_profit_dict = {}
    min_year = 9999
    max_year = 0
    total_profits_key = 'Total_profits'
    '''
        Create unique entries for year and year_month and 
        store profits associated to the period in a dict,.
        if there are multiple entries for the same year and month combination, 
        add the profit or loss to previous values.
    '''
    for item in data: 
        month = month_dict[item[0].split('-')[0]]
        year = item[0].split('-')[1]
        monthly_profit_loss = int(item[1])
        yearly_profit_loss = monthly_profit_loss
        year_month = '{}_{}'.format(year, month)
        
        if min_year > int(year): 
            min_year = int(year)
        
        if max_year < int(year): 
            max_year = int(year)
        
        if total_profits_key in periodic_profit_dict.keys(): 
            total_profits = periodic_profit_dict[total_profits_key] + monthly_profit_loss
        else: 
            total_profits = monthly_profit_loss
        periodic_profit_dict.update({total_profits_key: total_profits})
        
        if year in periodic_profit_dict.keys(): 
            yearly_profit_loss = periodic_profit_dict[year] + yearly_profit_loss
        else: 
            yearly_profit_loss = monthly_profit_loss
        periodic_profit_dict.update({year: yearly_profit_loss})
        
        if year_month in periodic_profit_dict.keys(): 
            monthly_profit_loss = periodic_profit_dict[year_month] + monthly_profit_loss
        periodic_profit_dict.update({year_month: monthly_profit_loss})
    
    return (min_year, max_year, periodic_profit_dict)


def calculate_deltas(periodic_profit_dict, min_year, max_year, month_dict): 
    
    '''
        Traverse through the dictionary and find the yearly and monthly deltas. 
        The dictionary will have only one entry for year and one entry for year_month. 
        
        Get per year data from the aggregated data and
        calculate the deltas
        Store deltas in separate dict
    '''
    periodic_delta_dict = {}
    
    min_month = min(month_dict.values())
    max_month = max(month_dict.values())
    prev_month_str = ''
    prev_month_dict = {}
    
    for year in range(min_year, max_year + 1):
        '''Create separate dict for consecutive years from the periodic_profit_dict'''
        current_year_dict = {k: v for k, v in periodic_profit_dict.items() if str(year) in k}
        next_year_dict = {k: v for k, v in periodic_profit_dict.items() if str(year + 1) in k}
        
        for month in range(min_month, max_month + 1): 
            current_month_str = '{}_{}'.format(str(year), str(month))
            next_month_str = '{}_{}'.format(str(year), str(month + 1))
            
            current_month_dict = {k: v for k, v in current_year_dict.items() if current_month_str == k}
            next_month_dict = {k: v for k, v in current_year_dict.items() if next_month_str == k}
            
            if len(prev_month_dict) != 0 and len(next_month_dict) != 0: 
                monthly_change = current_month_dict[current_month_str] - prev_month_dict[prev_month_str]
                monthly_period = '{}--{}'.format(prev_month_str, current_month_str)
                periodic_delta_dict.update({monthly_period: monthly_change})
                prev_month_str = ''
                prev_month_dict = {}
            
            if len(next_month_dict) == 0: 
                prev_month_str = current_month_str
                prev_month_dict = current_month_dict
                continue
            
            monthly_change = next_month_dict[next_month_str] - current_month_dict[current_month_str]
            monthly_period = '{}--{}'.format(current_month_str, next_month_str)
            
            periodic_delta_dict.update({monthly_period: monthly_change})
        
        if len(next_year_dict) == 0: 
            continue
        
        yearly_change = next_year_dict[str(year + 1)] - current_year_dict[str(year)]
        yearly_period = '{}--{}'.format(str(year), str(year + 1))
        
        periodic_delta_dict.update({yearly_period: yearly_change})
    
    return periodic_delta_dict


def write_results(out_path, content): 
    out_dir_name = os.path.dirname(out_path)

    if not os.path.exists(out_dir_name): 
        os.mkdir(out_dir_name, 511)
    file_name = os.path.split(out_path)[1]
    
    with open(os.path.join(out_dir_name, file_name), 'a') as ctx: 
        ctx.write(content)
    

def analyze_print_save_result(file_path, out_path): 
    
    month_dict = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
    total_profits_key = 'Total_profits'
    total_profits = 0
    sum_of_changes = 0
    average_change = 0
    
    max_change_in_profits = 0
    min_change_in_profits = 0
    
    file_data = file_to_list(file_path)
    total_months = calculate_total_months(file_data)
    
    min_year, max_year, profit_summary_dict = calculate_periodic_profits(file_data, month_dict)
    
    for key, value in profit_summary_dict.items(): 
        if key == total_profits_key:
            total_profits = profit_summary_dict[key]
            break
    
    periodic_delta_dict = calculate_deltas(profit_summary_dict, min_year, max_year, month_dict)

    y_m_count = 0
    date_max_change_in_profits = ''
    date_min_change_in_profits = ''
    for key, value in periodic_delta_dict.items(): 
        if len(key.split('_')) < 2:
            continue
        
        y_m_count += 1
        sum_of_changes = value + sum_of_changes
        
        key_y_m_stop = key.split('--')[1]
        key_y_stop = key_y_m_stop.split('_')[0]
        key_m_stop = key_y_m_stop.split('_')[1]
        
        date = ''
        for month, index in month_dict.items(): 
            if index == int(key_m_stop):
                date = '{}-{}'.format(month, key_y_stop)
        
        if max_change_in_profits < value: 
            max_change_in_profits = value
            date_max_change_in_profits = date
        
        if min_change_in_profits > value: 
            min_change_in_profits = value
            date_min_change_in_profits = date
        
    average_change = sum_of_changes / y_m_count
        
    out_str = ''
    out_str = out_str + '\n' + 'Financial Analysis' + '\n' + '----------------------------'
    out_str = out_str + '\n' + 'Total Months: ' + str(total_months)
    out_str = out_str + '\n' + 'Average  Change: $' + str(round(average_change, 2))
    out_str = out_str + '\n' + f'Greatest Increase in Profits: {date_max_change_in_profits} (${max_change_in_profits})'
    out_str = out_str + '\n' + f'Greatest Decrease in Profits: {date_min_change_in_profits} (${min_change_in_profits})'
    print(out_str)
    
    write_results(out_path, out_str)


file_path = os.path.join('./Resources/budget_data.csv')
out_path = os.path.join('.', 'output', 'out.txt')
analyze_print_save_result(file_path, out_path)
