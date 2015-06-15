//
//  AppDelegate.m
//  test
//
//  Created by virgil on 15-5-25.
//  Copyright (c) 2015年 xtownmobile. All rights reserved.
//

#import "AppDelegate.h"
#import "Base64Coder.h"
@interface AppDelegate ()

@end

@implementation AppDelegate


- (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions {
    NSString *s = @"eyJpZCI6MjQ0LCJ2ZXJzaW9uIjoiMS4wIiwiYm9va191bml0IjpbeyJib29rX3ZvbHVtZSI6IjTkuIsgQiIsImJvb2tfdW5pdF9uYW1lIjoi56ys5LiA5Y2V5YWDIiwiYm9va19pbmRleHMiOlt7ImJvb2tfaW5kZXhpZCI6OCwibmFtZSI6IuesrDEx6K++IiwicGFnZXMiOlt7ImlkIjo1LCJyYW5rIjoxLCJwYWdlX251bWJlciI6Inc4MyIsInVybCI6Im1hdGgvMTAwNDA2In0seyJpZCI6NCwicmFuayI6MiwicGFnZV9udW1iZXIiOiJ3ODIiLCJ1cmwiOiJtYXRoLzEwMDQwNSJ9LHsiaWQiOjYsInJhbmsiOjMsInBhZ2VfbnVtYmVyIjoidzg0IiwidXJsIjoibWF0aC8xMzQ0MDAzODAifSx7InJhbmsiOjR9LHsicmFuayI6NX0seyJyYW5rIjo2fSx7InJhbmsiOjd9LHsicmFuayI6OH0seyJyYW5rIjo5fSx7InJhbmsiOjEwfV19XX1dLCJhcGkiOltdfQ00";
     NSString *sss = [Base64Coder decodeString:s withEncodingOrZero:NSASCIIStringEncoding];
    // Override point for customization after application launch.
    return YES;
}

- (void)applicationWillResignActive:(UIApplication *)application {
    // Sent when the application is about to move from active to inactive state. This can occur for certain types of temporary interruptions (such as an incoming phone call or SMS message) or when the user quits the application and it begins the transition to the background state.
    // Use this method to pause ongoing tasks, disable timers, and throttle down OpenGL ES frame rates. Games should use this method to pause the game.
}

- (void)applicationDidEnterBackground:(UIApplication *)application {
    // Use this method to release shared resources, save user data, invalidate timers, and store enough application state information to restore your application to its current state in case it is terminated later.
    // If your application supports background execution, this method is called instead of applicationWillTerminate: when the user quits.
}

- (void)applicationWillEnterForeground:(UIApplication *)application {
    // Called as part of the transition from the background to the inactive state; here you can undo many of the changes made on entering the background.
}

- (void)applicationDidBecomeActive:(UIApplication *)application {
    // Restart any tasks that were paused (or not yet started) while the application was inactive. If the application was previously in the background, optionally refresh the user interface.
}

- (void)applicationWillTerminate:(UIApplication *)application {
    // Called when the application is about to terminate. Save data if appropriate. See also applicationDidEnterBackground:.
}

@end
