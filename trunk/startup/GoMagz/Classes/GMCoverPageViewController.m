    //
//  GMCoverPageViewController.m
//  GoMagz
//
//  Created by Aladdin on 11/20/10.
//  Copyright 2010 innovation-works. All rights reserved.
//

#import "GMCoverPageViewController.h"
#import "GMItemListViewController.h"
#import "GMRectButton.h"
#import "GMConstants.h"
#import "NSString+SBJSON.h"
#import "GMTopicItemModel.h"
#import "GoMagzAppDelegate.h"
#import "GMTopicTitleView.h"
#import "GMItemPagesViewController.h"
@implementation GMCoverPageViewController

@synthesize btn;
@synthesize isInScreen;
@synthesize maskView;
@synthesize curIndex;
@synthesize logoImageView;
@synthesize backgroundImageView;
@synthesize coverModel;
@synthesize networkQueue;

 // The designated initializer.  Override if you create the controller programmatically and want to perform customization that is not appropriate for viewDidLoad.
- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil {
    if ((self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil])) {
        // Custom initialization
	}
    return self;
}
- (void)loadView{
	[super loadView];
}
- (UIImage *)getCurBackground:(NSInteger)index{
	if (index<0) {
		index+=3;
	}
	if (index>=[((GoMagzAppDelegate*)[[UIApplication sharedApplication] delegate]).cacheItemsArray count]) {
		index = index %[((GoMagzAppDelegate*)[[UIApplication sharedApplication] delegate]).cacheItemsArray count];
	}
	NSLog(@"%@",[NSString stringWithFormat:@"fm_0%d.png",index]);
	UIImage * image = [UIImage imageNamed:[NSString stringWithFormat:@"fm_0%d.png",index]];
	
		self.curIndex ++;
	if (self.curIndex>=3) {
		self.curIndex -=3;
	}
	return image;
}

- (GMTopicItemModel*)getCurBackgroundModel:(NSInteger)index{
	if (index<0) {
		index+=3;
	}
	if (index>=[((GoMagzAppDelegate*)[[UIApplication sharedApplication] delegate]).cacheItemsArray count]) {
		index = index %[((GoMagzAppDelegate*)[[UIApplication sharedApplication] delegate]).cacheItemsArray count];
	}
	GMTopicItemModel* model =[((GoMagzAppDelegate*)[[UIApplication sharedApplication] delegate]).cacheItemsArray objectAtIndex:self.curIndex];
	NSLog(@"%@",[NSString stringWithFormat:@"Model : fm_0%d.png",index]);
	return model;
}

// Implement viewDidLoad to do additional setup after loading the view, typically from a nib.
- (void)viewDidLoad {
	[super viewDidLoad];
	[[NSNotificationCenter defaultCenter]addObserver:self selector:@selector(animationBackground:) name:@"DownLoad OK" object:nil];
	[self.navigationController setNavigationBarHidden:YES animated:NO];
#pragma mark Aladdin
	
	[self performSelectorInBackground:@selector(requestItemList:) withObject:nil];
	
//	[self performSelectorInBackground:@selector(requestItemListFromLocal:) withObject:nil];
	
	self.curIndex = 0;
	UIImage * backgroundImage = [UIImage imageNamed:@"Default.png"];
	self.backgroundImageView = [[UIImageView alloc] initWithImage:backgroundImage];
	self.backgroundImageView.frame = CGRectMake(0, 0, backgroundImage.size.width, backgroundImage.size.height);	
	[self.view addSubview:self.backgroundImageView];
	[backgroundImageView release];
	[backgroundImage release];
	
	
	
//	GMRectButton * btn = [GMRectButton rectButtonWithTarget:self andSelector:@selector(actionToItemList:) andTitle:@"查看商品列表" andColor:[UIColor darkGrayColor]];
//	btn.center = CGPointMake(200, 800);
//	[self.view addSubview:btn];
	
	
	self.view.backgroundColor  = [UIColor redColor];
	
	
	self.maskView = [[UIView alloc] initWithFrame:CGRectMake(0, 0, 768, 1024)];
	self.maskView.center = CGPointMake(384, self.maskView.center.y);
	self.maskView.backgroundColor = [UIColor blackColor];
	[self.view addSubview:self.maskView];
	[self.maskView release];
	
	
	UIImage * logoImage = [UIImage imageNamed:@"logo.png"];
	self.logoImageView = [[UIImageView alloc] initWithImage:logoImage];
	self.logoImageView.frame = CGRectMake(28, 28, logoImage.size.width,  logoImage.size.height);
	[self.view addSubview:self.logoImageView];
	
	[[NSNotificationCenter defaultCenter] addObserver:self selector:@selector(notificationToPage:) name:@"CoverTitleSelector" object:nil];
	
	self.btn =[UIButton buttonWithType:UIButtonTypeCustom];
	[btn addTarget:self action:@selector(notificationToPage:) forControlEvents:UIControlEventTouchUpInside];
	btn.frame = CGRectMake(0,600,768,424);
	[self.view addSubview:btn];
}

