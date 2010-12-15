    //
//  GMItemPagesViewController.m
//  GoMagz
//
//  Created by Aladdin on 11/20/10.
//  Copyright 2010 innovation-works. All rights reserved.
//
#import "GoMagzAppDelegate.h"
#import "GMItemPagesViewController.h"
#import "GMItemSinglePageViewController.h"
#import "GMTopicItemModel.h"
static NSUInteger kNumberOfItemsPages = 3;
@interface GMItemPagesViewController (PrivateMethods)


- (void)scrollViewDidScroll:(UIScrollView *)sender;

@end


@implementation GMItemPagesViewController

@synthesize toPage;
@synthesize pageControlUsed;
@synthesize pageScrollView;
@synthesize viewControllers;
@synthesize topicArray;
@synthesize numberOfPage;

- (void)reloadPageView{
	NSMutableArray *controllers = [[NSMutableArray alloc] init];
    for (unsigned i = 0; i < ceil(self.numberOfPage); i++) {
        [controllers addObject:[NSNull null]];
    }
    self.viewControllers = controllers;
    [controllers release];
	
	
	self.pageScrollView.contentSize = CGSizeMake(self.pageScrollView.frame.size.width*ceil(self.numberOfPage),self.pageScrollView.frame.size.height);
	self.pageScrollView.showsHorizontalScrollIndicator = NO;
	self.pageScrollView.showsVerticalScrollIndicator = NO;
	self.pageScrollView.scrollsToTop = NO;
	self.pageScrollView.delegate = self;
//	self.pageControl.numberOfPages = ceil(self.numberOfPage);
//	self.pageControl.currentPage = 0;
	
	
	[self loadScrollViewWithPage:0];
    [self loadScrollViewWithPage:1];
}




 // The designated initializer.  Override if you create the controller programmatically and want to perform customization that is not appropriate for viewDidLoad.
- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil {
    if ((self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil])) {
        // Custom initialization
		self.toPage = -1;
    }
    return self;
}


// Implement viewDidLoad to do additional setup after loading the view, typically from a nib.
- (void)viewDidLoad {
    [super viewDidLoad];
	self.topicArray = [(GoMagzAppDelegate*)[[UIApplication sharedApplication] delegate] cacheItemsArray];
	if (self.topicArray == nil||[self.topicArray count]==0) {
		[[NSNotificationCenter defaultCenter] postNotificationName:@"allItemIsEmpty" object:nil];
	}

	
//	self.numberOfPage = ceil([self.allItems count]/40.0);
	self.numberOfPage = [self.topicArray count]; 
	[self reloadPageView];
	if (self.toPage !=-1) {
		[self loadScrollViewWithPage:self.toPage];
	}
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
	
	[viewControllers release], viewControllers = nil;
	[topicArray release], topicArray = nil;
	
    [super dealloc];
}

#pragma mark -
#pragma mark methods
- (void)loadScrollViewWithPage:(int)page {
    if (page < 0) return;
    if (page >= kNumberOfItemsPages) return;
	if (page >= self.numberOfPage) return;
	if ([viewControllers count]==0) return;
    // replace the placeholder if necessary
	GMItemSinglePageViewController *controller = [viewControllers objectAtIndex:page];
    if ((NSNull *)controller == [NSNull null]) {
		//  controller = [[SingleBrandPageViewController alloc] initWithPageNumber:page];
		controller = [[GMItemSinglePageViewController alloc] initWithNibName:@"GMItemSinglePageViewController" bundle:[NSBundle mainBundle]];
//		if (40*page+40<[self.allItems	count]) {
//			controller.emotions = [NSMutableArray arrayWithArray:[self.allEmotions subarrayWithRange:NSMakeRange(40*page, 40)]];
//		}else {
//			controller.emotions = [NSMutableArray arrayWithArray:[self.allEmotions subarrayWithRange:NSMakeRange(40*page, [self.allEmotions count]-40*page)]];
//		}
		controller.topicModel = (GMTopicItemModel*)[self.topicArray objectAtIndex:page];
//		controller.itemArray = [(GMTopicItemModel*)[self.topicArray objectAtIndex:page] items];
		
        [viewControllers replaceObjectAtIndex:page withObject:controller];
//        [controller release];
    }
	
    // add the controller's view to the scroll view
    if (nil == controller.view.superview) {
        CGRect frame = pageScrollView.frame;
        frame.origin.x = frame.size.width * page;
        frame.origin.y = 0;
        controller.view.frame = frame;
        [pageScrollView addSubview:controller.view];
    }
}

- (void)scrollViewDidScroll:(UIScrollView *)sender {
    // We don't want a "feedback loop" between the UIPageControl and the scroll delegate in
    // which a scroll event generated from the user hitting the page control triggers updates from
    // the delegate method. We use a boolean to disable the delegate logic when the page control is used.
   if (pageControlUsed) {
	 //do nothing - the scroll was initiated from the page control, not the user dragging
		 return;
	 }
	
    // Switch the indicator when more than 50% of the previous/next page is visible
    CGFloat pageWidth = pageScrollView.frame.size.width;
    int page = floor((pageScrollView.contentOffset.x - pageWidth / 2) / pageWidth) + 1;
  //  pageControl.currentPage = page;
	
    // load the visible page and the page on either side of it (to avoid flashes when the user starts scrolling)
    [self loadScrollViewWithPage:page - 1];
    [self loadScrollViewWithPage:page];
    [self loadScrollViewWithPage:page + 1];
	
    // A possible optimization would be to unload the views+controllers which are no longer visible
}

// At the begin of scroll dragging, reset the boolean used when scrolls originate from the UIPageControl
- (void)scrollViewWillBeginDragging:(UIScrollView *)scrollView {
    pageControlUsed = NO;
}

// At the end of scroll animation, reset the boolean used when scrolls originate from the UIPageControl
- (void)scrollViewDidEndDecelerating:(UIScrollView *)scrollView {
    pageControlUsed = NO;
}
- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation {
	// Return YES for supported orientations
	if ((interfaceOrientation == UIDeviceOrientationPortraitUpsideDown)||![[[NSUserDefaults standardUserDefaults] objectForKey:@"landscapeInputSupport"] boolValue]){
		return NO;
	}
	return YES;
}

#pragma mark -

@end


