//
//  GoMagzAppDelegate.m
//  GoMagz
//
//  Created by Aladdin on 11/20/10.
//  Copyright 2010 innovation-works. All rights reserved.
//

#import "GoMagzAppDelegate.h"
#import "GMCoverPageViewController.h"

@implementation GoMagzAppDelegate

@synthesize cacheItemsArray;
@synthesize window;
@synthesize viewController;

#pragma mark -
#pragma mark Application lifecycle

- (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions {    
    self.cacheItemsArray = [NSMutableArray arrayWithCapacity:30];
    // Override point for customization after app launch. 
	UINavigationController * nav = [[UINavigationController alloc] initWithRootViewController:viewController];
	
    [window addSubview:nav.view];
    [window makeKeyAndVisible];
	UIView * bottomMaskView = [[UIView alloc] initWithFrame:CGRectMake(0,992+20, 768, 12)];
	bottomMaskView.backgroundColor = [UIColor colorWithRed:187.0/255.0 green:0 blue:0 alpha:1.0];
	[nav.view addSubview:bottomMaskView];
	
	return YES;
}


- (void)applicationWillResignActive:(UIApplication *)application {
    /*
     Sent when the application is about to move from active to inactive state. This can occur for certain types of temporary interruptions (such as an incoming phone call or SMS message) or when the user quits the application and it begins the transition to the background state.
     Use this method to pause ongoing tasks, disable timers, and throttle down OpenGL ES frame rates. Games should use this method to pause the game.
     */
}


- (void)applicationDidBecomeActive:(UIApplication *)application {
    /*
     Restart any tasks that were paused (or not yet started) while the application was inactive. If the application was previously in the background, optionally refresh the user interface.
     */
}


- (void)applicationWillTerminate:(UIApplication *)application {
    /*
     Called when the application is about to terminate.
     See also applicationDidEnterBackground:.
     */
}


#pragma mark -
#pragma mark Memory management

- (void)applicationDidReceiveMemoryWarning:(UIApplication *)application {
    /*
     Free up as much memory as possible by purging cached data objects that can be recreated (or reloaded from disk) later.
     */
}


- (void)dealloc {
	[cacheItemsArray release], cacheItemsArray = nil;
    [viewController release];viewController = nil;
    [window release];  window = nil;
    [super dealloc];
}


@end
@interface UINavigationBar (TransparentAdditions)
@end
@implementation UINavigationBar (TransparentAdditions)
- (void)drawRect:(CGRect)rect {
	CGRect lineRect = CGRectMake(0, 0, 768, 44);
	CGContextRef current = UIGraphicsGetCurrentContext();
	CGContextSetFillColorWithColor(current,[UIColor colorWithRed:187.0/255.0 green:0.0 blue:0.0 alpha:1.0].CGColor);
	CGContextFillRect(current, lineRect);
}
@end

