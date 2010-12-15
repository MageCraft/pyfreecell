//
//  GMItemModel.h
//  GoMagz
//
//  Created by Aladdin on 11/20/10.
//  Copyright 2010 innovation-works. All rights reserved.
//

#import <Foundation/Foundation.h>


@interface GMItemModel : NSObject<NSCopying> {
	NSString * name;
	NSString * price;
	NSString * region;
	NSString * type;
	NSString * description;
	NSString * link;
	NSString * img_url;
}

@property (nonatomic, copy) NSString *img_url;
@property (nonatomic ,copy) NSString * name;
@property (nonatomic ,copy) NSString * price;
@property (nonatomic ,copy) NSString * region;
@property (nonatomic ,copy) NSString * type;
@property (nonatomic ,copy) NSString * description;
@property (nonatomic ,copy) NSString * link;

+(id) itemModelWithDictionary:(NSDictionary *)d;

@end

