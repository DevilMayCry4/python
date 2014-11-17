#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
from ftplib import  FTP
import Foundation, objc

PROJDIR = "/Users/virgil/Documents/HKDeals7/"
OutPut = "/Users/virgil/Desktop/"
SIGN_NAME = "iPhone Distribution: Guangzhou Yuncheng Information Technology Co., Ltd./"
EMBED = "/Users/virgil/Desktop/iOS_Provisioning_Profile.mobileprovision"
TARGET_NAME = "HKDeals"

TARGET_SDK = "iphoneos"
ipa_name ="Test.11.17"
PROJECT_BUILDDIR = PROJDIR + "build/Release-iphoneos/"
FTPServer = "10.38.178.77"
Port = "21"
UploadDir ="/Fred/"

NSUserNotification = objc.lookUpClass('NSUserNotification')
NSUserNotificationCenter = objc.lookUpClass('NSUserNotificationCenter')


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

def run_main(read_file):
        os.chdir(PROJDIR)
        build_app_command = "xcodebuild -target " + TARGET_NAME + " -sdk " \
                            + TARGET_SDK + " -configuration Release"
        os.system(build_app_command)
        print "*************************"
        print "build app"+ ipa_name
        print "*************************"
        OutPutPath = OutPut + ipa_name.rstrip()+".ipa"
        build_ipa_command = " ".join(
            ("/usr/bin/xcrun -sdk iphoneos PackageApplication -v",
            PROJECT_BUILDDIR + TARGET_NAME + ".app" + " -o",
           OutPutPath
            )
        )
        print build_ipa_command
        print "************************"
        os.system(build_ipa_command)
        print "*************************"
        print build_ipa_command
        print "build ipa"+ ipa_name
        print "*************************"
        ftp=FTP()
        ftp.set_debuglevel(2)
        ftp.connect(FTPServer,Port)
        ftp.login()
        ftp.cwd(UploadDir)
        ftp.storbinary("stor "+ipa_name+".ipa",open(OutPutPath,"rb"))
        print("############################")
        url = "ftp:"+FTPServer+UploadDir+ipa_name+".ipa"
        print url
        notify("IPA build finish", ipa_name, url, userInfo={"action":"open_url", "value":url})


if __name__ == "__main__":
    run_main(sys.argv[0])
