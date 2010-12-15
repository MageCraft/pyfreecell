//
//  GMTopicTitleView.h
//  GoMagz
//
//  Created by Aladdin on 11/21/10.
//  Copyright 2010 innovation-works. All rights reserved.
//

#import <UIKit/UIKit.h>
@class GMTopicItemModel;

@interface GMTopicTitleView : UIView {
	GMTopicItemModel * Topic;
	NSInteger  TitleType;
	NSInteger TopicIndex;
}

@property (nonatomic, assign) NSInteger TopicIndex;
@property (nonatomic, assign) NSInteger TitleType;
@property (nonatomic, retain) GMTopicItemModel *Topic;
+ (id)titleViewWithModel:(GMTopicItemModel*)model;
+ (id)coverViewWithModel:(GMTopicItemModel*)model;
@end




