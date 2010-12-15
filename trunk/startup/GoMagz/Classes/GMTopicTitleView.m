//
//  GMTopicTitleView.m
//  GoMagz
//
//  Created by Aladdin on 11/21/10.
//  Copyright 2010 innovation-works. All rights reserved.
//

#import "GMTopicTitleView.h"
#import "GMTopicItemModel.h"

@implementation GMTopicTitleView

@synthesize TopicIndex;
@synthesize TitleType;
@synthesize Topic;


- (id)initWithFrame:(CGRect)frame {
    if ((self = [super initWithFrame:frame])) {
        // Initialization code
    }
    return self;
}


// Only override drawRect: if you perform custom drawing.
// An empty implementation adversely affects performance during animation.
- (void)drawRect:(CGRect)rect {
    // Drawing code
		if (self.TitleType ==1) {
		CGRect lineRect = CGRectMake(0, 191, 638, 1);
		CGContextRef current = UIGraphicsGetCurrentContext();
		CGContextSetFillColorWithColor(current,[UIColor colorWithRed:187.0/255.0 green:0.0 blue:0.0 alpha:1.0].CGColor);
		CGContextFillRect(current, lineRect);
		}
}

- (void)dealloc {
    [Topic release], Topic = nil;
    [super dealloc];
}
- (IBAction)postCoverTitleClickNotification:(NSNotification*)n{
	NSAutoreleasePool * pool = [[NSAutoreleasePool alloc] init];
	NSLog(@"%s",_cmd);
	NSDictionary * dic= [NSDictionary dictionaryWithObjectsAndKeys:[NSString stringWithFormat:@"%d",self.TopicIndex],@"topicIndex",nil];
	[[NSNotificationCenter defaultCenter] postNotificationName:@"CoverTitleSelector" object:nil userInfo:dic];
	[pool release];
} 
#pragma mark -
+ (id)titleViewWithModel:(GMTopicItemModel*)model{
	
	GMTopicTitleView * titleView = [[GMTopicTitleView alloc] initWithFrame:CGRectMake(0, 0, 638, 192)];
	titleView.backgroundColor = [UIColor clearColor];
	titleView.TitleType = 1;
	
	UILabel * titleLabel = [[UILabel alloc] initWithFrame:CGRectMake(0, 0, 638, 60)];
	[titleLabel setFont:[UIFont boldSystemFontOfSize:60]];
	[titleLabel setMinimumFontSize:40];
	titleLabel.adjustsFontSizeToFitWidth = YES;
	[titleLabel setText:model.topicName_en];
	[titleLabel setTextColor:[UIColor colorWithRed:51.0/255.0 green:51.0/255.0 blue:51.0/255.0 alpha:1.0]];
	[titleLabel setCenter:CGPointMake(319, 30)];
	[titleLabel setTextAlignment:UITextAlignmentCenter];
	[titleLabel setBackgroundColor:[UIColor clearColor]];
	[titleView addSubview:titleLabel];
	[titleLabel release];
	
	UILabel * subTitleLabel = [[UILabel alloc] initWithFrame:CGRectMake(0, 0, 638, 55)];
	[subTitleLabel setFont:[UIFont boldSystemFontOfSize:48]];
	[subTitleLabel setText:model.topicName_cn];
	[subTitleLabel setTextColor:[UIColor colorWithRed:51.0/255.0 green:51.0/255.0 blue:51.0/255.0 alpha:1.0]];
	[subTitleLabel setCenter:CGPointMake(319, 90)];
	[subTitleLabel setTextAlignment:UITextAlignmentCenter];
	[subTitleLabel setBackgroundColor:[UIColor clearColor]];
	[titleView addSubview:subTitleLabel];
	[subTitleLabel release];
	
	UILabel * topicIntro = [[UILabel alloc] initWithFrame:CGRectMake(0, 0, 500, 80)];
	[topicIntro setFont:[UIFont systemFontOfSize:14]];
	[topicIntro setNumberOfLines:3];
	[topicIntro setText:model.topic_intro];
	[topicIntro setTextColor:[UIColor colorWithRed:80.0/255.0 green:80.0/255.0 blue:80.0/255.0 alpha:1.0]];
	[topicIntro setCenter:CGPointMake(319, 150)];
	[topicIntro setTextAlignment:UITextAlignmentCenter];
	[topicIntro setBackgroundColor:[UIColor clearColor]];
	[titleView addSubview:topicIntro];
	[topicIntro release];
	
	return [titleView autorelease];
}

+ (id)coverViewWithModel:(GMTopicItemModel*)model{
	GMTopicTitleView * titleView = [[GMTopicTitleView alloc] initWithFrame:CGRectMake(0, 0, 638, 192)];
	titleView.backgroundColor = [UIColor clearColor];
	titleView.Topic = model;
	titleView.TitleType = 0;
	
	UILabel * titleLabel = [[UILabel alloc] initWithFrame:CGRectMake(0, 0, 638, 60)];
	[titleLabel setFont:[UIFont boldSystemFontOfSize:60]];
	[titleLabel setMinimumFontSize:40];
	titleLabel.adjustsFontSizeToFitWidth = YES;
	[titleLabel setText:model.topicName_en];
	[titleLabel setTextColor:[UIColor whiteColor]];
	[titleLabel setCenter:CGPointMake(319, 30)];
	[titleLabel setTextAlignment:UITextAlignmentLeft];
	[titleLabel setBackgroundColor:[UIColor clearColor]];
	[titleView addSubview:titleLabel];
	[titleLabel release];
	
	UILabel * subTitleLabel = [[UILabel alloc] initWithFrame:CGRectMake(0, 0, 638, 55)];
	[subTitleLabel setFont:[UIFont boldSystemFontOfSize:48]];
	[subTitleLabel setText:model.topicName_cn];
	[subTitleLabel setTextColor:[UIColor whiteColor]];
	[subTitleLabel setCenter:CGPointMake(319, 84)];
	[subTitleLabel setTextAlignment:UITextAlignmentLeft];
	[subTitleLabel setBackgroundColor:[UIColor clearColor]];
	[titleView addSubview:subTitleLabel];
	[subTitleLabel release];
	
	UILabel * topicIntro = [[UILabel alloc] initWithFrame:CGRectMake(0, 0, 638, 80)];
	[topicIntro setFont:[UIFont systemFontOfSize:24]];
	[topicIntro setNumberOfLines:1];
	[topicIntro setText:model.topic_brands];
	[topicIntro setTextColor:[UIColor whiteColor]];
	[topicIntro setCenter:CGPointMake(319, 120)];
	[topicIntro setTextAlignment:UITextAlignmentLeft];
	[topicIntro setBackgroundColor:[UIColor clearColor]];
	[titleView addSubview:topicIntro];
	[topicIntro release];
	
	
	UIButton * maskButton = [UIButton buttonWithType:UIButtonTypeCustom];
	maskButton.frame = titleView.frame;
	[maskButton addTarget:titleView action:@selector(postCoverTitleClickNotification:) forControlEvents:UIControlEventTouchUpInside];
	[titleView addSubview:maskButton];
	return [titleView autorelease];
}
#pragma mark -
@end




