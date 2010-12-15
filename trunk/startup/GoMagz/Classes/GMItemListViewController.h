//
//  GMItemListViewController.h
//  GoMagz
//
//  Created by Aladdin on 11/20/10.
//  Copyright 2010 innovation-works. All rights reserved.
//

#import <UIKit/UIKit.h>

@class GMItemPagesViewController;
@interface GMItemListViewController : UIViewController {
	GMItemPagesViewController* pages;
	
	NSInteger toPage;
}

@property (nonatomic, assign) NSInteger toPage;
@property (nonatomic, retain) GMItemPagesViewController *pages;

@end


