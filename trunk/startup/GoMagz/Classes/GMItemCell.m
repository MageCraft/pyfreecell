//
//  GMItemCell.m
//  GoMagz
//
//  Created by Aladdin on 11/20/10.
//  Copyright 2010 innovation-works. All rights reserved.
//

#import "GMItemCell.h"
#import "GMItemModel.h"
#import "UIImageView+WebCache.h"
@implementation GMItemCell

@synthesize item;


- (id)initWithFrame:(CGRect)frame {
    if ((self = [super initWithFrame:frame])) {
        // Initialization code
    }
    return self;
}

/*
// Only override drawRect: if you perform custom drawing.
// An empty implementation adversely affects performance during animation.
- (void)drawRect:(CGRect)rect {
    // Drawing code
}
*/

- (void)dealloc {
    [item release], item = nil;
    [super dealloc];
}
#pragma mark -
+ (id)itemCellWithModel:(GMItemModel*)model{
	if ([model isEqual:[NSNull null]]) {
		return nil;
	}
	GMItemCell * cell = [GMItemCell buttonWithType:UIButtonTypeCustom];
	cell.frame = CGRectMake(0, 0, 212, 350);
	cell.item = model;
	
	UIImageView * itemImage = [[UIImageView alloc] initWithFrame:CGRectMake(0, 30, 212, 212)];
	[itemImage setBackgroundColor:[UIColor whiteColor]];
//	[itemImage setImage:[UIImage imageWithData:[NSData dataWithContentsOfURL:[NSURL URLWithString:cell.item.img_url]]]];
	
	[itemImage setImageWithURL:[NSURL URLWithString:cell.item.img_url]
                   placeholderImage:[UIImage imageNamed:@"logo.png"]];

	
	itemImage.contentMode = UIViewContentModeScaleAspectFit;
	[cell addSubview:itemImage];
	[itemImage release];
	
	
	
	UILabel * itemName = [[UILabel alloc] initWithFrame:CGRectMake(0,262, 180, 35)];
	itemName.center = CGPointMake(106, itemName.center.y);
	itemName.font = [UIFont boldSystemFontOfSize:14];
	itemName.lineBreakMode = UILineBreakModeWordWrap;
	itemName.textAlignment = UITextAlignmentCenter;
	itemName.backgroundColor = [UIColor clearColor];
	itemName.adjustsFontSizeToFitWidth =YES;
	[itemName setNumberOfLines:2];
	[itemName setText:model.name];
	[itemName setTextColor:[UIColor colorWithRed:34.0/255.0 green:34.0/255.0 blue:34.0/255.0 alpha:1.0]];
	[cell addSubview:itemName];
	[itemName release];
	
	UILabel * itemPrice = [[UILabel alloc] initWithFrame:CGRectMake(0,300, 180, 35)];
	itemPrice.center = CGPointMake(106, itemPrice.center.y);
	itemPrice.font = [UIFont boldSystemFontOfSize:14];
	itemPrice.lineBreakMode = UILineBreakModeWordWrap;
	itemPrice.textAlignment = UITextAlignmentCenter;
	itemPrice.backgroundColor = [UIColor clearColor];
	itemPrice.adjustsFontSizeToFitWidth =YES;
	[itemPrice setNumberOfLines:2];
	[itemPrice setText:[NSString stringWithFormat:@"RMB %@",model.price]];
	[itemPrice setTextColor:[UIColor blackColor]];
	[cell addSubview:itemPrice];
	[itemPrice release];
	
//	[cell setBackgroundColor:[UIColor redColor]];
	return cell;	
}

@end

