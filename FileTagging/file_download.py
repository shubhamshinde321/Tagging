from sqlalchemy import create_engine
from datetime import datetime
import psycopg2
import csv
import sys
import os


def create_conn():           # Postgresql Database Connection is been Created.
    conn1 = psycopg2.connect(user='postgres', password='Shubham@123', host='localhost', port='5432', database='File_Tagging')
    cur1 = conn1.cursor()
    return conn1, cur1


def update_table(trimmed_file_path, status, files):
    conn, cur = create_conn()
    downoad_path_update = "Update input_master set download_path = '{0}', status='{1}' where batchfile_name='{2}'".format(trimmed_file_path, status, files)
    cur.execute(downoad_path_update)
    conn.commit()

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


def file_download_path(filename):
    date = str(datetime.date(datetime.now()))
    mydir = os.getcwd()
    media_dir = os.path.join(mydir, 'media')
    if not os.path.exists(media_dir):
        os.mkdir(media_dir)
    download_dir = os.path.join(media_dir, 'download')
    if not os.path.exists(download_dir):
        os.mkdir(download_dir)
    date_dir = os.path.join(download_dir, date)
    if not os.path.exists(date_dir):
        os.mkdir(date_dir)
    file_dir = os.path.join(date_dir, filename)
    print(file_dir)
    return file_dir


def file_download(files, log_file):
    date = str(datetime.date(datetime.now()))
    conn, cur = create_conn()
    try:
        export_query = """SELECT id, daily, domain, company_name, dba, existing_match, variant, industry from transactions."{}" ORDER BY id""".format(files)
        cur.execute(export_query)
        data_list = cur.fetchall()
        filename = files + '.txt'
        file_path = file_download_path(filename)
        with open(file_path, 'w', newline='', encoding="utf-8") as f1:
            new_file = csv.writer(f1, delimiter='\t')
            new_file.writerow(
                ['Id', 'Daily', 'Domain', 'Company_name', 'dba', 'Existing_match', 'Variant', 'Industry'])
            for data in data_list:
                new_file.writerow(data)
        trimmed_file_path = str('media' + '/' + 'download' + '/' + date + '/' + filename)
        status = 'Download'
        update_table(trimmed_file_path, status, files)
    except Exception as error:
        process = "File Download"
        log_update(log_file, process, files, str(error))


if __name__ == '__main__':
    conn, cur = create_conn()
    date = str(datetime.date(datetime.now()))
    mydir = os.getcwd()
    log_folder = os.path.join(mydir, 'Log_Folder')
    if not os.path.exists(log_folder):
        os.mkdir(log_folder)
    date_folder = os.path.join(log_folder, date)
    if not os.path.exists(date_folder):
        os.mkdir(date_folder)
    file_select = """Select batchfile_name from input_master where status='Export'"""
    cur.execute(file_select)
    file_result = cur.fetchall()
    print(file_result)
    for file in file_result:
        batch_file = file[0]
        log_file_name = 'Export_' + batch_file + "_LogFile.txt"
        log_file = os.path.join(date_folder, log_file_name)
        file_download(batch_file, log_file)
