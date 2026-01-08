from fastapi import UploadFile, HTTPException
import os

def validate_excel_file(file: UploadFile):
    if not file.filename.endswith(('.xls', '.xlsx')):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload an Excel file.")
    return True
