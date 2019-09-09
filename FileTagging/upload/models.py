from .validators import validate_file_extension
from django.db import models

class Upload(models.Model):
    batchfile_name = models.CharField(max_length=250, verbose_name=('Batch File Name'))
    file_path = models.FileField(upload_to="upload/%Y/%m/%d", verbose_name=('Files'), validators=[validate_file_extension])
    uploaded_by = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)
    download_path = models.CharField(max_length=250, null=True)

    def __str__(self):
        return str(self.batchfile_name)

    class Meta:
        db_table = "input_master"

