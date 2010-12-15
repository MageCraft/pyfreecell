//
//  GMTopicItemModel.h
//  GoMagz
//
//  Created by Aladdin on 11/20/10.
//  Copyright 2010 innovation-works. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface GMTopicItemModel : NSObject {
	NSMutableArray * items;
	NSString	* topicName_cn;
	NSString	* topicName_en;
	NSString	* topic_intro;
	NSString	* topic_brands;
	NSString	* topic_image_url;
	NSInteger	 topic_type;
	NSString	* topic_userInfo; 
}

@property (nonatomic, copy) NSString *topic_userInfo;
@property (nonatomic, assign) NSInteger topic_type;
@property (nonatomic, copy) NSString *topic_image_url;
@property (nonatomic, copy) NSString *topic_brands;
@property (nonatomic, copy) NSString *topic_intro;
@property (nonatomic, retain) NSMutableArray *items;
@property (nonatomic, copy) NSString *topicName_en;
@property (nonatomic, copy) NSString *topicName_cn;


+ (id)topicItemWithDictionary:(NSDictionary*)d;

@end





