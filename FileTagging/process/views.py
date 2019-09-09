from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection
from upload.models import Upload
import json

cur = connection.cursor()

@login_required
def process(request):
    item_list = Upload.objects.filter(status='Processed').order_by('-uploaded_at')[:7]
    return render(request, 'process/process.html', {'item_list': item_list})


def load_button(request):
    files = request.POST.get('doc_file')
    select_query = """Select * from transactions."{}" where existing_match is not null order by id """.format(files)
    cur.execute(select_query)
    result = cur.fetchall()
    old_data_list = []
    i = 1
    for data in result:
        old_data_list.append({"id":i, "comp_name":data[3], "exist_match":data[5]})
        i += 1
    page = request.GET.get('page', 1)
    paginator = Paginator(old_data_list, 5)
    try:
        data_list = paginator.page(page)
    except PageNotAnInteger:
        data_list = paginator.page(1)
    except EmptyPage:
        data_list = paginator.page(paginator.num_pages)
    return render(request, 'process/load_button.html', {'page_obj': data_list})


def load_exact(request):
    files = request.POST.get('doc_file')
    print(files)
    select_query = """Select * from transactions."{}" where existing_match is not null order by id """.format(files)
    cur.execute(select_query)
    result = cur.fetchall()
    old_data_list = []
    i = 1
    for data in result:
        old_data_list.append({"id":i, "comp_name":data[3], "exist_match":data[5]})
        i += 1
    page = request.GET.get('page', 1)
    paginator = Paginator(old_data_list, 5)
    try:
        data_list = paginator.page(page)
    except PageNotAnInteger:
        data_list = paginator.page(1)
    except EmptyPage:
        data_list = paginator.page(paginator.num_pages)
    return render(request, 'process/load_exact.html', {'page_obj': data_list})


def load_exact_page(request):
    page = request.POST.get('page')
    print(page)
    files = request.POST.get('doc_file')
    select_query = """Select * from transactions."{}" where existing_match is not null order by id """.format(files)
    cur.execute(select_query)
    result = cur.fetchall()
    print(result)
    old_data_list = []
    i = 1
    for data in result:
        old_data_list.append({"id":i, "comp_name":data[3], "exist_match":data[5]})
        i += 1
    paginator = Paginator(old_data_list, 5)
    try:
        data_list = paginator.page(page)
    except PageNotAnInteger:
        data_list = paginator.page(1)
    except EmptyPage:
        data_list = paginator.page(paginator.num_pages)
    print(data_list)
    return render(request, 'process/load_exact_page.html', {'page_obj': data_list})


def load_variance(request):
    files = request.POST.get('doc_file')
    print(files)
    select_query = """Select * from transactions."{}" where partial_match is not null order by id """.format(files)
    cur.execute(select_query)
    result = cur.fetchall()
    old_data_list = []
    i = 1
    for data in result:
        old_data_list.append({"id":i, "comp_name":data[3], "variant":data[6], "selected_name":data[10]})
        i += 1
    page = request.GET.get('page', 1)
    paginator = Paginator(old_data_list, 5)
    try:
        data_list = paginator.page(page)
    except PageNotAnInteger:
        data_list = paginator.page(1)
    except EmptyPage:
        data_list = paginator.page(paginator.num_pages)
    return render(request, 'process/load_variance.html', {'page_obj': data_list})


