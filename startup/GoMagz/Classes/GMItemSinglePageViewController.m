    //
//  GMItemSinglePageViewController.m
//  GoMagz
//
//  Created by Aladdin on 11/20/10.
//  Copyright 2010 innovation-works. All rights reserved.
//

#import "GMItemSinglePageViewController.h"
#import "GMItemCell.h"
#import "GMTopicTitleView.h"
#import "GMTopicItemModel.h"
#import "GMHotSpotRectButton.h"
#import "UIImageView+WebCache.h"
@implementation GMItemSinglePageViewController

@synthesize topicModel;
/*
 // The designated initializer.  Override if you create the controller programmatically and want to perform customization that is not appropriate for viewDidLoad.
- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil {
    if ((self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil])) {
        // Custom initialization
    }
    return self;
}
*/


// Implement viewDidLoad to do additional setup after loading the view, typically from a nib.
- (void)viewDidLoad {
    [super viewDidLoad];
	if (self.topicModel.topic_type == 1) {
		GMTopicTitleView * titleView = [GMTopicTitleView titleViewWithModel:self.topicModel];
		titleView.center = CGPointMake(384, 160);
		[self.view addSubview:titleView];
		
		NSInteger count = [self.topicModel.items count];
		NSInteger i = 0;
		
		for (i = 0;i<count; i++ ) {
			//		GMItemModel* model = [self.itemArray objectAtIndex:i];
			int y = (int)i/3;
			int x = (int)i%3;
			NSInteger width = 212;
			NSInteger height = 350;
			CGRect f = CGRectMake(65+x*width, 185+72+y*height, width, height);
			GMItemCell * cell = [GMItemCell itemCellWithModel:[self.topicModel.items objectAtIndex:i]];
			[cell addTarget:self action:@selector(actionToNotification:) forControlEvents:UIControlEventTouchUpInside];
			cell.frame = f;
			cell.tag = i;
			[self.view addSubview:cell];
		}
		
	}
	if (self.topicModel.topic_type == 2) {
//		UIImage * bgImage = [[[UIImage alloc] initWithData:[NSData dataWithContentsOfURL:[NSURL URLWithString:self.topicModel.topic_image_url]]] autorelease];
//		
		UIImageView * bgImageView = [[[UIImageView alloc] initWithFrame:CGRectMake(0, 0, 786, 1024)] autorelease];
		
		[bgImageView setImageWithURL:[NSURL URLWithString:self.topicModel.topic_image_url]
					   placeholderImage:[UIImage imageNamed:@"logo.png"]];

		[self.view  addSubview:bgImageView];
		
		NSInteger usedCellCount = [self.topicModel.items count];
		NSArray * freeCellArray = [self.topicModel.topic_userInfo componentsSeparatedByString:@","];
		NSInteger freeCellCount = [freeCellArray count];
		NSInteger count = usedCellCount + freeCellCount;
		NSInteger i = 0;
		NSInteger j = 0;
		NSMutableArray * allItems = [NSMutableArray arrayWithCapacity:10];
		
		for (int k =0 ; k<count; k++) {
			if (k+1!=[[freeCellArray objectAtIndex:j] intValue]) {
				[allItems addObject:[self.topicModel.items objectAtIndex:i++]];
			}else {
				j++;
				[allItems addObject:[NSNull null]];
			}
		}
		NSLog(@"%@ %d",allItems,[allItems count]);
		for (i = 0;i<count; i++ ) {
			//		GMItemModel* model = [self.itemArray objectAtIndex:i];
			int y = (int)i/3;
			int x = (int)i%3;
			NSInteger width = 212;
			NSInteger height = 296;
			CGRect f = CGRectMake(65+x*width, y*height, width, height);
			NSLog(@"i=%d : j=%d",i,j);
			if (![[allItems objectAtIndex:i] isEqual:[NSNull null]]) {
				GMItemCell * cell = [GMItemCell itemCellWithModel:[allItems objectAtIndex:i]];
				[cell addTarget:self action:@selector(actionToNotification:) forControlEvents:UIControlEventTouchUpInside];
				cell.frame = f;
				cell.tag = i;
				[self.view addSubview:cell];
			}
			
		}
		
		
		
		
	}
	if (self.topicModel.topic_type == 3) {
		
		UIImageView * bgImageView = [[[UIImageView alloc] initWithFrame:CGRectMake(0, 0, 786, 1024)] autorelease];
		
		[bgImageView setImageWithURL:[NSURL URLWithString:self.topicModel.topic_image_url]
					placeholderImage:[UIImage imageNamed:@"logo.png"]];
		
		[self.view  addSubview:bgImageView];
		
		GMTopicTitleView * titleView = [GMTopicTitleView titleViewWithModel:self.topicModel];
		titleView.center = CGPointMake(384, 160);
		[self.view addSubview:titleView];
		
		NSArray * rectStringArray =[self.topicModel.topic_userInfo componentsSeparatedByString:@"|"];		
		NSInteger count = [rectStringArray count];
		
		NSInteger i = 0;
		
		for (i = 0;i<count; i++ ) {
			//		GMItemModel* model = [self.itemArray objectAtIndex:i];
//			int y = (int)i/3;
//			int x = (int)i%3;
//			NSInteger width = 212;
//			NSInteger height = 350;
			
			NSString * rectString = [rectStringArray objectAtIndex:i];
			CGRect rect = CGRectFromString(rectString);
			GMHotSpotRectButton * cell = [GMHotSpotRectButton rectButtonCellWithModel:[self.topicModel.items objectAtIndex:i] andFrame:rect];
			[cell addTarget:self action:@selector(actionToNotification:) forControlEvents:UIControlEventTouchUpInside];
			cell.tag = i;
			
			
			
		[self.view addSubview:cell];
		}
		
		
	}
	
	//GMTopicTitleView * titleView = [GMTopicTitleView titleViewWithModel:self.topicModel];
//	titleView.center = CGPointMake(384, 160);
//	[self.view addSubview:titleView];
//	
//	NSInteger count = [self.topicModel.items count];
//	NSInteger i = 0;
//	
//	for (i = 0;i<count; i++ ) {
////		GMItemModel* model = [self.itemArray objectAtIndex:i];
//		int y = (int)i/3;
//		int x = (int)i%3;
//		NSInteger width = 212;
//		NSInteger height = 350;
//		CGRect f = CGRectMake(65+x*width, 185+72+y*height, width, height);
//		GMItemCell * cell = [GMItemCell itemCellWithModel:[self.topicModel.items objectAtIndex:i]];
//		[cell addTarget:self action:@selector(actionToNotification:) forControlEvents:UIControlEventTouchUpInside];
//		cell.frame = f;
//		cell.tag = i;
//		[self.view addSubview:cell];
//	}
	

}
- (IBAction) actionToNotification:(id )sender{
	NSAutoreleasePool * pool = [[NSAutoreleasePool alloc] init];
	GMItemCell * cell = (GMItemCell*)sender;
	NSDictionary * dic = [NSDictionary dictionaryWithObjectsAndKeys:cell.item,@"GMItemModel",nil];
	[[NSNotificationCenter defaultCenter] postNotificationName:@"GoToItemDetail" object:nil userInfo:dic];
	[pool release];
}

- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation {
    // Overriden to allow any orientation.
    return YES;
}


- (void)didReceiveMemoryWarning {
    // Releases the view if it doesn't have a superview.
    [super didReceiveMemoryWarning];
    
    // Release any cached data, images, etc that aren't in use.
}


- (void)viewDidUnload {
    [super viewDidUnload];
    // Release any retained subviews of the main view.
    // e.g. self.myOutlet = nil;
}


- (void)dealloc {
	[topicModel release], topicModel = nil;
    [super dealloc];
}


@end

