'''This is a script to assist data processing for SMARTscan field engineers'''
import os
import sys
import ftplib
import glob
import zipfile
from PIL import Image

# #######################################################################
# Configuration of all parameters 
ClientConfig = {
    'host' : '185.66.115.194',
    'user' : 'carnell',
    'passwd' : 'iFd_u163',
    'remote' : '/SMARTproject'
    }

# #######################################################################
# Function definitions for data processing

def GetWorkPath():
    '''Get working path for python to recognise data'''
    workingdirt = os.path.dirname(os.getcwd())
    return workingdirt

def CheckDirectory(workDict):
    '''Check if all required directories exist'''
    imageFd = os.path.join(workingdirt,"2-Image")
    photoFd = os.path.join(workingdirt,"3-Photo")
    repotFd = os.path.join(workingdirt,"4-Report")

    #Check for each and output result
    if ((os.path.isdir(imgeFd)) and (os.path.isdir(photoFd)) and (os.path.isdir(repotFd))):
        return True
    else:
        return False

def ResizeImages(imageDict):
    '''Reize all images in the folder'''
    os.chdir(imageDict)
    imgs = glob.glob("*.jpg")
    for img in imgs:
        imgIns = Image.open(img)
        size = 300, 300
        try:
            imgIns.thumbnail(size, Image.ANTIALIAS)
            imgIns.save(img)
            print "Images '%s' have been resized" %imgIns
        except IOError:
            print "Cannot resize image for '%s'" %imgIns

def UploadFileToFTP(origDir, remoteDir):
    '''Connect to the file server with user account and upload data'''
    ftpIns = ftplib.FTP(host=ClientConfig['host'])
    ftpIns.login(user=ClientConfig['user'], passwd=ClientConfig['passwd'])
    remoteFd = ClientConfig['remote']+"/"+ remoteDir
    ftpIns.mkd(remoteFd)
    ftpIns.cwd(remoteFd)

    # Retrieve all data on local machine
    os.chdir(origDir)
    imgs = glob.glob("*")
    for img in imgs:
            file = open(img,'r')
            ftpIns.storbinary('STOR ' + img, file)    
            print "File '%s' Upload succesful!" %img
            file.close()
    ftpIns.close()

def ZipAllFile(InputPath, outputPath): 
    '''Zip all file frm a directory, parent directory'''
    parent_folder = os.path.dirname(InputPath)
    contents = os.walk(parent_folder)
    zip_file = zipfile.ZipFile(outputPath,'w', zipfile.ZIP_DEFLATED)
    try:
        for root, folders, allfiles in contents:
            # Add all directories to zipfile without parent directory tree
            for folderName in folders:
                if (folderName == "2-Image" or folderName == "3-Photo" or folderName == "4-Report"):
                    absolute_path = os.path.join(root, folderName)
                    relative_path = absolute_path.replace(parent_folder + '\\','')
                    print "Adding '%s' to directory archive." % absolute_path
                    zip_file.write(absolute_path, relative_path)

                    #write files to zip file
                    os.chdir(absolute_path)
                    files = os.listdir(absolute_path)
                    for file in files:
                        filePath = os.path.join(absolute_path,file)
                        zip_file.write(filePath, relative_path+ '\\' + file)
                        print "Adding '%s' file to archive." % filePath
    
        print "'%s' created successfully." % outputPath
    except IOError, message:
        print message
        sys.exit(1)
    except OSError, message:
        print message
        sys.exit(1)
    except zipfile.BadZipfile, message:
        print message
        sys.exit(1)
    finally:
        zip_file.close()

#################################################################################

zipfilepath = os.path.join(os.getcwd(),'sample1.zip')
ZipAllFile(os.getcwd(),zipfilepath)

