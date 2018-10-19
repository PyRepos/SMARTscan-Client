import os
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
# Function definition for data processing

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

def ZipAllFile(directory): 
    '''Zip all file frm a directory, parent directory'''
    zf = zipfile.ZipFile('projectname.zip','w',zipfile.ZIP_DEFLATED)
    file_paths = [] 
    os.chdir(directory)
    files = glob.glob("*")
    # crawling through directory and subdirectories 
    for root, dirs, files in os.walk(directory):
        for file in files:
            zf.write(os.path.join(root, file))
    zf.close()

# ########################################################################
# Main function to implement program
# List all the image sources from the directory

# GPR images
#imgFd = os.path.join(GetWorkPath(),'2-Image')
#UploadFileToFTP(ImgFd, '2-Image')

# Photos
#phoFd = os.path.join(GetWorkPath(),'3-Photo')
#UploadFileToFTP(phoFd, '3-Photo')

# Reports
#repFd = os.path.join(GetWorkPath(),'4-Report')
#UploadFileToFTP(repFd, '4-Report')



