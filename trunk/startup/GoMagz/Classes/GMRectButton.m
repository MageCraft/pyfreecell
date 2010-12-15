//
//  GMRectButton.m
//  GoMagz
//
//  Created by Aladdin on 11/20/10.
//  Copyright 2010 innovation-works. All rights reserved.
//

#import "GMRectButton.h"


@implementation GMRectButton


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
    [super dealloc];
}

#pragma mark -
+ (id)rectButtonWithTarget:(id)target andSelector:(SEL)aSelector andTitle:(NSString *)title andColor:(UIColor*)color{
	CGSize titleSize = [title sizeWithFont:[UIFont boldSystemFontOfSize:50]];
	CGRect btnFrame = CGRectMake(0, 0, titleSize.width+5, titleSize.height+5);
	GMRectButton* btn = [GMRectButton buttonWithType:UIButtonTypeCustom];
	btn.frame = btnFrame;
	[btn setTitle:title forState:UIControlStateNormal];
	[btn setFont:[UIFont boldSystemFontOfSize:50]];
	[btn setTitleColor:color forState:UIControlStateNormal];
	[btn setBackgroundColor:[UIColor clearColor]];
	[btn addTarget:target action:aSelector forControlEvents:UIControlEventTouchUpInside];
	return btn;
}
@end