def load_page(request):
    print("Innn")
    page = request.POST.get('page')
    files = request.POST.get('doc_file')
    print(files)
    user = request.user.username
    data = request.POST.getlist('data_new[]')
    if data:
        for value in data:
            new_value = value.split(',')
            comp_name = new_value[1]
            code = new_value[2]
            selected_name = new_value[4]
            print(selected_name)
            if (selected_name != '') :
                if 'No search results.' not in selected_name:
                    if '1 result is available' not in selected_name:
                        if 'results are available' not in selected_name:
                            update_query = """Update transactions."{0}" set variant='{1}', selected_name='{2}', batch_id='{3}', user_name='{4}' where company_name='{5}' """.format(files, code, selected_name, files, user, comp_name)
                            cur.execute(update_query)
                            connection.commit()
    select_query = """Select * from transactions."{}" where partial_match is not null order by id """.format(files)
    cur.execute(select_query)
    result = cur.fetchall()
    old_data_list = []
    i = 1
    for data in result:
        old_data_list.append({"id":i, "comp_name":data[3], "variant":data[6], "selected_name":data[10]})
        i += 1
    paginator = Paginator(old_data_list, 5)
    try:
        data_list = paginator.page(page)
    except PageNotAnInteger:
        data_list = paginator.page(1)
    except EmptyPage:
        print('heyyy')
        data_list = paginator.page(paginator.num_pages)
    print(data_list)
    if int(page) >= int(paginator.num_pages):
        return render(request, 'process/load_last_page.html', {'page_obj': data_list})
    else:
        return render(request, 'process/load_page.html', {'page_obj': data_list})


def load_autocomplete(request): 
    files = request.POST.get('doc_file')
    comp_name = request.POST.get('value')
    select_query = """Select partial_match from transactions."{0}" where company_name = '{1}' """.format(files, comp_name)
    cur.execute(select_query)
    result = cur.fetchone()[0]
    return HttpResponse(result)


def load_variance_code(request):
    match = request.POST.get('match')
    select_query = """Select code from transactions."Master_alt_new" where company_name='{0}'""".format(match)
    cur.execute(select_query)
    result = cur.fetchone()[0]
    return HttpResponse(result)


def load_industry(request):
    files = request.POST.get('doc_file')
    print(files)
    select_query = """Select * from transactions."{}" where existing_match is null and variant is null order by id """.format(files)
    cur.execute(select_query)
    result = cur.fetchall()
    old_data_list = []
    i = 1
    for data in result:
        old_data_list.append({"id":i, "comp_name":data[3], "selected_industry":data[11]})
        i += 1
    page = request.GET.get('page', 1)
    paginator = Paginator(old_data_list, 5)
    try:
        data_list = paginator.page(page)
    except PageNotAnInteger:
        data_list = paginator.page(1)
    except EmptyPage:
        data_list = paginator.page(paginator.num_pages)
    return render(request, 'process/load_industry.html', {'page_obj': data_list})


def load_industry_page(request):
    print('new_file')
    page = request.POST.get('page')
    files = request.POST.get('doc_file')
    save = request.POST.get('save')
    print(files)
    user = request.user.username
    data = request.POST.getlist('data_new[]')
    print(save)
    print(data)
    if data:
        for value in data:
            if value != '':
                new_value = value.split(',')
                comp_name = new_value[1]
                selected_industry = new_value[2]
                if selected_industry != '':
                    update_query = """Update transactions."{0}" set industry='{1}', selected_industry='{2}', batch_id='{3}', user_name='{4}' where company_name='{5}' """.format(files, selected_industry, selected_industry, files, user, comp_name)
                    cur.execute(update_query)
                    connection.commit()
    if save == 'True':
        status = 'Export'
        master_update_query = """Update input_master set status='{0}' where batchfile_name='{1}' """.format(status, files)
        cur.execute(master_update_query)
        connection.commit()
    select_query = """Select * from transactions."{}" where existing_match is null and variant is null order by id """.format(files)
    cur.execute(select_query)
    result = cur.fetchall()
    old_data_list = []
    i = 1
    for data in result:
        old_data_list.append({"id":i, "comp_name":data[3], "selected_industry":data[11]})
        i += 1
    paginator = Paginator(old_data_list, 5)
    print(paginator.num_pages)
    try:
        data_list = paginator.page(page)
    except PageNotAnInteger:
        data_list = paginator.page(1)
    except EmptyPage:
        data_list = paginator.page(paginator.num_pages)
    if int(page) >= int(paginator.num_pages):
        return render(request, 'process/load_industry_last_page.html', {'page_obj': data_list})
    else:
        return render(request, 'process/load_industry_page.html', {'page_obj': data_list})

    



