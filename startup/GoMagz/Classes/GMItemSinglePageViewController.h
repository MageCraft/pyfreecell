//
//  GMItemSinglePageViewController.h
//  GoMagz
//
//  Created by Aladdin on 11/20/10.
//  Copyright 2010 innovation-works. All rights reserved.
//

#import <UIKit/UIKit.h>

@class GMTopicItemModel;
@interface GMItemSinglePageViewController : UIViewController {
	GMTopicItemModel * topicModel;
}

@property (nonatomic, retain) GMTopicItemModel *topicModel;
@end

