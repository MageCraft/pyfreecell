//
//  GMHotSpotRectButton.m
//  GoMagz
//
//  Created by Aladdin on 11/21/10.
//  Copyright 2010 innovation-works. All rights reserved.
//

#import "GMHotSpotRectButton.h"
#import "GMItemModel.h"

@implementation GMHotSpotRectButton

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

+ (id)rectButtonCellWithModel:(GMItemModel*)model andFrame:(CGRect)rect{
	if ([model isEqual:[NSNull null]]) {
		return nil;
	}
	GMHotSpotRectButton * cell = [GMHotSpotRectButton buttonWithType:UIButtonTypeCustom];
	cell.frame = rect;
	cell.item = model;
	NSInteger yChanges = 0;
	if (cell.frame.origin.y+cell.frame.size.height>900) {
		yChanges = 70;
	}
	//UIImageView * itemImage = [[UIImageView alloc] initWithFrame:CGRectMake(0, 30, 212, 212)];
//	[itemImage setBackgroundColor:[UIColor whiteColor]];
//	[itemImage setImage:[UIImage imageWithData:[NSData dataWithContentsOfURL:[NSURL URLWithString:cell.item.img_url]]]];
//	itemImage.contentMode = UIViewContentModeScaleAspectFit;
//	[cell addSubview:itemImage];
//	[itemImage release];

	
	UILabel * itemName = [[UILabel alloc] initWithFrame:CGRectMake(50,40-yChanges, 150, 35)];
	itemName.center = CGPointMake(106, itemName.center.y);
	itemName.font = [UIFont boldSystemFontOfSize:14];
	itemName.lineBreakMode = UILineBreakModeWordWrap;
	itemName.textAlignment = UITextAlignmentCenter;
	itemName.backgroundColor = [UIColor clearColor];
	itemName.adjustsFontSizeToFitWidth =YES;
	[itemName setNumberOfLines:2];
	[itemName setText:model.name];
//	[itemName setTextColor:[UIColor colorWithRed:34.0/255.0 green:34.0/255.0 blue:34.0/255.0 alpha:1.0]];
	[itemName setTextColor:[UIColor whiteColor]];
	[itemName setBackgroundColor:[UIColor colorWithRed:80.0/255.0 green:80.0/255.0 blue:80.0/255.0 alpha:0.8]];
	[cell addSubview:itemName];
	[itemName release];

	
	
	UILabel * itemPrice = [[UILabel alloc] initWithFrame:CGRectMake(85,78-yChanges, 100, 20)];
	itemPrice.center = CGPointMake(106+25, itemPrice.center.y);
	itemPrice.font = [UIFont boldSystemFontOfSize:14];
	itemPrice.lineBreakMode = UILineBreakModeWordWrap;
	itemPrice.textAlignment = UITextAlignmentCenter;
	itemPrice.backgroundColor = [UIColor clearColor];
	itemPrice.adjustsFontSizeToFitWidth =YES;
	[itemPrice setNumberOfLines:2];
	[itemPrice setText:[NSString stringWithFormat:@"RMB %@",model.price]];
//	[itemPrice setTextColor:[UIColor blackColor]];
	[itemPrice setTextColor:[UIColor whiteColor]];
	[cell addSubview:itemPrice];
	[itemPrice release];
	
	[itemPrice setBackgroundColor:[UIColor colorWithRed:80.0/255.0 green:80.0/255.0 blue:80.0/255.0 alpha:0.8]];
	return cell;	
}


@end

