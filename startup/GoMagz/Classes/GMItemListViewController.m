    //
//  GMItemListViewController.m
//  GoMagz
//
//  Created by Aladdin on 11/20/10.
//  Copyright 2010 innovation-works. All rights reserved.
//

#import "GMItemListViewController.h"
#import "GMDetailViewController.h"
#import "GMItemPagesViewController.h"
#import "GMItemCell.h"
@implementation GMItemListViewController

@synthesize toPage;
@synthesize pages;


 // The designated initializer.  Override if you create the controller programmatically and want to perform customization that is not appropriate for viewDidLoad.
- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil {
    if ((self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil])) {
        // Custom initialization
		self.pages = [[GMItemPagesViewController alloc] initWithNibName:@"GMItemPagesViewController" bundle:[NSBundle mainBundle]];
		self.toPage = -1;
    }
    return self;
}


// Implement viewDidLoad to do additional setup after loading the view, typically from a nib.
- (void)viewDidLoad {
    [super viewDidLoad];
	[[NSNotificationCenter defaultCenter] addObserver:self selector:@selector(actionToDetailView:) name:@"GoToItemDetail" object:nil];
	[self.navigationController setNavigationBarHidden:NO animated:NO];
	
	// Add Back Bar Button  
    UIButton *backBtn = [UIButton buttonWithType:UIButtonTypeCustom];  
    UIImage * selectBackImage = [[UIImage imageNamed:@"back-normal-btn.png"] stretchableImageWithLeftCapWidth:30 topCapHeight:15];  
	UIImage * normalBackImage = [[UIImage imageNamed:@"back-selected-btn.png"] stretchableImageWithLeftCapWidth:30 topCapHeight:15];
	
    [backBtn setBackgroundImage:normalBackImage forState:UIControlStateNormal];  
	[backBtn setBackgroundImage:selectBackImage forState:UIControlStateSelected];
	[backBtn setFont:[UIFont systemFontOfSize:14]];
	[backBtn setTitle:@"Back" forState:UIControlStateNormal];

    [backBtn addTarget:self action:@selector(back:) forControlEvents:UIControlEventTouchUpInside];  
    backBtn.frame = CGRectMake(0, 0, 99, 35);  
    UIBarButtonItem *cancelButton = [[[UIBarButtonItem alloc]  
									  initWithCustomView:backBtn] autorelease];  
    self.navigationItem.leftBarButtonItem = cancelButton;  
	
	//UILabel * titleLabel = [[UILabel alloc] initWithFrame:CGRectMake(0, 0, 300, 40)];
//	[titleLabel setText:@"購 物 志"];
//	[titleLabel setTextAlignment:UITextAlignmentCenter];
//	[titleLabel setFont:[UIFont boldSystemFontOfSize:30]];
//	[titleLabel setTextColor:[UIColor whiteColor]];
//	[titleLabel setBackgroundColor:[UIColor clearColor]];
//	self.navigationItem.titleView =titleLabel;
//	[titleLabel release];
	
	if (self.toPage !=-1) {
		self.pages.toPage = self.toPage;
	}
	
	[self.view addSubview:pages.view];
}

- (IBAction)back:(id)sender{
	NSAutoreleasePool * pool = [[NSAutoreleasePool alloc] init];	
	[self.navigationController popViewControllerAnimated:YES];
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
	[pages release], pages = nil;
	[[NSNotificationCenter defaultCenter] removeObserver:self name:@"GoToItemDetail" object:nil];
    [super dealloc];
}
#pragma mark -
- (IBAction)actionToDetailView:(NSNotification*)n{
	NSAutoreleasePool * pool = [[NSAutoreleasePool alloc] init];
	NSLog(@"%@",n);
	
	GMItemModel * model = [[n userInfo] objectForKey:@"GMItemModel"];
	GMDetailViewController * detailViewController = [[GMDetailViewController alloc] initWithNibName:@"GMDetailViewController" bundle:[NSBundle mainBundle]];
	detailViewController.item = model;
	[self.navigationController pushViewController:detailViewController animated:YES];
	[detailViewController release];
	[pool release];
}
#pragma mark -


@end


