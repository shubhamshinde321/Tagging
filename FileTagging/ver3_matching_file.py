#Version 3.0

from sqlalchemy import create_engine
from datetime import datetime
import pandas as pd
import psycopg2
import json
import sys
import os
import re


def create_conn():           # Postgresql Database Connection is been Created.
    conn = psycopg2.connect(user='postgres', password='Shubham@123', host='localhost', port='5432', database='File_Tagging')
    cur = conn.cursor()
    return conn, cur


def log_headers(log_file):
    if not os.path.exists(log_file):
        with open(log_file, 'w') as f:
            f.write('File_Name' + '\t')
            f.write('Process' + '\t')
            f.write('Status' + '\t')
            f.write('Time')


def log_update(log_file, process, file_name, message):          # Update log table.
    log_headers(log_file)
    with open(log_file, 'a') as f:
        f.write('\n')
        f.write(str(file_name) + '\t')
        f.write(str(process) + '\t')
        f.write(message + '\t')
        f.write(str(datetime.now()))


def update_table(status, batch_file_name):
    conn, cur = create_conn()
    update = """Update input_master set status='{}' where batchfile_name='{}' """.format(status, batch_file_name)
    cur.execute(update)
    conn.commit()


def create_keyword_table(new_keyword_table):
    conn, cur = create_conn()
    create_table_keyword = """Create table if not exists transactions."{}"(company_name text,
                            matched_company_name text)""".format(new_keyword_table)
    cur.execute(create_table_keyword)
    conn.commit()


def create_input_master_table(input_master_table):
    conn, cur = create_conn()
    create_table_keyword = """Create table if not exists transactions.{}(
                            id bigserial primary key,
                            file_name text,
                            uploaded_by text,
                            batch_file_name text,
                            date timestamp with time zone)""".format(input_master_table)
    cur.execute(create_table_keyword)
    conn.commit()


def create_table(path, table_name, log_file):
    table_created = False
    try:
        engine = create_engine("postgresql://postgres:Shubham@123@localhost:5432/File_Tagging")
        df_column = pd.read_excel(open(path, 'rb'), sheet_name=0, nrows=0)
        columns = df_column.columns
        column_list = []

        for col in columns:
            if '(' in col:
                col = str(col).replace('(', ' ').replace(')', ' ')
            col = col.strip()
            col = re.sub(r"\s+", '_', col)
            column_list.append(col.lower())

        df = pd.read_excel(open(path, 'rb'), sheet_name=0, names=column_list)
        # if "Input" in table_name:
        df.insert(loc=4, column='existing_match', value=None)
        df.insert(loc=5, column='variant', value=None)
        df.insert(loc=6, column='industry', value=None)
        df.insert(loc=7, column='batch_id', value=None)
        df.insert(loc=8, column='partial_match', value=None)
        df.insert(loc=9, column='selected_name', value=None)
        df.insert(loc=10, column='selected_industry', value=None)
        df.insert(loc=11, column='user_name', value=None)
        df.rename({'original': 'company_name'}, axis=1, inplace=True)
        # cols = ['company_name', 'domain', 'Daily', 'existing_match', 'variant', 'industry']
        # df = df[cols]
        df.index += 1
        df.to_sql(table_name, engine, schema='transactions', index=True, index_label='id')
        table_created = True
        # else:
        #     df.rename({'syncon': 'code'}, axis=0, inplace=True)
        #     df.rename({'lemma1': 'company_name'}, axis=1, inplace=True)
        #     # df.insert(loc=2, column='file_name', value=file_name)
        #     df.to_sql(table_name, engine, schema='transactions', index=False)
        #     table_created = True

    except Exception as error:
        process = "Table Creation"
        log_update(log_file, process, table_name, str(error))

    return table_created


def tagging(master_table, input_table, keyword_table, log_file):
    conn, cur = create_conn()
    file_name = input_table
    try:
        select_input_query = """Select company_name from transactions."{}" order by id""".format(input_table)
        cur.execute(select_input_query)
        input_result = cur.fetchall()
        select_master_query = """Select code, company_name from transactions."{}" """.format(master_table)
        cur.execute(select_master_query)
        result = cur.fetchall()

        for data in result:
            code = data[0]
            company_name = data[1]
            for keyword in input_result:
                key = keyword[0]
                if key == company_name:
                    print(key)
                    print(code)
                    update_data_query = """Update transactions."{}" set existing_match = '{}' where company_name='{}' """.format(input_table, code, company_name)
                    cur.execute(update_data_query)
                    conn.commit()
        partial_tagging(result, input_table, keyword_table, file_name, log_file)

    except Exception as error1:
        process = "Perfect match tagging"
        log_update(log_file, process, file_name, str(error1))


