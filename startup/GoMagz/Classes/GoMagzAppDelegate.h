//
//  GoMagzAppDelegate.h
//  GoMagz
//
//  Created by Aladdin on 11/20/10.
//  Copyright 2010 innovation-works. All rights reserved.
//

#import <UIKit/UIKit.h>

@class GMCoverPageViewController;

@interface GoMagzAppDelegate : NSObject <UIApplicationDelegate> {
    UIWindow *window;
	
    GMCoverPageViewController *viewController;
	
	NSMutableArray * cacheItemsArray;
}

@property (nonatomic, retain) NSMutableArray *cacheItemsArray;
@property (nonatomic, retain) IBOutlet UIWindow *window;
@property (nonatomic, retain) IBOutlet GMCoverPageViewController *viewController;

@end


