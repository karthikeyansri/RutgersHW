
import os
import csv


def file_to_summary_dict(file_path): 
    ## Empty_dict for candidate and the votes received
    candidate_votes = {}
    
    with open(file_path, 'r', newline='') as ctx: 
        csvReader = csv.reader(ctx, delimiter = ',')
        records = 0
        for row in csvReader: 
            if csvReader.line_num == 1:
                continue
            
            records += 1
            candidate = row[2].strip()

            if candidate in candidate_votes.keys(): 
                votes = candidate_votes[candidate] + 1
                candidate_votes.update({candidate: votes})
            else: 
                candidate_votes.update({candidate: 1})
    
    return candidate_votes, records


def file_to_county_summary_dict(file_path): 

    ## Empty_dict for checking county-wise votes received by a candidate
    candidate_county_votes = {}

    with open(file_path, 'r', newline='') as ctx: 
        csvReader = csv.reader(ctx, delimiter = ',')
        records = 0
        for row in csvReader: 
            if csvReader.line_num == 1:
                continue
            
            records += 1
            candidate = row[2].strip()
            candidate_county = candidate + '~~' + row[1].strip()

            if candidate_county in candidate_county_votes.keys(): 
                votes = candidate_county_votes[candidate_county] + 1
                candidate_county_votes.update({candidate_county: votes})
            else: 
                candidate_county_votes.update({candidate_county: 1})
    
    return candidate_county_votes, records


def get_line_str(): 
    return '--------------------------------------------------------------'


def write_results(out_path, content): 
    out_dir_name = os.path.dirname(out_path)

    if not os.path.exists(out_dir_name): 
        os.mkdir(out_dir_name, 511)
    file_name = os.path.split(out_path)[1]
    
    with open(os.path.join(out_dir_name, file_name), 'a') as ctx: 
        ctx.write(content)


def get_std_result_str(rec_dict, rec_len): 
    max_votes = -1
    winner_str = ''
    
    out_str = ''
    out_str = out_str + '\n' + get_line_str()
    out_str = out_str + '\n' + 'Election Results'
    out_str = out_str + '\n' + get_line_str()
    out_str = out_str + '\n' + 'Total Votes: ' + str(rec_len)
    out_str = out_str + '\n' + get_line_str()
    
    for key, value in rec_dict.items(): 
        if max_votes < value: 
            max_votes = value
            winner_str = 'Winner: ' + key
        
        vote_percentage = 100 * value/rec_len
        out_str = out_str + '\n' + key + ': ' + str(round(vote_percentage, 3)) + '% (' + str(value) + ')'
    
    out_str = out_str + '\n' + get_line_str()
    out_str = out_str + '\n' + winner_str
    out_str = out_str + '\n' + get_line_str()
    
    print(out_str)
    
    return out_str

def get_extended_result_str(rec_dict, total_votes): 
    max_votes_per_county_per_candidate = -1
    county_winner_str = ''
    
    counties = {}
    out_str = '' + '\n\n\n'
    out_str = out_str + '\n' + get_line_str()
    out_str = out_str + '\n' + 'County-Wise election results'
    out_str = out_str + '\n' + get_line_str()

    for key, value in rec_dict.items(): 
        county = key.split('~~')[1]
        if county in counties.keys(): 
            counties.update({county: counties[county] + value})
        else: 
            counties.update({county: value})

    for key, value in counties.items(): 
        out_str = out_str + '\n' + 'Polled votes in ' + key + ' county: ' + str(value) 
        out_str = out_str + '; (' + str(round(100 * value / total_votes, 3)) + '% of total votes polled)'
        out_str = out_str + '\n' + get_line_str()
        prev_cndt = ''
        for cndt_cnty, votes in rec_dict.items(): 
            candidate = cndt_cnty.split('~~')[0]
            county = cndt_cnty.split('~~')[1]
            if county == key and prev_cndt != candidate: 
                if max_votes_per_county_per_candidate < votes: 
                    max_votes_per_county_per_candidate = votes
                    county_winner_str = '\n' + get_line_str() + '\n'
                    county_winner_str = county_winner_str + 'Winner in ' + county + ': ' + candidate
                    county_winner_str = county_winner_str + '\n' + get_line_str()

                county_vote_percentage = 100 * votes / value
                out_str = out_str + '\n' + candidate + ' -- Vote Percentage: ' + str(round(county_vote_percentage, 3)) + '% -- Votes: ' + str(votes)
        max_votes_per_county_per_candidate = -1
        out_str = out_str + '\n' + county_winner_str + '\n'
    
    print(out_str)
    return out_str

file_path = os.path.join('.', 'Resources', 'election_data.csv')
out_path = os.path.join('.', 'output', 'out.txt')

summary_dict, rec_len = file_to_summary_dict(file_path)
out_str = get_std_result_str(summary_dict, rec_len)
write_results(out_path, out_str)

summary_dict, rec_len = file_to_county_summary_dict(file_path)
out_str = get_extended_result_str(summary_dict, rec_len)
write_results(out_path, out_str)
