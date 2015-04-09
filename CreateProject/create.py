

import os
import shutil
import errno
import sys
import string
import Foundation, objc,AppKit
import uuid
import plistlib
import inspect
import time
import getpass

if sys.version_info[0] < 3:
   reload(sys)
   sys.setdefaultencoding('utf8')

#from mod_pbxproj import XcodeProject

NSMutableDictionary = objc.lookUpClass('NSMutableDictionary')
NSMutableArray = objc.lookUpClass('NSMutableArray')
NSDictionary = objc.lookUpClass('NSDictionary')
NSArray = objc.lookUpClass('NSArray')

ProjectName = 'Example'
NewProjectName  = ''
NewProjectDir = ''

SourceFileExtension = ['c','m','mm']
ResourceExtension = ['png','jpg','jpeg','js','html','shtml','hml','json','sh']
FrameWorkExtension = ['a','framewrok','dylib']

class BuildPhaseType:
     Sources = 'PBXSourcesBuildPhase'
     Frameworks = 'PBXFrameworksBuildPhase'
     Resources = 'PBXResourcesBuildPhase'



class ProjectFileItem:

    def __init__(self,path):
        self.path = path
        self.project = NSMutableDictionary.dictionaryWithContentsOfFile_(path)
        self.rootId = self.project.objectForKey_('rootObject')
        self.objects =  self.project.objectForKey_('objects')
        self.PBXProject = self.objects.objectForKey_(self.rootId)
        self.projectProduct = self.objects.objectForKey_(self.PBXProject.objectForKey_('targets')[0])

    def save(self):
        return self.project.writeToFile_atomically_(self.path,True)

    def reload(self):
        self.project = NSMutableDictionary.dictionaryWithContentsOfFile_(self.path)

    def getBuildPhase(self,type):
        buildPhases = self.projectProduct.objectForKey_('buildPhases')
        for buildPhaseId in buildPhases:
            buildPhase = self.objects.objectForKey_(buildPhaseId)
            if buildPhase.objectForKey_('isa') == type:
                return buildPhase
        return None

    def buildPhaseAddFile(self,buildPhaseType,fileReferenceId):
        if buildPhaseType != None:
           PBXBuildFileId = createId()
           buildPhase = self.getBuildPhase(buildPhaseType)
           files = buildPhase.objectForKey_('files')
           for fileId in files:
               file = self.objects.objectForKey_(fileId)
               if file.objectForKey_('fileRef') == fileReferenceId:
                   return fileReferenceId
           if None == files:
              PBXBuildFileIdArray = NSMutableArray.array()
              PBXBuildFileIdArray.addObject_(PBXBuildFileId)
              buildPhase.setValue_forKey_(PBXBuildFileIdArray,'files')
           else:
               files.addObject_(PBXBuildFileId)
               buildPhase.setValue_forKey_(files,'files')
           self.objects.setValue_forKey_(createDict({
                                                 'isa':'PBXBuildFile',
                                                 'fileRef':fileReferenceId,
                                             }),PBXBuildFileId,)
           return PBXBuildFileId
        return None

    def getFileExtention(self,path):
        return  os.path.basename(path).split('.')[-1]

    def getLastKnowFileType(self,path):
        extention = self.getFileExtention(path)

        types = {
            'h':'sourcecode.c.h',
            'm':'sourcecode.c.objc',
            'dylib':'compiled.mach-o.dylib',
            'framework':'wrapper.framework',
            'png':'image.png',
            'sh':'text.script.sh',
            'a':'archive.ar',
            'jpeg':'image.jpeg',
            'jpg':'image.jpeg',
            'mm':'sourcecode.cpp.objcpp',
            }
        if extention in types:
           return types[extention]
        else:
            return None

    def getBuildSetting(self,Debug = True):
        buildConfigurationListId = self.projectProduct.objectForKey_('buildConfigurationList')
        buildConfigurationList = self.objects.objectForKey_(buildConfigurationListId)
        buildConfigurations = buildConfigurationList.objectForKey_('buildConfigurations')
        for buildConfigurationId in buildConfigurations:
            buildConfiguration = self.objects.objectForKey_(buildConfigurationId)
            if buildConfiguration.objectForKey_('name') == 'Debug' and Debug:
                return buildConfiguration
            if buildConfiguration.objectForKey_('name') == 'Release' and Debug == False:
               return buildConfiguration
        return None

    def addHeaderSearchPath(self,path):
        if path != None:
             buildConfigurationListId = self.projectProduct.objectForKey_('buildConfigurationList')
             buildConfigurationList = self.objects.objectForKey_(buildConfigurationListId)
             buildConfigurations = buildConfigurationList.objectForKey_('buildConfigurations')
             for buildConfigurationId in buildConfigurations:
                buildConfiguration = self.objects.objectForKey_(buildConfigurationId)
                buildSettings = buildConfiguration.objectForKey_('buildSettings')
                headers = buildSettings.objectForKey_('HEADER_SEARCH_PATHS')
                if headers == None:
                    headers = NSMutableArray.array()
                    headers.addObject_('"$(inherited)"')
                    headers.addObject_('/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/include')
                    buildSettings.setValue_forKey_(headers,'HEADER_SEARCH_PATHS')
                headers.addObject_(path)

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
               children = NSMutableArray.array()
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
                groupChildren = NSMutableArray.array()
                children.addObject_(groupId)
                objects.setValue_forKey_(
                    createDict({
                        'isa':'PBXGroup',
                        'children':groupChildren,
                        'name':groupName,
                        'sourceTree':'<group>'}),groupId)
            else:
                group = objects.objectForKey_(groupId)
                groupChildren = group.objectForKey_('children')


        if systemLibrary:
           lastKnowFileType = self.getLastKnowFileType(library)
           libraryDir =   None
           if '.dylib' in library:
                    libraryDir =  'usr/lib/'
           else:
                   libraryDir = 'System/Library/Frameworks/'
           for childId in groupChildren:
               child = objects.objectForKey_(childId)
               if child.objectForKey_('lastKnownFileType') == lastKnowFileType  and child.objectForKey_('name') == library:
                      FileReferenceId = childId
                      break

           if FileReferenceId == None:
               FileReferenceId = createId()
               objects.setValue_forKey_(
                   createDict({
                       'isa':'PBXFileReference',
                       'lastKnownFileType':lastKnowFileType,
                       'name':library,
                       'path':os.path.join(libraryDir,library),
                       'sourceTree':'SDKROOT'
                    }),FileReferenceId)
           if groupChildren != None:

               if groupChildren.containsObject_(FileReferenceId) == False:
                  groupChildren.addObject_(FileReferenceId)
           else:
               children.addObject_(FileReferenceId)



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
           self.buildPhaseAddFile(BuildPhaseType.Frameworks,FileReferenceId)

    def addLibrarySearchPath(self,path):
        if path != None:
             buildConfigurationListId = self.projectProduct.objectForKey_('buildConfigurationList')
             buildConfigurationList = self.objects.objectForKey_(buildConfigurationListId)
             buildConfigurations = buildConfigurationList.objectForKey_('buildConfigurations')
             for buildConfigurationId in buildConfigurations:
                buildConfiguration = self.objects.objectForKey_(buildConfigurationId)
                buildSettings = buildConfiguration.objectForKey_('buildSettings')
                paths = buildSettings.objectForKey_('LIBRARY_SEARCH_PATHS')
                if paths == None:
                    paths = NSMutableArray.array()
                    paths.addObject_('"$(inherited)",')
                    buildSettings.setValue_forKey_(paths,'LIBRARY_SEARCH_PATHS')
                tmpPath = path.replace(NewProjectDir,'')
                tmpPath = os.path.dirname(tmpPath)
                paths.addObject_('$(PROJECT_DIR)'+tmpPath)


    def addFile(self,path,Group = None):
        if Group == None:
           print('no group')
        else:
            lastKnowFileType = self.getLastKnowFileType(path)
            if lastKnowFileType == None:
                return
            itemId = createId()
            children = Group.objectForKey_('children')
            children.addObject_(itemId)
            extension = self.getFileExtention(path)
            if extension in SourceFileExtension:
               self.objects.setValue_forKey_(createDict({
                                         'isa':'PBXFileReference',
                                         'fileEncoding':'4',
                                         'lastKnownFileType':lastKnowFileType,
                                         'path':os.path.basename(path),
                                         'sourceTree':'<group>'
                                         }),itemId)
               self.buildPhaseAddFile(BuildPhaseType.Sources,itemId)

            elif extension in ResourceExtension:
                self.objects.setValue_forKey_(createDict({
                    'isa':'PBXFileReference',
                    'lastKnownFileType':lastKnowFileType,
                    'path':os.path.basename(path),
                    'sourceTree':'<group>'
                    }),itemId)
                self.buildPhaseAddFile(BuildPhaseType.Resources,itemId)

            elif extension in FrameWorkExtension:
                 self.objects.setValue_forKey_(createDict({
                                         'isa':'PBXFileReference',
                                         'lastKnownFileType':lastKnowFileType,
                                         'path':os.path.basename(path),
                                         'sourceTree':'<group>'
                                         }),itemId)
                 self.buildPhaseAddFile(BuildPhaseType.Frameworks,itemId)
                 self.addLibrarySearchPath(path)

            else:
                 self.objects.setValue_forKey_(createDict({
                                         'isa':'PBXFileReference',
                                         'fileEncoding':'4',
                                         'lastKnownFileType':lastKnowFileType,
                                         'path':os.path.basename(path),
                                         'sourceTree':'<group>'
                                         }),itemId)



    def addDir(self,dir,groupName = 'Source',Group = None):
        if os.path.isdir(dir) == False:
            return
        if Group == None:
           mainGroupId = self.PBXProject.objectForKey_('mainGroup')
           mainGroup = self.objects.objectForKey_(mainGroupId)
           children = mainGroup.objectForKey_('children')
           projectGroupId = None
           for groupId  in children:
               tmpGroup = self.objects.objectForKey_(groupId)
               if tmpGroup.objectForKey_('path') == NewProjectName:
                   projectGroupId = groupId
                   break
           if projectGroupId == None:
               return
           projectGroup = self.objects.objectForKey_(projectGroupId)
           for childId in projectGroup.objectForKey_('children'):
               child = self.objects.objectForKey_(childId)
               if child.objectForKey_('path') == groupName:
                   Group = child
                   break
        if Group == None:
            return
        PBXGroupId = createId()
        subChildren = Group.objectForKey_('children')
        subChildren.append(PBXGroupId)
        items = NSMutableArray.array()
        currentGroup = NSMutableDictionary.dictionary()
        currentGroup.setValue_forKey_('PBXGroup','isa')
        currentGroup.setValue_forKey_(items,'children')
        currentGroup.setValue_forKey_(os.path.basename(dir),'path')
        currentGroup.setValue_forKey_('<group>','sourceTree')


        for obj in os.listdir(dir):
            obj = os.path.join(dir,obj)
            if 'DS_Store' in obj:
               continue
            if os.path.isdir(obj):
               self.addDir(obj,os.path.basename(dir),Group = currentGroup)
            else:
               self.addFile(obj,Group = currentGroup)
        self.objects.setValue_forKey_(currentGroup,PBXGroupId)




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
        children.addObject_(ProjectRefId)

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

        name = ''

        for targetId in fromPBXProject.objectForKey_('targets'):

            tmpObject = fromObjects.objectForKey_(targetId)
            if tmpObject.objectForKey_('productType') == 'com.apple.product-type.library.static':
                name = tmpObject.objectForKey_('name')
                break

        children = NSMutableArray.array()
        children.addObject_(createId())
        children.addObject_(createId())
        a = 0
        projectProduct = objects.objectForKey_(PBXProject.objectForKey_('targets')[0])
        dependencies = projectProduct.objectForKey_('dependencies')
        for child in fromPBXGroup.objectForKey_('children'):
            a = a +1
            PBXFileReference = fromObjects.objectForKey_(child)
            referencePath = PBXFileReference.objectForKey_('path')
            remoteRefId = createId()
            objects.setValue_forKey_(createDict({
                                         'isa':'PBXContainerItemProxy',
                                         'containerPortal':ProjectRefId,
                                         'proxyType':'2',
                                         'remoteGlobalIDString':createId(),
                                         'remoteInfo':'ZXingWidget',
            }),remoteRefId)

            objects.setValue_forKey_(createDict({
                                            'isa':'PBXReferenceProxy',
                                            'fileType':PBXFileReference.objectForKey_('explicitFileType'),
                                            'path': referencePath,
                                            'remoteRef':remoteRefId,
                                            'sourceTree':PBXFileReference.objectForKey_('sourceTree')
                                        }),children.objectAtIndex_(a-1))
            if self.getFileExtention(referencePath) in FrameWorkExtension:
                self.buildPhaseAddFile(BuildPhaseType.Frameworks,children.objectAtIndex_(a-1))

        objects.setValue_forKey_(createDict({
                                        'isa':'PBXGroup',
                                        'children':children,
                                        'name':'Products',
                                        'sourceTree':'<group>'
                                        }),ProductGroupId)



        objects.setValue_forKey_(createDict({
                                     'isa':'PBXFileReference',
                                     'lastKnownFileType':'wrapper.pb-project',
                                     'name':os.path.basename(projectFile),
                                     'path':projectFile.replace(os.path.dirname(inspect.getfile(inspect.currentframe()))+'/',''),
                                     'sourceTree':'<group>'


        }),ProjectRefId)

        fromProductName = fromObjects.objectForKey_(fromPBXProject.objectForKey_('mainGroup')).objectForKey_('name')
        dependencyId = createId()
        if dependencies == None:
                    dependencyArray = NSMutableArray.array()
                    dependencyArray.addObject(dependencyId)
                    projectProduct.setValue_forKey_(dependencyArray,'dependencies')
        else:
                    dependencies.addObject_(dependencyId)
        targetProxyId = createId()
        PBXTargetDependency = {
                    'isa':'PBXTargetDependency',
                    'name':fromProductName,
                    'targetProxy':targetProxyId}
        PBXTargetDependency = createDict(PBXTargetDependency)
        objects.setValue_forKey_(PBXTargetDependency,dependencyId)

        PBXContainerItemProxy = {
                    'isa':'PBXContainerItemProxy',
                    'containerPortal':ProjectRefId,
                    'proxyType':'1',
                    'remoteGlobalIDString':createId(),
                    'remoteInfo':fromProductName
        }
        PBXContainerItemProxy = createDict(PBXContainerItemProxy)

        objects.setValue_forKey_(PBXContainerItemProxy,targetProxyId)

