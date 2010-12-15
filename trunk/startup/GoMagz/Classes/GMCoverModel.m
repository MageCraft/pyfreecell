//
//  GMCoverModel.m
//  GoMagz
//
//  Created by Aladdin on 11/20/10.
//  Copyright 2010 innovation-works. All rights reserved.
//

#import "GMCoverModel.h"


@implementation GMCoverModel
@synthesize titleString,subTitleString,imageUrlString;
@synthesize normalColor,selectedColor;
+ (id)coverModelWithTitle:(NSString *)title andSubTitle:(NSString*)subTitle andImageUrlString:(NSString *)imageUrl andColor:(UIColor*)color{
	GMCoverModel * model = [[GMCoverModel alloc] init];
	model.titleString = title;
	model.subTitleString = subTitle;
	model.imageUrlString = imageUrl;
	model.normalColor = color;
	return [model autorelease];
}

@end
