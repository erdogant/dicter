import os
from glob import glob

############### Download rst file ###############
def download_file(url_rst, filename):
    try:
    	from urllib.request import urlretrieve
    	if os.path.isfile(filename):
    		os.remove(filename)
    		print('Download %s..' %(filename))
    	urlretrieve (url_rst, filename)
    except:
    	print('Downloading %s failed.' %(url_rst))

############### Include ADD to rst files ###############
def add_includes_to_rst_files():
    for file_path in glob("*.rst"):
        with open(file_path, "r+") as file:
            contents = file.read()
            if ".. include:: add_top.add" not in contents:
                file.seek(0)
                file.write(".. include:: add_top.add\n\n" + contents)
                print('Top Add included >%s' %(file_path))

            if ".. include:: add_bottom.add" not in contents:
                file.seek(0, 2)
                file.write("\n\n.. include:: add_bottom.add")
                print('Bottom Add included >%s' %(file_path))
