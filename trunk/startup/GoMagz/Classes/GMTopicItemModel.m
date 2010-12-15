//
//  GMTopicItemModel.m
//  GoMagz
//
//  Created by Aladdin on 11/20/10.
//  Copyright 2010 innovation-works. All rights reserved.
//

#import "GMTopicItemModel.h"
#import "GMItemModel.h"
#import "GMConstants.h"
@implementation GMTopicItemModel

@synthesize topic_userInfo;
@synthesize topic_type;
@synthesize topic_image_url;
@synthesize topic_brands;
@synthesize topic_intro;
@synthesize items;
@synthesize topicName_en;
@synthesize topicName_cn;


- (void)dealloc {
	[topic_userInfo release], topic_userInfo = nil;
	[topic_image_url release], topic_image_url = nil;
	[topic_brands release], topic_brands = nil;
	[topic_intro release], topic_intro = nil;
	[items release], items = nil;
	[topicName_en release], topicName_en = nil;
	[topicName_cn release], topicName_cn = nil;
	[super dealloc];
}
#pragma mark -

+ (id)topicItemWithDictionary:(NSDictionary*)d{
	if (!d) {
		NSLog(@"%s dictionary is vaild",_cmd);
		return nil;
	}
	NSLog(@"%@",d);
	GMTopicItemModel * topicItem = [[GMTopicItemModel alloc] init];
	topicItem.topicName_en = [d objectForKey:@"topic_en"];
	topicItem.topicName_cn = [d objectForKey:@"topic_cn"];
	topicItem.topic_brands = [d objectForKey:@"topic_brands"];
	topicItem.topic_intro = [d objectForKey:@"topic_intro"];
	topicItem.topic_image_url = [NSString stringWithFormat:@"%@%@",kItemImageURL,[d objectForKey:@"img_url"]];
	topicItem.topic_type = [[d objectForKey:@"topic_type"] intValue];
	topicItem.topic_userInfo = [d objectForKey:@"topic_userInfo"];
	topicItem.items = [NSMutableArray arrayWithCapacity:10];
	NSAutoreleasePool * pool = [[NSAutoreleasePool alloc] init];
	for (NSDictionary * itemDic in [d objectForKey:@"topic_item"]) {
		GMItemModel * item = [GMItemModel itemModelWithDictionary:itemDic];
		[topicItem.items addObject:item];
	}
	[pool release];
	return [topicItem autorelease];
}

#pragma mark -

@end