- (void)requestItemListFromLocal:(id)sender{
	NSAutoreleasePool * pool = [[NSAutoreleasePool alloc] init];
	NSData *jsonData = [NSData dataWithContentsOfFile:[[NSBundle mainBundle]pathForResource:@"demo" ofType:@"go"]];
		NSLog(@"%@",jsonData);
	NSArray * topicArray = [[[NSString alloc] initWithBytes:[jsonData bytes] length:[jsonData length] encoding:NSUTF8StringEncoding] JSONValue];
	//	NSLog(@"%@",[topicArray objectAtIndex:0]);
	
	for (NSDictionary * topicItemDictionary in topicArray) {
		GMTopicItemModel * topicModel =[GMTopicItemModel topicItemWithDictionary:topicItemDictionary];
		NSLog(@"%@ ",topicModel);
		[((GoMagzAppDelegate*)[[UIApplication sharedApplication] delegate]).cacheItemsArray addObject:topicModel];
	}
	[[NSNotificationCenter defaultCenter] postNotificationName:@"DownLoad OK" object:nil];
	
	[pool release];
	
}

- (void)notificationToPage:(id)n{
	GMItemListViewController * itemListVC = [[GMItemListViewController alloc] initWithNibName:@"GMItemListViewController" bundle:[NSBundle mainBundle]];
	NSInteger topicIndex = self.curIndex;
	if ([n isKindOfClass:[NSNotification class]]) {
		topicIndex = [[[(NSNotification*)n userInfo] objectForKey:@"topicIndex"] intValue];
	}
	if ([n isKindOfClass:[UIButton class]]) {
		topicIndex = self.curIndex;
	}

	[self.navigationController pushViewController:itemListVC animated:YES];
	
	[itemListVC.pages loadScrollViewWithPage:topicIndex];
	[itemListVC autorelease];
}

- (IBAction) animationBackground:(NSNotification*)n{
	NSAutoreleasePool * pool = [[NSAutoreleasePool alloc] init];
	GMTopicTitleView * coverTitleView = [GMTopicTitleView coverViewWithModel:[self getCurBackgroundModel:self.curIndex]];
	coverTitleView.TopicIndex = self.curIndex;
	coverTitleView.alpha = 0.0;
	coverTitleView.center = CGPointMake(coverTitleView.center.x+29, coverTitleView.center.y+623);
	[self.view addSubview:coverTitleView];
	[self.view bringSubviewToFront:self.btn];
	self.backgroundImageView.image = [self getCurBackground:self.curIndex];
	[UIView beginAnimations:@"coverTitleViewIn" context:coverTitleView];
	[UIView setAnimationDelegate:self];
	[UIView setAnimationDidStopSelector:@selector(animationDidStop:finished:context:)];
	[UIView setAnimationDuration:0.5];
	self.maskView.center = CGPointMake(1152, self.maskView.center.y); 
	coverTitleView.alpha = 1.0;
	[UIView commitAnimations];
	[pool release];
}

