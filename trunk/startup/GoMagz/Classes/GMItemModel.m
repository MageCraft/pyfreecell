//
//  GMItemModel.m
//  GoMagz
//
//  Created by Aladdin on 11/20/10.
//  Copyright 2010 innovation-works. All rights reserved.
//

#import "GMItemModel.h"
#import "GMConstants.h"

@implementation GMItemModel

@synthesize img_url;
@synthesize name,price,region,type,description,link;
- (void)dealloc{
	[img_url release], img_url = nil;
	[name release];name = nil;
	[price release];price = nil;
	[region release];region = nil;
	[type release];type = nil;
	[description release];description = nil;
	[link release];link = nil;
	[super dealloc];
}
+(id) itemModelWithDictionary:(NSDictionary *)d{
	GMItemModel * item =[[GMItemModel alloc] init];
	if ([d isKindOfClass:[NSDictionary class]]&&d) {
		item.img_url = [NSString stringWithFormat:@"%@%@",kItemImageURL,[d objectForKey:@"img_url"]];
		item.name = [d objectForKey:@"name"];
		item.price = [d objectForKey:@"price"];
		item.region = [d objectForKey:@"region"];
		item.type = [d objectForKey:@"type"];
		item.description = [d objectForKey:@"description"];
		item.link = [d objectForKey:@"link"];
	}else {
		NSLog(@"%s Dictionary is vaild",_cmd);
	}
	return [item autorelease];
}

- (id)copyWithZone:(NSZone *)zone
{
    GMItemModel *copy = [[[self class] allocWithZone: zone] init];
	
    copy->name = nil;
	copy->link = nil;
	copy->img_url = nil;
	copy->price = nil;
	copy->region = nil;
	copy->type = nil;
	copy->description = nil;
    
	[copy setLink:[self link]];
	[copy setName:[self name]];
	[copy setImg_url:[self img_url]];
	[copy setPrice:[self price]];
	[copy setRegion:[self region]];
	[copy setType:[self type]];
    return copy;
}
@end