def createDict(dict):
    ocDict = NSMutableDictionary.dictionary()
    for key in dict:
        ocDict.setValue_forKey_(dict[key],key)
    return ocDict


def copyDir(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)

def today():
        now = time.localtime(time.time())
        year = time.strftime('%y',now)
        month = time.strftime('%m',now)
        day = time.strftime('%d',now)
        return year+'-'+month+'-'+day

def cleanPath(path,newProjectName):
      for obj in os.listdir(path):
          obj = os.path.join(path,obj)
          if os.path.isdir(obj):
              newPath = obj.replace(ProjectName,newProjectName)
              os.rename(obj,newPath)
              cleanPath(newPath,newProjectName)
          else:
                    if '.DS_Store' in obj:
                        continue
                    if '.h' in obj or '.m' in obj or '.pbxproj' in obj:
                        filePath = obj
                        try:
                            s = open(filePath).read()
                        except IOError:
                            print ("Could not open file! Please close !")
                        else:
                            s = s.replace(ProjectName,newProjectName)
                            s = s.replace('virgil',getpass.getuser())
                            s = s.replace('6/3/15',today())
                            f = open(filePath, 'w')
                            f.write(s)
                            f.close()
                        if ProjectName+'Tests.m' in filePath:
                            os.rename(filePath,filePath.replace(ProjectName,newProjectName))



