import os
import shutil
import errno
import sys
import string
import Foundation, objc,AppKit
import uuid
import plistlib

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
        return self.project.writeToFile_atomically_(self.path,True)

    def reload(self):
        self.project = NSMutableDictionary.dictionaryWithContentsOfFile_(self.path)


    def addLibrary(self,library,systemLibrary = False,groupName = None):
        rootId = self.project.objectForKey_('rootObject')
        objects =  self.project.objectForKey_('objects')
        PBXProject = objects.objectForKey_(rootId)
        projectProduct = objects.objectForKey_(PBXProject.objectForKey_('targets')[0])
        buildPhases = projectProduct.objectForKey_('buildPhases')

        FileReferenceId = None
        mainGroupId = PBXProject.objectForKey_('mainGroup')
        mainGroup = objects.objectForKey_(mainGroupId)
        children = mainGroup.objectForKey_('children')
        if children == None:
               children = []
               mainGroup.setValue_forKey_(children,'children')
        groupChildren = None
        if groupName != None:
            groupId = None
            for childId in mainGroup.objectForKey_('children'):
                child = objects.objectForKey_(childId)
                isa = child.objectForKey_('isa')
                if isa == 'PBXGroup' and child.objectForKey_('name') == groupName:
                    groupId = childId
                    break
            if groupId == None:
                groupId = createId()
                groupChildren = []
                children.append(groupId)
                objects.setValue_forKey_(
                    {
                        'isa':'PBXGroup',
                        'children':groupChildren,
                        'name':groupName,
                        'sourceTree':'<group>'},groupId)
            else:
                group = objects.objectForKey_(groupId)
                groupChildren = group.objectForKey_('children')


        if systemLibrary:

           for childId in mainGroup.objectForKey_('children'):
               child = objects.objectForKey_(childId)
               lastKnowFileType = None
               libraryDir =   None
               if '.dylib' in library:
                    lastKnowFileType = 'compiled.mach-o.dylib'
                    libraryDir =  'usr/lib/'
               else:
                   lastKnowFileType = 'wrapper.framework'
                   libraryDir = 'System/Library/Frameworks/'
               if child.objectForKey_('lastKnownFileType') == lastKnowFileType  and child.objectForKey_('name') == library:
                   FileReferenceId = childId
                   break
           if FileReferenceId == None:
               FileReferenceId = createId()
               objects.setValue_forKey_(
                   {
                       'isa':'PBXFileReference',
                       'lastKnownFileType':lastKnowFileType,
                       'name':library,
                       'path':os.path.join(libraryDir,library),
                       'sourceTree':'SDKROOT'
                    },FileReferenceId)
           if groupChildren != None:
               groupChildren.append(FileReferenceId)
           else:
               children.append(FileReferenceId)


        else:
            keys = objects.allKeys()
            count = keys.count()

            for a in range(0,count -1):
                key = keys[a]
                object = objects.objectForKey_(key)
                path = ''
                if object and isinstance(object,dict):
                    try:
                        path = object['path']
                    except:
                        continue
                else:
                    path = object.objectForKey_('path')

                if None == path:
                    continue
                if path == library:
                    FileReferenceId = key
                    break

        if FileReferenceId != None:
           for buildPhaseId in buildPhases:
                       buildPhase = objects.objectForKey_(buildPhaseId)
                       if buildPhase.objectForKey_('isa') == 'PBXFrameworksBuildPhase':
                          PBXBuildFileId = createId()

                          files = buildPhase.objectForKey_('files')

                          if None == files:
                             buildPhase.setValue_forKey_([PBXBuildFileId],'files')
                          else:
                              files.addObject_(PBXBuildFileId)
                              buildPhase.setValue_forKey_(files,'files')

                          objects.setValue_forKey_({
                                                 'isa':'PBXBuildFile',
                                                 'fileRef':FileReferenceId,
                                             },PBXBuildFileId,)
                          break


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
    #projectItem.addProject('/Users/virgil/Documents/python/CreateProject/zxing/iphone/ZXingWidget/ZXingWidget.xcodeproj')
    projectItem.addLibrary('libxml2.dylib',True,'framework')
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


