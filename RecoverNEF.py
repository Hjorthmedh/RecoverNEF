#!/usr/bin/python3
import os
import sys
import numpy as np

print("!!! Use this program at your own risk.\nIt reads in multiple copies of" \
      + " a corrupt file, and tries to create a non-corrupt version by" \
      + " doing a majority vote for each byte in the file.")

print("This code runs with Python3, not Python")
      
# You run this program with:
#
# python3 RecoverNEF.py
#
# If you have a memory card which gives you corrupted photos when you download
# them to your computer, but the corruption changes each time you download
# the file, then this program might help you.
#
# What you need to do. First, download multiple copies of the files on your
# memory card, and store them in different directories. For example you might
# download the files seven times, and store them in directories DL1, DL2, ...
# 

# Change this to the directory where you have the DL1, DL2, etc directories
basePath = "./"

# Add additional directories here if you downloaded it more times.
dirList = ["DL1","DL2","DL3","DL4","DL5","DL6"]

# This is where the rescued files will be stored
outDir = basePath + "OUT/"

# Reading the filenames in the DL1 directory
fileNames = os.listdir(basePath + dirList[0])

# Creating the OUT directory if it does not exist
if not os.path.exists(outDir):
  os.makedirs(outDir)

# This will tell you some statistics, more about it later.
nFiles = len(dirList)
voteStats = np.zeros((nFiles+1,),dtype=int)

# Change this to True if you want more information about the errors corrected
verbose = False


for fName in fileNames:
  
  fData = []

  voteStats[:] = 0

  print("Reading files:")
  for dName in dirList:
   fNameFull = basePath + dName + "/" + fName 
   print(fNameFull)
   ff = open(fNameFull,'rb')
   data = ff.read()
   ff.close()
   
   fData.append(data)

  dLen = [len(x) for x in fData]
  assert min(dLen) == max(dLen), "All data not equal length " + fName
  dLen = int(np.median(dLen))
   
  outData = bytearray()
  totErrors = 0

  bdata = np.zeros((len(fData),),dtype=np.byte)

  print("Processing " + str(fName) + " (this is a bit slow)")

  for idx in range(0,dLen):

    if(idx % 1000000 == 0):
      sys.stdout.write('.')
      sys.stdout.flush()
      
    
    bdata[:] = 0
   
    for fn in range(0,len(fData)):
      import pdb
      pdb.set_trace()
      bdata[fn] = fData[fn][idx]
           
    if((bdata == bdata[0]).all()):
      outData.append(bdata[0])
      voteStats[nFiles] += 1
    else:
    
      b = max(set(bdata), key=list(bdata).count)
      outData.append(b)
      totErrors += 1

      voteCnt = np.sum(b == bdata)
      voteStats[voteCnt] += 1

      if(verbose):
        print(fName + ": Corrected byte " + str(b) + " at position " + str(idx)\
              + ", vote count " + str(voteCnt) + "/" + str(len(fData)))
       
       
  fOutName = outDir + fName

  if(os.path.isfile(fOutName)):
    print("\n" + fOutName + " already exists," \
       + " press enter to continue, Ctrl+C to abort")
    input()
    print("Overwriting file.")
  
  with open(fOutName,'wb') as fOut:
    fOut.write(outData)

  print("\n" + fName + " total errors found: " + str(totErrors))
  voteStr = ""
  for i in range(0,len(voteStats)):
    voteStr += str(i) + ":" + str(voteStats[i]) + "  "

  print("Vote statistics: " + str(voteStr))
    
  if(np.sum(voteStats[0:int(np.ceil(nFiles/2.0)+1)]) > 0):
    print("!!! Warning, voting might be wrong. Download more copies.")
    
    
  # import pdb
  # pdb.set_trace()