def partial_tagging(result, input_table, keyword_table, file_name, log_file):
    conn, cur = create_conn()
    stop_words = ['A', 'About', 'Above', 'Above', 'Across', 'After', 'Afterwards', 'Again', 'Against', 'All', 'Almost',
                  'Alone', 'Along', 'Already', 'Also', 'Although', 'Always', 'Am', 'Among', 'Amongst', 'Amoungst',
                  'Amount', 'An', 'And', 'Another', 'Any', 'Anyhow', 'Anyone', 'Anything', 'Anyway', 'Anywhere', 'Are',
                  'Around', 'As', 'At', 'Back', 'Be', 'Became', 'Because', 'Become', 'Becomes', 'Becoming', 'Been',
                  'Before', 'Beforehand', 'Behind', 'Being', 'Below', 'Beside', 'Besides', 'Between', 'Beyond', 'Bill',
                  'Both', 'Bottom', 'But', 'By', 'Call', 'Can', 'Cannot', 'Cant', 'Co', 'Con', 'Could', 'Couldnt',
                  'Cry', 'De', 'Describe', 'Detail', 'Do', 'Done', 'Down', 'Due', 'During', 'Each', 'Eg', 'Eight',
                  'Either', 'Eleven', 'Else', 'Elsewhere', 'Empty', 'Enough', 'Etc', 'Even', 'Ever', 'Every',
                  'Everyone', 'Everything', 'Everywhere', 'Except', 'Few', 'Fifteen', 'Fify', 'Fill', 'Find', 'Fire',
                  'First', 'Five', 'For', 'Former', 'Formerly', 'Forty', 'Found', 'Four', 'From', 'Front', 'Full',
                  'Further', 'Get', 'Give', 'Go', 'Had', 'Has', 'Hasnt', 'Have', 'He', 'Hence', 'Her', 'Here',
                  'Hereafter', 'Hereby', 'Herein', 'Hereupon', 'Hers', 'Herself', 'Him', 'Himself', 'His', 'How',
                  'However', 'Hundred', 'Ie', 'If', 'In', 'Inc', 'Indeed', 'Interest', 'Into', 'Is', 'It', 'Its',
                  'Itself', 'Keep', 'Last', 'Latter', 'Latterly', 'Least', 'Less', 'Ltd', 'Made', 'Many', 'May', 'Me',
                  'Meanwhile', 'Might', 'Mill', 'Mine', 'More', 'Moreover', 'Most', 'Mostly', 'Move', 'Much', 'Must',
                  'My', 'Myself', 'Name', 'Namely', 'Neither', 'Never', 'Nevertheless', 'Next', 'Nine', 'No', 'Nobody',
                  'None', 'Noone', 'Nor', 'Not', 'Nothing', 'Now', 'Nowhere', 'Of', 'Off', 'Often', 'On', 'Once',
                  'One', 'Only', 'Onto', 'Or', 'Other', 'Others', 'Otherwise', 'Our', 'Ours', 'Ourselves', 'Out',
                  'Over', 'Own', 'Part', 'Per', 'Perhaps', 'Please', 'Put', 'Rather', 'Re', 'Same', 'See', 'Seem',
                  'Seemed', 'Seeming', 'Seems', 'Serious', 'Several', 'She', 'Should', 'Show', 'Side', 'Since',
                  'Sincere', 'Six', 'Sixty', 'So', 'Some', 'Somehow', 'Someone', 'Something', 'Sometime', 'Sometimes',
                  'Somewhere', 'Still', 'Such', 'System', 'Take', 'Ten', 'Than', 'That', 'The', 'Their', 'Them',
                  'Themselves', 'Then', 'Thence', 'There', 'Thereafter', 'Thereby', 'Therefore', 'Therein',
                  'Thereupon', 'These', 'They', 'Thick', 'Thin', 'Third', 'This', 'Those', 'Though', 'Three', 'Through',
                  'Throughout', 'Thru', 'Thus', 'To', 'Together', 'Too', 'Top', 'Toward', 'Towards', 'Twelve', 'Twenty',
                  'Two', 'Un', 'Under', 'Until', 'Up', 'Upon', 'Us', 'Very', 'Via', 'Was', 'We', 'Well', 'Were', 'What',
                  'Whatever', 'When', 'Whence', 'Whenever', 'Where', 'Whereafter', 'Whereas', 'Whereby', 'Wherein',
                  'Whereupon', 'Wherever', 'Whether', 'Which', 'While', 'Whither', 'Who', 'Whoever', 'Whole', 'Whom',
                  'Whose', 'Why', 'Will', 'With', 'Within', 'Without', 'Would', 'Yet', 'You', 'Your', 'Yours',
                  'Yourself', 'Yourselves', 'The', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
                  'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    try:
        select_new_input_query = """Select company_name from transactions."{}" where existing_match is null order by id""".format(input_table)
        cur.execute(select_new_input_query)
        new_input_result = cur.fetchall()

        for keyword in new_input_result:
            raw_input_key = keyword[0]
            if '(' in raw_input_key:
                input_key = raw_input_key.split('(')[0]
                key_list = input_key.split(' ')
            else:
                key_list = raw_input_key.split(' ')
            if len(key_list) > 1:
                new_key_list = []
                stop_word_key = []
                for i in range(len(key_list) - 1):
                    if new_key_list:
                        new_key_list.append(new_key_list[-1] + " " + key_list[i])
                    else:
                        if key_list[i].title() in stop_words:
                            stop_word_key.append(key_list[i])
                        else:
                            if stop_word_key:
                                new_key = str(' '.join(stop_word_key))
                                new_key = new_key + ' ' + key_list[i]
                                new_key_list.append(new_key)
                            else:
                                new_key_list.append(key_list[i])
            else:
                new_key_list = key_list

            match_found = []
            temp_list = []
            try:
                match_found_dict = {}
                for i in range(len(new_key_list)):
                    if i < 1:
                        for sentence in result:
                            search_key = r'^{}\s'.format(new_key_list[i])
                            match = re.search(search_key, sentence[1])
                            if match:
                                match_found.append(sentence[1])
                    else:
                        for new_sentence in match_found:
                            if i == len(new_key_list) - 1:
                                search_key = r'^{}'.format(new_key_list[i])
                            else:
                                search_key = r'^{}\s'.format(new_key_list[i])
                            match = re.search(search_key, new_sentence)
                            if match:
                                temp_list.append(new_sentence)

                        if not temp_list:
                            break

                    if temp_list:
                        match_found.clear()
                        match_found = temp_list.copy()
                        temp_list.clear()

                if match_found:
                    new_match_found = []
                    for val in match_found:
                        new_dict = {'name': val}
                        new_match_found.append(new_dict)
                    json_match_found = json.dumps(new_match_found)
                    # insert_keyword_query = """Insert into transactions."{}"(company_name, matched_company_name) values(%s, %s) """.format(keyword_table)
                    insert_keyword_query = """Update transactions."{0}" set partial_match=%s where company_name=%s """.format(input_table)
                    cur.execute(insert_keyword_query, (json_match_found, raw_input_key),)
                    conn.commit()

            except Exception as err:
                process = "Partial tagging:- Input iterating"
                error = str(err) + " " + new_key_list[-1]
                log_update(log_file, process, file_name, error)

        final_update = "Update input_master set status='Processed' where batchfile_name='{}'".format(file_name)
        cur.execute(final_update)
        conn.commit()

    except Exception as err1:
        print(err1)
        process = "Partial tagging"
        log_update(log_file, process, file_name, str(err1))


if __name__ == '__main__':
    start = datetime.now()
    mydir = os.getcwd()
    date = str(datetime.date(datetime.now()))
    conn, cur = create_conn()
    select_file_query = "Select * from input_master where status='Uploaded' order by uploaded_by"
    cur.execute(select_file_query)
    result = cur.fetchall()
    print(result)
    for data in result:
        file_id = data[0]
        batch_file_name = data[1]
        file_path = data[2]
        uploaded_by = [3]
        input_file_path = mydir + '/media/' + file_path
        new_keyword_table = batch_file_name + '_partial'
        master_table = "Master_alt_new"

        log_folder = os.path.join(mydir, 'Log_Folder')
        if not os.path.exists(log_folder):
            os.mkdir(log_folder)
        date_folder = os.path.join(log_folder, date)
        if not os.path.exists(date_folder):
            os.mkdir(date_folder)
        log_file_name = batch_file_name + "_LogFile.txt"
        log_file = os.path.join(date_folder, log_file_name)
        status = 'Processing Started'
        update_table(status, batch_file_name)
        # master_table = "Master_main_new"
        # input_table = "Input_alt_new"
        # keyword_table = "keyword_alt_new"
        # input_master_table = "input_master_table"
        # create_input_master_table(input_master_table)
        # master_table_created = create_table(data_file_path, master_table, data_file, log_file)
        keyword_table_created = create_table(input_file_path, batch_file_name, log_file)
        if keyword_table_created:
            tagging(master_table, batch_file_name, new_keyword_table, log_file)
        print(datetime.now() - start)

