import os
import shutil
import errno
import sys
import string
import Foundation, objc,AppKit
import uuid

#from mod_pbxproj import XcodeProject

NSMutableDictionary = objc.lookUpClass('NSMutableDictionary')
NSMutableArray = objc.lookUpClass('NSMutableArray')
NSDictionary = objc.lookUpClass('NSDictionary')
NSArray = objc.lookUpClass('NSArray')

ProjectName = 'Example'


class ProjectFileItem:

    def __init__(self,path):
        self.path = path
        self.project = NSMutableDictionary.dictionaryWithContentsOfFile_(path)


    def save(self):
        return self.project.writeToFile_atomically_(self.path +'tst',True)

    def getFileType(fileExtentsion):
        fileTypes = {
            'app':'wrapper.application',
            'a':'archive.ar',
            'octest':'wrapper.cfbundle'
        }
        return fileTypes(fileExtentsion)

    def addLibrary(self,library):


    def addProject(self,projectFile):

        fileName = 'project.pbxproj'
        rootId = self.project.objectForKey_('rootObject')
        objects =  self.project.objectForKey_('objects')
        PBXProject = objects.objectForKey_(rootId)

        productRefGroupId = PBXProject.objectForKey_('productRefGroup')

        ProductGroupId = createId()
        ProjectRefId = createId()
        mainGroupId = PBXProject.objectForKey_('mainGroup')
        PBXGroup = objects.objectForKey_(mainGroupId)
        children = PBXGroup.objectForKey_('children')
        children.insertObject_atIndex_(ProjectRefId,0)

        projectReferencesList = PBXProject.objectForKey_('projectReferences')
        if None != projectReferencesList:
           projectReferencesList.append({'ProductGroup':ProductGroupId,'ProjectRef':ProjectRefId})
        else:
            PBXProject.setValue_forKey_([{'ProductGroup':ProductGroupId,'ProjectRef':ProjectRefId}],'projectReferences')

        fromProject = NSMutableDictionary.dictionaryWithContentsOfFile_(os.path.join(projectFile,fileName))
        fromRootId = fromProject.objectForKey_('rootObject')
        fromObjects =  fromProject.objectForKey_('objects')
        fromPBXProject = fromObjects.objectForKey_(fromRootId)
        fromProductRefGroupId = fromPBXProject.objectForKey_('productRefGroup')
        fromPBXGroup = fromObjects.objectForKey_(fromProductRefGroupId)
        children = [createId(),createId()]
        a = 0
        projectProduct = objects.objectForKey_(PBXProject.objectForKey_('targets')[0])
        dependencies = projectProduct.objectForKey_('dependencies')
        for child in fromPBXGroup.objectForKey_('children'):
            a = a +1
            PBXFileReference = fromObjects.objectForKey_(child)
            referencePath = PBXFileReference.objectForKey_('path')

            baseName = os.path.basename(referencePath)
            name = baseName.split('.')[0]
            remoteRefId = createId()
            objects.setValue_forKey_({
                                         'isa':'PBXContainerItemProxy',
                                         'containerPortal':ProjectRefId,
                                         'proxyType':'2',
                                         'remoteGlobalIDString':createId(),
                                         'remoteInfo':name,
            },remoteRefId)

            objects.setValue_forKey_({
                                            'isa':'PBXReferenceProxy',
                                            'fileType':PBXFileReference.objectForKey_('explicitFileType'),
                                            'path': referencePath,
                                            'remoteRef':remoteRefId,
                                            'sourceTree':PBXFileReference.objectForKey_('sourceTree')
                                        },children[a-1])






        objects.setValue_forKey_({
                                        'isa':'PBXGroup',
                                        'children':children,
                                        'name':'Products',
                                        'sourceTree':'<group>'
                                        },ProductGroupId)



        objects.setValue_forKey_({
                                     'isa':'PBXFileReference',
                                     'lastKnownFileType':'wrapper.pb-project',
                                     'name':os.path.basename(projectFile),
                                     'path':projectFile.replace(os.getcwd()+'/',''),
                                     'sourceTree':'<group>'


        },ProjectRefId)

        fromProductName = fromObjects.objectForKey_(fromPBXProject.objectForKey_('mainGroup')).objectForKey_('name')
        dependencyId = createId()
        if dependencies == None:
                    projectProduct.setValue_forKey_([dependencyId],'dependencies')
        else:
                    dependencies.addObject_(dependencyId)
        targetProxyId = createId()
        PBXTargetDependency = {
                    'isa':'PBXTargetDependency',
                    'name':fromProductName,
                    'targetProxy':targetProxyId}
        objects.setValue_forKey_(PBXTargetDependency,dependencyId)

        PBXContainerItemProxy = {
                    'isa':'PBXContainerItemProxy',
                    'containerPortal':ProjectRefId,
                    'proxyType':'1',
                    'remoteGlobalIDString':createId(),
                    'remoteInfo':fromProductName
        }

        objects.setValue_forKey_(PBXContainerItemProxy,targetProxyId)





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
                            print ("Could not open file! Please close Excel!")
                        else:
                            s = s.replace(ProjectName,newProjectName)
                            f = open(filePath, 'w')
                            f.write(s)
                            f.close()
                        if ProjectName+'Tests.m' in filePath:
                            os.rename(filePath,filePath.replace(ProjectName,newProjectName))



def createId():
    return ''.join(str(uuid.uuid4()).upper().split('-')[1:])



if __name__ == '__main__':

    projectItem = ProjectFileItem('/Users/virgil/Desktop/project.pbxproj')
    projectItem.addProject('/Users/virgil/Desktop/Example/Example/zxing/iphone/ZXingWidget/ZXingWidget.xcodeproj')
    projectItem.save()
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


