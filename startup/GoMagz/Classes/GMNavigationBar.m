//
//  GMNavigationBar.m
//  GoMagz
//
//  Created by Aladdin on 11/21/10.
//  Copyright 2010 innovation-works. All rights reserved.
//

#import "GMNavigationBar.h"


@implementation GMNavigationBar


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
+ (id) bar{
	GMNavigationBar * bar = [[GMNavigationBar alloc] initWithFrame:CGRectMake(0, 0, 768, 44)];
	[bar setBackgroundColor:[UIColor colorWithRed:187.0/255.0 green:0.0 blue:0.0 alpha:1.0]];
	
	return [bar autorelease];
}

@end
