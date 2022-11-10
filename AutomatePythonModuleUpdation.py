import os
import subprocess
import pandas as pd
import pyperclip as pc

# running the command in background in 
# python child process to list outdated modules

values = subprocess.run('pip list --outdated', capture_output=True)

# converting the captured output 
# from binary to utf-8 format

Outdated_packages = values.stdout.decode('UTF-8')

# since the captured output is in string copying 
# it helps so that it can be converted into dataframe
pc.copy(Outdated_packages)

Outdated_packages_clip = pd.read_clipboard()

# array to store modules which are not updated
modules_not_updated = list()

# array to store modules which are updated
modules_updated = list()

# traverses through each row of data frame 
# takes one package at a time and updates it .
for ind in Outdated_packages_clip.index:
    package = 'pip install -U {}'.format(Outdated_packages_clip['Package'][ind])
    try:
        subprocess.run(package, capture_output=True)
        modules_updated.append(Outdated_packages_clip['Package'][ind])
        print(package)
    except Exception as e:
        modules_not_updated.append({"Package": Outdated_packages_clip['Package'][ind], "error": Exception})
        
        

if len(modules_not_updated) != 0:
    # stores the array of json objects which contains packages 
    #which are not updated and the exception occurred in
    # file so that since it will require human intervention for updation

    if os.path.isfile('modules_not_updated.txt'):
        with open('modules_not_updated.txt', 'a') as f:
            f.write(str(modules_not_updated))
            f.close()
    else:
        with open('modules_not_updated.txt', 'x') as f:
            f.write(str(modules_not_updated))
            f.close()
else:
    # after successful updates code stores the array of modules 
    #which are updated into module_updated file so that
    # user can go through the list of modules which are updated
    print("all the modules were updated successfully")
    if os.path.isfile('modules_updated.txt'):
        with open('modules_updated.txt', 'a') as f:
            f.write(str(modules_updated))
            f.close()
    else:
        with open('modules_updated.txt', 'x') as f:
            f.write(str(modules_updated))
            f.close()


