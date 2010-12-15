//
//  GMCoverPageViewController.h
//  GoMagz
//
//  Created by Aladdin on 11/20/10.
//  Copyright 2010 innovation-works. All rights reserved.
//

#import <UIKit/UIKit.h>
#import "GMCoverModel.h"
#import "ASIHTTPRequest.h"
#import "ASINetworkQueue.h"
#import "ASIHTTPRequestDelegate.h"
@interface GMCoverPageViewController : UIViewController<ASIHTTPRequestDelegate> {
	UIImageView * backgroundImageView;
	
	UIImageView * logoImageView;
	UIButton * btn;
	
	UIView * maskView;
	
//Models
	GMCoverModel * coverModel;
	
	ASIHTTPRequest *getActorMoviesRequest;
	ASINetworkQueue *networkQueue;

	
	NSInteger curIndex;
	BOOL isInScreen;
}

@property (nonatomic, retain) UIButton *btn;
@property (nonatomic, assign) BOOL isInScreen;
@property (nonatomic, retain) UIView *maskView;
@property (nonatomic, assign) NSInteger curIndex;
@property (nonatomic, retain) UIImageView *logoImageView;
@property (nonatomic, retain) 	UIImageView * backgroundImageView;
@property (nonatomic, retain) 	GMCoverModel * coverModel;
@property (retain) ASINetworkQueue *networkQueue;
- (IBAction) actionToItemList:(id)sender; 
@end






