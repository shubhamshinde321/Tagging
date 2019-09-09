from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from upload.models import Upload


@login_required
def export(request):
    file_download = Upload.objects.filter(status='Download').order_by('-uploaded_at')
    print(file_download)
    return render(request, 'export/export.html', {'file_download': file_download})

def load_files(request):
    files = request.POST.get('doc_file')
    print(files)
    file_path = Upload.objects.filter(batchfile_name=files).values('download_path')
    print(file_path)
    return render(request, 'export/load_files.html', {'file_path': file_path})