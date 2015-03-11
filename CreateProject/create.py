import os
import shutil
import errno
import sys
import string
from mod_pbxproj import XcodeProject


ProjectName = 'Example'

def copyDir(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
       # else:
            #raise OSError,("can't copy ,errno %d"%exc.errno)
def walkPath(arg,dirs,files):
    print(dirs)
    print(files)

def cleanPath(path,newProjectName):
      for obj in os.listdir(path):
          obj = os.path.join(path,obj)
          print('---------%s'%obj)
          if os.path.isdir(obj):
              newPath = obj.replace(ProjectName,newProjectName)
              os.rename(obj,newPath)
              print('newpath %s'%newPath)
              cleanPath(newPath,newProjectName)
          else:
                    if '.DS_Store' in obj:
                        continue
                    if 'pbxproj' in obj:
                        print('project file'+obj)
                    if '.h' in obj or '.m' in obj or '.pbxproj' in obj:
                        filePath = obj
                        try:
                            s = open(filePath).read()
                        except IOError:
                            print "Could not open file! Please close Excel!"
                        else:
                            s = s.replace(ProjectName,newProjectName)
                            f = open(filePath, 'w')
                            f.write(s)
                            f.close()
                        if ProjectName+'Tests.m' in filePath:
                            os.rename(filePath,filePath.replace(ProjectName,newProjectName))

def addZxing(projectFile):
    currentPath = os.getcwd()
    zxingDir = os.path.join(currentPath,'zxing')
    if os.path.exists(zxingDir):
         project = XcodeProject.Load(projectFile)



if __name__ == '__main__':

    project = XcodeProject.Load('/Users/virgil/Documents/python/CreateProject/testvv/testvv.xcodeproj/project.pbxproj')
    frameWork = project.get_or_create_group('framework')

    new_group = project.get_or_create_group('testvv')
    project.add_file('/Users/virgil/Desktop/te.m', parent=new_group)
    project.save()
    '''
    if len(sys.argv) > 1:
            newProjectName = sys.argv[1]
    else:
        newProjectName = 'testvv'
    currentPath = os.getcwd()
    projectDir = os.path.join(currentPath,ProjectName)
    if os.path.exists(projectDir) == False:
        print('Project File Not Exist')
    else:
        newProjectPath = os.path.join(currentPath,newProjectName)
        try:
            copyDir(projectDir,newProjectPath)
        except Exception, e:
            print (e)
        else:
            cleanPath(newProjectPath,newProjectName)
    '''


