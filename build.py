#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
from ftplib import  FTP
import Foundation, objc,AppKit
import time

#默认的工程文件所在文件夹，也可以在命令行里设置
DefaultProjectDir = "/Users/virgil/Documents/Epub1/epub.xcodeproj"

#ipa 文件输出的文件夹
OutPutDir = "/Users/virgil/Desktop/"

#FTP 设置
FTPServer = "10.38.178.77"
Port = "21"
UploadDir ="/Fred/"

IPA_Extentsion = ".ipa"
ProjectExtentsion =".xcodeproj"
ProjectFileName = "project.pbxproj"

NSUserNotification = objc.lookUpClass('NSUserNotification')
NSUserNotificationCenter = objc.lookUpClass('NSUserNotificationCenter')
NSDictionary = objc.lookUpClass('NSDictionary')
NSPasteboard = objc.lookUpClass('NSPasteboard')

def notify(title, subtitle, info_text, delay=0, sound=False, userInfo={}):
  """ Python method to show a desktop notification on Mountain Lion. Where:
        title: Title of notification
        subtitle: Subtitle of notification
        info_text: Informative text of notification
        delay: Delay (in seconds) before showing the notification
        sound: Play the default notification sound
        userInfo: a dictionary that can be used to handle clicks in your
                  app's applicationDidFinishLaunching:aNotification method
  """
  notification = NSUserNotification.alloc().init()
  notification.setTitle_(title)
  notification.setSubtitle_(subtitle)
  notification.setInformativeText_(info_text)
  notification.setUserInfo_(userInfo)
  if sound:
    notification.setSoundName_("NSUserNotificationDefaultSoundName")
  notification.setDeliveryDate_(Foundation.NSDate.dateWithTimeInterval_sinceDate_(delay, Foundation.NSDate.date()))
  NSUserNotificationCenter.defaultUserNotificationCenter().scheduleNotification_(notification)

def parseProject(path):
     projectFile = ""
     if os.path.exists(path) ==False:
         log("%s 不存在"%path)
         return []
     if  os.path.splitext(path)[1] == ProjectExtentsion:
         projectFile = os.path.join(path,ProjectFileName)
     else:
         for file in  os.listdir(path):
             extentsion =  os.path.splitext(file)[1]
             if extentsion == ProjectExtentsion:
                projectFile = file
                break;
         if len(projectFile)==0:
            log("没有找到.xcodeproj文件")
            return []
         projectFile = os.path.join(path,projectFile,ProjectFileName)
         if  os.path.exists(projectFile) == False:
             log("没有找到.xcodeproj文件")
             return []
     project = NSDictionary.dictionaryWithContentsOfFile_(projectFile)
     rootKey = project.objectForKey_("rootObject")
     objects = project.objectForKey_("objects")
     rootObject = objects.objectForKey_(rootKey)
     targets = rootObject.objectForKey_("targets")
     count = targets.count()
     AllTarget =[]
     for a in range(0,count):
         tartgetKey = targets.objectAtIndex_(a)
         target = objects.objectForKey_(tartgetKey)
         if target.objectForKey_("productType") == "com.apple.product-type.application":
             targetName = target.objectForKey_("name")
             configKey = target.objectForKey_("buildConfigurationList")
             config = objects.objectForKey_(configKey)
             releaseConfigKey = findReleaseConfi(config,objects)
             releaseConfig = objects.objectForKey_(releaseConfigKey)
             setting = releaseConfig.objectForKey_("buildSettings")
             productName= setting.objectForKey_("PRODUCT_NAME")
             if productName == "$(TARGET_NAME)":
                productName = targetName
             AllTarget.append([targetName,productName])
     return AllTarget


def findReleaseConfi(config,allObject):
    configs = config.objectForKey_("buildConfigurations")
    count = configs.count()
    for a in range (0,count):
        configKey = configs.objectAtIndex_(a)
        configObject = allObject.objectForKey_(configKey)
        if configObject.objectForKey_("name")=="Release":
            return configKey

def today():
    today = time.strftime('.%m.%d',time.localtime(time.time()))
    return today

def ipaName(outPutDir,prodocutName):
    date = today()
    name = prodocutName+date+IPA_Extentsion
    if os.path.exists(outPutDir+name):
        a = 2
        name=prodocutName+today()+".%02d"%a+IPA_Extentsion
        while os.path.exists(outPutDir+name):
            a=a+1
            name = prodocutName+date+".%02d"%a+IPA_Extentsion
    return name

def run_main(PROJDIR):
        if os.path.exists(PROJDIR) == False:
            log("%s不存在"%PROJDIR)
            return
        dir = PROJDIR
        if os.path.splitext(dir)[1] == ProjectExtentsion:
            dir = os.path.dirname(dir)
        os.chdir(dir)
        targets = parseProject(PROJDIR)
        targetCount = len(targets)
        for a in range(0,targetCount):
            target = targets[a]
            targetName = target[0]
            prodoctName = target[1]

            log("clean target %s"%targetName)
            clean_command ="xcodebuild -target " + targetName +" clean"
            os.system(clean_command)

            log("build target %s"%targetName)
            build_app_command = "xcodebuild -target " + targetName + " -sdk " \
                            + "iphoneos" + " -configuration Release"
            os.system(build_app_command)

            log("zip ipa %s"%prodoctName)
            IPA_Name = ipaName(OutPutDir,prodoctName)
            OutPutPath = OutPutDir + IPA_Name
            build_ipa_command = " ".join(
                ("/usr/bin/xcrun -sdk iphoneos PackageApplication -v",
                 os.path.join(dir,"build/Release-iphoneos/"+prodoctName+".app")+ " -o",
                 OutPutPath
                )
            )
            print build_ipa_command
            print "************************"
            os.system(build_ipa_command)
            print "*************************"
            print build_ipa_command

            log("FTP Trans")
            ftp=FTP()
            ftp.set_debuglevel(2)
            ftp.connect(FTPServer,Port)
            ftp.login()
            ftp.cwd(UploadDir)
            ftp.storbinary("stor "+IPA_Name,open(OutPutPath,"rb"))
            print("############################")
            url = "ftp:"+FTPServer+UploadDir+IPA_Name
            print url
            pasteboard = NSPasteboard.generalPasteboard()
            pasteboard.clearContents()
            pasteboard.writeObjects_([url])
            notify("IPA build finish", IPA_Name, url, userInfo={"action":"open_url", "value":url})

def log(string):
    print "*************************"
    print string
    print "*************************"

if __name__ == "__main__":
        path = DefaultProjectDir
        if len(sys.argv) > 1:
            path = sys.argv[1]
        run_main(path)
