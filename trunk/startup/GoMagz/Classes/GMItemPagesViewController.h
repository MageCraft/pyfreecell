//
//  GMItemPagesViewController.h
//  GoMagz
//
//  Created by Aladdin on 11/20/10.
//  Copyright 2010 innovation-works. All rights reserved.
//

#import <UIKit/UIKit.h>


@interface GMItemPagesViewController : UIViewController <UIScrollViewDelegate>{
	UIScrollView * pageScrollView;
	
	NSInteger numberOfPage;
	
	NSMutableArray * viewControllers;
	NSMutableArray * topicArray;
	BOOL pageControlUsed;
	
	NSInteger toPage;
	
}

@property (nonatomic, assign) NSInteger toPage;
@property (nonatomic, assign) BOOL pageControlUsed;
@property (nonatomic ,retain) IBOutlet 	UIScrollView * pageScrollView;
@property (nonatomic ,assign) NSInteger numberOfPage;
@property (nonatomic ,retain) NSMutableArray * viewControllers;
@property (nonatomic ,retain) NSMutableArray * topicArray;
- (void)loadScrollViewWithPage:(int)page;
@end


