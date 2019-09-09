from django.core.exceptions import ValidationError
import os

def validate_file_extension(files):
    ext = os.path.splitext(files.name)[1]
    valid_ext = ['.xlsx', '.xls']
    if not ext.lower() in valid_ext:
        raise ValidationError("File Extension Not Valid")