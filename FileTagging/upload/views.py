from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UploadForm
from .models import Upload


@login_required
def home(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            batch_file_name = form.cleaned_data['batchfile_name']
            file_path = form.cleaned_data['file_path']
            user = request.user.username
            if file_path != 'None':
                if Upload.objects.filter(batchfile_name=batch_file_name).exists() == False:
                    form = Upload(batchfile_name=batch_file_name, file_path=file_path, uploaded_by=user, status='Uploaded')
                    form.save()
                    print(file_path)
                    print(batch_file_name)
                    print(user)
                    print("successfull")
                    messages.success(request, "File Uploaded Successfully")
                    return redirect('home')
                else:
                    messages.warning(request, "Batch File already exists")
                    return redirect('home')
        else:
            print("Not Valid")
            messages.warning(request, "File Extension is Invalid")
            return redirect('home')
    else:
        form = UploadForm()
        files_list_data = Upload.objects.all().values('batchfile_name', 'uploaded_by', 'uploaded_at', 'status').order_by('-uploaded_at')[0:50]
        page = request.GET.get('page', 1)
        paginator = Paginator(files_list_data, 5)
        # print(paginator)
        try:
            files_list = paginator.page(page)
        except PageNotAnInteger:
            files_list = paginator.page(1)
        except EmptyPage:
            files_list = paginator.page(paginator.num_pages)
        return render(request, 'upload/upload.html', {'form': form, 'files_list': files_list})


def file_table(request):
    files_list = Upload.objects.all().values('batchfile_name', 'uploaded_by', 'uploaded_at', 'status').order_by('-uploaded_at')[0:50]
    return render(request, 'upload/upload.html', {'files_list': files_list})

def load_status_table(request):
    print('innn')
    files_list_data = Upload.objects.all().values('batchfile_name', 'uploaded_by', 'uploaded_at', 'status').order_by('-uploaded_at')[0:50]
    page = request.GET.get('page', 1)
    paginator = Paginator(files_list_data, 5)
    try:
        files_list = paginator.page(page)
    except PageNotAnInteger:
        files_list = paginator.page(1)
    except EmptyPage:
        files_list = paginator.page(paginator.num_pages)
    print(files_list)
    return render(request, 'upload/load_status_table.html', {'files_list': files_list})

