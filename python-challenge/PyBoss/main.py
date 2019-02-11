
import os
import csv

us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}

def file_to_manipulated_list(file_path, us_state_abbrev): 
    out_list = []
    out_list.append(['Emp ID', 'First Name', 'Last Name', 'DOB', 'SSN', 'State'])
    with open(file_path, 'r') as ctx: 
        csvReader = csv.reader(ctx, delimiter = ',')
        for row in csvReader: 
            if csvReader.line_num == 1: 
                continue
            emp_id = row[0]
            f_name = row[1].split(' ')[0]
            l_name = row[1].split(' ')[1]
            dt_o_b = '{}/{}/{}'.format(row[2].split('-')[1], row[2].split('-')[2], row[2].split('-')[0])
            so_sec = '***-**-{}'.format(row[3].split('-')[2])
            abb_st = ''
            for key, value in us_state_abbrev.items(): 
                if key == row[4]: 
                    abb_st = value
            out_list.append([emp_id, f_name, l_name, dt_o_b, so_sec, abb_st])
    return out_list


def write_results(out_path, out_list): 
    out_dir_name = os.path.dirname(out_path)

    if not os.path.exists(out_dir_name): 
        os.mkdir(out_dir_name, 511)
    file_name = os.path.split(out_path)[1]
    
    with open(os.path.join(out_dir_name, file_name), 'w') as ctx: 
        writer = csv.writer(ctx)
        for row in out_list: 
            writer.writerow(row)


file_path = os.path.join('.', 'Resources', 'employee_data.csv')
out_path = os.path.join('.', 'output', 'out.csv')
data_list = file_to_manipulated_list(file_path, us_state_abbrev)
write_results(out_path, data_list)