#!/usr/bin/env python
# coding: utf-8

# ## Pick Testcases
# 
# ### Input
# 
# list of filenames : string from https: //codeforces.com /contest/xxxx/submission/xxxxx. This string should have some test details, which is in div `tests-placeholder` 
# 
# 
# ### Output
# 
# regard to the given output-directory path argument, this python script generates many files. diretory schema follows the shape described at `CppSynth/findVarErrror`'s `naiveSolution`
# 
# For invalid testcase (when the testcase input or output is too long), It ignores them.

# In[3]:


#
# INPUT OUTPUT EXAMPLES
#

### INPUT
#
# "/home/ubuntu/.../htmlfiles"   # folder. it represents the root for input files.
# - 1200    # folder. it represents the contest number
#   - A     # file. this represents the question name
#   - B
#   - C
#   - ...
# - 1202
#   - A
#   - B
#   - C
#   - D
#   - ...
# - 1203
#   - ...
# - ...

### OUTPUT
#
# "/home/ubuntu/.../testcasesOutput"   # folder. it represents the root for output files.
# - 1200
#   - A
#     - input
#       - 1.txt
#       - 2.txt
#       - ...
#     - output
#       - 1.txt
#       - ...
#   - B
#     - input
#       - ...
#     - output
#       - ...
#   - ...
# - 1202
#   - ...
# - ...


# ## CODE

# In[1]:


# import
from bs4 import BeautifulSoup
import os
import pathlib  # This module is best used with Python 3.2 or later, but it is also compatible with Python 2.6 and 2.7.


# In[2]:


# INPUT AND OUTPUT PATH NAMES
baseDir = '/home/ubuntu/workspace/pyws/getTestcases'
inputDir = os.path.join(baseDir, 'inputs')
outputDir = os.path.join(baseDir, 'outputs')


# In[3]:


# get contest list
inputContestDir = next(os.walk(inputDir))[1]


# In[4]:


# input: 
#  - html-file-handler (class '_io.TextIOWrapper')
#  - testcase-input-dirname (string)
#  - testcase-output-dirname (string)

# output: multiple values
#  - the number of generated testcase pairs (int)
#  - result code (0 for normal)
def gen_testCases(htmlf, inDir, outDir):
    htmlStr = htmlf.read()
    soup = BeautifulSoup(htmlStr, 'html.parser')
    for script in soup(["script", "style"]):
        script.extract()
    alltests = soup.find('div', 'tests-placeholder')
    inputs = alltests.find_all('pre', 'input')
    outputs = alltests.find_all('pre', 'answer')
    count = 1
    exclude_first_flag = True
    for (i, o) in zip(inputs, outputs):
        if exclude_first_flag:
            exclude_first_flag = False
            continue
        istr = i.get_text()
        ostr = o.get_text()
        if istr[-3:] == '...' or ostr[-3:] == '...':
            continue
        else:
            ifn = os.path.join(inDir, str(count))
            ofn = os.path.join(outDir, str(count))
            with open(ifn, 'w') as ifile:
                with open(ofn, 'w') as ofile:
                    ifile.write(istr)
                    ofile.write(ostr)
            count += 1
    return ((count - 1), 0)


# In[5]:


# iterate files and generate testcases

for ictDir in inputContestDir:
    ictDirFull = os.path.join(inputDir, ictDir)
    octDirFull = os.path.join(outputDir, ictDir)
    qFilenames = next(os.walk(ictDirFull))[2]
    for qFilename in qFilenames:
        qFilenameFull = os.path.join(ictDirFull, qFilename)
        with open(qFilenameFull, 'r') as qf:
            tcInDirFull = os.path.join(octDirFull, qFilename, 'input')
            tcOutDirFull = os.path.join(octDirFull, qFilename, 'output')
            pathlib.Path(tcInDirFull).mkdir(parents=True, exist_ok=True) 
            pathlib.Path(tcOutDirFull).mkdir(parents=True, exist_ok=True) 
            gen_testCases(qf, tcInDirFull, tcOutDirFull)
    print('Contest ' + str(ictDir) + ' testcases are collected.')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