def createId():
    return ''.join(str(uuid.uuid4()).upper().split('-')[1:])

def raiseException(exception):
    if sys.version_info[0] < 3:
       raise OSError(exception)
    else:
       raise OSError(exception)

if __name__ == '__main__':
    configPath = os.path.join(os.path.dirname(inspect.getfile(inspect.currentframe())),'config.plist')
    config = NSMutableDictionary.dictionaryWithContentsOfFile_(configPath)
    NewProjectName = config.objectForKey_('name')
    path = config.objectForKey_('path')
    if os.path.exists(path) == False or os.path.isfile(path):
         raiseException('%s not accept'%path)

    currentPath = os.path.dirname(inspect.getfile(inspect.currentframe()))
    projectDir = os.path.join(currentPath,ProjectName)
    if os.path.exists(projectDir) == False:
         raiseException(NewProjectName + '  already exist')

    else:
        NewProjectDir = os.path.join(path,NewProjectName)
        if os.path.exists(NewProjectDir):
            if sys.version_info[0] < 3:
               raise OSError (NewProjectName + '  already exist')
            else:
                raise OSError(NewProjectName + '  already exist')
        try:
            copyDir(projectDir,NewProjectDir)

        except e:
            print (e)

        else:
            cleanPath(NewProjectDir,NewProjectName)

        projectFilePath = os.path.join(NewProjectDir,'%s.xcodeproj/project.pbxproj'%(NewProjectName))
        if  os.path.exists(projectFilePath) == False:
            print ('project file not exist')
        else:
            projectItem = ProjectFileItem(projectFilePath)
            projectConfig = config.objectForKey_('config')
            bundleId = config.objectForKey_('CFBundleIdentifier')
            frameworkConfig = config.objectForKey_('frameworkConfig')
            headrSearchPathConfig = config.objectForKey_('headerSearchPathConfig')

            infoPlistPath = os.path.join(NewProjectDir,('%s/Info.plist'%NewProjectName))
            print(infoPlistPath)
            if bundleId != None and os.path.exists(infoPlistPath):
               info = NSMutableDictionary.dictionaryWithContentsOfFile_(infoPlistPath)
               info.setValue_forKey_(bundleId,'CFBundleIdentifier')
               info.writeToFile_atomically_(infoPlistPath,True)
            for  key in projectConfig.allKeys():
                 if key == 'zxing':
                   if True == projectConfig.objectForKey_(key):
                      print('----------------------')
                      print('add   '+key)
                      zxingDir = os.path.dirname(inspect.getfile(inspect.currentframe()))+'/zxing'
                      newZxingDir = os.path.join(NewProjectDir,'zxing')
                      copyDir(zxingDir,newZxingDir)
                      zxingPath = os.path.join(newZxingDir,'iphone/ZXingWidget/ZXingWidget.xcodeproj')
                      projectItem.addProject(zxingPath)
                 else:
                      dir =os.path.join(os.path.dirname(inspect.getfile(inspect.currentframe())),key)
                      if  os.path.isdir(dir) and os.path.exists(dir) and True == projectConfig.objectForKey_(key):
                          print('----------------------')
                          print('add  ' + key)
                          newDir = os.path.join(NewProjectDir,('%s/Source/%s'%(NewProjectName,key)))
                          copyDir(dir,newDir)
                          projectItem.addDir(newDir)

                 if True == projectConfig.objectForKey_(key):
                     unitFrameworks = frameworkConfig.objectForKey_(key)
                     if unitFrameworks != None:
                        for framework in unitFrameworks:
                            projectItem.addLibrary(framework,True,'Framework')
                     unitHeadrSearchPaths = headrSearchPathConfig.objectForKey_(key)
                     if  unitHeadrSearchPaths != None:
                         for headerSearchPath in unitHeadrSearchPaths:
                             projectItem.addHeaderSearchPath(headerSearchPath)


            projectItem.save()
            print('Finish')

