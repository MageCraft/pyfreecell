//
//  GMCoverModel.h
//  GoMagz
//
//  Created by Aladdin on 11/20/10.
//  Copyright 2010 innovation-works. All rights reserved.
//

#import <Foundation/Foundation.h>


@interface GMCoverModel : NSObject {
	NSString * titleString;
	NSString * subTitleString;
	NSString * imageUrlString;
	UIColor * normalColor;
	UIColor * selectedColor;
}
@property (nonatomic, retain) UIColor * normalColor;
@property (nonatomic, retain) UIColor * selectedColor;
@property (nonatomic, copy) NSString * titleString;
@property (nonatomic, copy) NSString * subTitleString;
@property (nonatomic, copy) NSString * imageUrlString;
+ (id)coverModelWithTitle:(NSString *)title andSubTitle:(NSString*)subTitle andImageUrlString:(NSString *)imageUrl andColor:(UIColor*)color;
@end
