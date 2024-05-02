import os

def keep_recent_files(folder_path, number_of_files_to_keep=5):
    # Get the list of files in the folder
    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    
    files.sort(key=os.path.getmtime, reverse=True)
    
    files_to_delete = files[number_of_files_to_keep:]
    
    for file in files_to_delete:
        os.remove(file)
        print(f"Deleted old backup file: {file}")

    if not files_to_delete:
        print(f"There are only {len(files)} backups, and the threshold is {number_of_files_to_keep}, so no files were deleted.")