- (void)viewWillAppear:(BOOL)animated{
	[super viewWillAppear:animated];
	self.isInScreen = YES;
	if ([((GoMagzAppDelegate*)[[UIApplication sharedApplication] delegate]).cacheItemsArray count]>0) {
		[self animationBackground:nil];
	}
	[self.navigationController setNavigationBarHidden:YES animated:NO];
}
- (void)viewWillDisappear:(BOOL)animated{
	[super viewWillDisappear:animated];
	self.isInScreen = NO;
}
- (void) animationDidStop:(NSString *)animationID finished:(NSNumber *)finished context:(void *)context{
	
	if ([animationID isEqualToString:@"coverTitleViewIn"]) {
		self.maskView.center = CGPointMake(-384, self.maskView.center.y);
		GMTopicTitleView * coverTitleView = (GMTopicTitleView*)context;
		
		[UIView beginAnimations:@"coverTitleViewOut" context:coverTitleView];
		[UIView setAnimationDelegate:self];
		[UIView setAnimationDelay:2.0];
		[UIView setAnimationDidStopSelector:@selector(animationDidStop:finished:context:)];
		[UIView setAnimationDuration:0.3];
		self.maskView.center = CGPointMake(384, self.maskView.center.y); 
		coverTitleView.alpha = 0.0;
		[UIView commitAnimations];
	}
	if ([animationID isEqualToString:@"coverTitleViewOut"]) {
		self.maskView.center = CGPointMake(384, self.maskView.center.y);
		GMTopicTitleView * coverTitleView = (GMTopicTitleView*)context;
		[coverTitleView removeFromSuperview];
		coverTitleView = nil;
		if (self.isInScreen) {
			coverTitleView = [GMTopicTitleView coverViewWithModel:[self getCurBackgroundModel:self.curIndex]];
			coverTitleView.TopicIndex = self.curIndex;
			coverTitleView.alpha = 0.0;
			coverTitleView.center = CGPointMake(coverTitleView.center.x+29, coverTitleView.center.y+623);
			[self.view addSubview:coverTitleView];
			[self.view bringSubviewToFront:self.btn];
			self.backgroundImageView.image = [self getCurBackground:self.curIndex];
			[UIView beginAnimations:@"coverTitleViewIn" context:coverTitleView];
			[UIView setAnimationDelegate:self];
			[UIView setAnimationDelay:0.5];
			[UIView setAnimationDidStopSelector:@selector(animationDidStop:finished:context:)];
			[UIView setAnimationDuration:0.3];
			self.maskView.center = CGPointMake(1152, self.maskView.center.y); 
			coverTitleView.alpha = 1.0;
			[UIView commitAnimations];
		}
	}
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
	self.backgroundImageView = nil;
    [super viewDidUnload];
    // Release any retained subviews of the main view.
    // e.g. self.myOutlet = nil;
}


- (void)dealloc {
	[btn release], btn = nil;
	[maskView release], maskView = nil;
	[[NSNotificationCenter defaultCenter] removeObserver:self name:@"CoverTitleSelector" object:nil];
	[[NSNotificationCenter defaultCenter] removeObserver:self name:@"DownLoad OK" object:nil];
	
	[logoImageView release], logoImageView = nil;
	[networkQueue cancelAllOperations];
	[networkQueue release];
	networkQueue = nil;
	
	[backgroundImageView release];
    [super dealloc];
}

#pragma mark actions
#pragma mark -
- (IBAction) actionToItemList:(id)sender{
	GMItemListViewController * itemListVC = [[GMItemListViewController alloc] initWithNibName:@"GMItemListViewController" bundle:[NSBundle mainBundle]];
	[self.navigationController pushViewController:itemListVC animated:YES];
	[itemListVC release];
}

- (IBAction)requestItemList:(id)sender{
	NSAutoreleasePool * pool = [[NSAutoreleasePool alloc] init];
	NSURL * itemListURL = [NSURL URLWithString:kItemListURL];
	
	[networkQueue cancelAllOperations];
	networkQueue = [ASINetworkQueue queue];
	[networkQueue retain];
	networkQueue.delegate = self;
	networkQueue.requestDidFinishSelector = @selector(requestFinished:);
	networkQueue.requestDidFailSelector = @selector(actorRequestFailed:);
	networkQueue.queueDidFinishSelector = nil;
	
	getActorMoviesRequest = [ASIHTTPRequest requestWithURL:itemListURL];
	
	[networkQueue addOperation:getActorMoviesRequest];
	[networkQueue go];
	[pool release];
}
- (void)actorRequestFailed:(ASIHTTPRequest *)inRequest;
{
	NSAutoreleasePool * pool = [[NSAutoreleasePool alloc] init];
	NSLog(@"ItemList request timed out or cancelled");
	[pool release];
}

- (void)requestFinished:(ASIHTTPRequest *)inRequest;
{
	NSAutoreleasePool * pool = [[NSAutoreleasePool alloc] init];
	NSData *jsonData = [inRequest responseData];
//	NSLog(@"%@",jsonData);
	NSArray * topicArray = [[[NSString alloc] initWithBytes:[jsonData bytes] length:[jsonData length] encoding:NSUTF8StringEncoding] JSONValue];
//	NSLog(@"%@",[topicArray objectAtIndex:0]);

	for (NSDictionary * topicItemDictionary in topicArray) {
		GMTopicItemModel * topicModel =[GMTopicItemModel topicItemWithDictionary:topicItemDictionary];
		NSLog(@"%@ ",topicModel);
		[((GoMagzAppDelegate*)[[UIApplication sharedApplication] delegate]).cacheItemsArray addObject:topicModel];
	}
	[[NSNotificationCenter defaultCenter] postNotificationName:@"DownLoad OK" object:nil];
	[pool release];
}
#pragma mark -
@end






