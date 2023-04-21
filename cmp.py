def compare_files(file1_path, file2_path):
    with open(file1_path, 'rb') as f1, open(file2_path, 'rb') as f2:
        while True:
            f1_chunk = f1.read(1024)
            f2_chunk = f2.read(1024)
            if f1_chunk != f2_chunk:
                return False
            if not f1_chunk:
                return True
if compare_files('lossless_h264_bill', 'report'):
    print('Files are the same')
else:
    print('Files are different')

