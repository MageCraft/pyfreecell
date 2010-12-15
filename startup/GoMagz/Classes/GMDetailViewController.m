    //
//  GMDetailViewController.m
//  GoMagz
//
//  Created by Aladdin on 11/20/10.
//  Copyright 2010 innovation-works. All rights reserved.
//

#import "GMDetailViewController.h"
#import "GMItemModel.h"
#import "GMWebViewController.h"
#import "UIImageView+WebCache.h"
@implementation GMDetailViewController

@synthesize imageView;
@synthesize goButton;
@synthesize description;
@synthesize nameLabel;
@synthesize typeLabel;
@synthesize regionLabel;
@synthesize priceLabel;
@synthesize item;

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
	UIButton *backBtn = [UIButton buttonWithType:UIButtonTypeCustom];  
    UIImage * selectBackImage = [[UIImage imageNamed:@"back-normal-btn.png"] stretchableImageWithLeftCapWidth:30 topCapHeight:15];  
	UIImage * normalBackImage = [[UIImage imageNamed:@"back-selected-btn.png"] stretchableImageWithLeftCapWidth:30 topCapHeight:15];
	
    [backBtn setBackgroundImage:normalBackImage forState:UIControlStateNormal];  
	[backBtn setBackgroundImage:selectBackImage forState:UIControlStateSelected];
	[backBtn setTitle:@"Back" forState:UIControlStateNormal];
	[backBtn setFont:[UIFont systemFontOfSize:14]];
    [backBtn addTarget:self action:@selector(back:) forControlEvents:UIControlEventTouchUpInside];  
    backBtn.frame = CGRectMake(0, 0, 99, 35);  
    UIBarButtonItem *cancelButton = [[[UIBarButtonItem alloc]  
									  initWithCustomView:backBtn] autorelease];  
    self.navigationItem.leftBarButtonItem = cancelButton;  
	
//	UILabel * titleLabel = [[UILabel alloc] initWithFrame:CGRectMake(0, 0, 300, 40)];
//	[titleLabel setText:@"購 物 志"];
//	[titleLabel setTextAlignment:UITextAlignmentCenter];
//	[titleLabel setFont:[UIFont boldSystemFontOfSize:30]];
//	[titleLabel setTextColor:[UIColor whiteColor]];
//	[titleLabel setBackgroundColor:[UIColor clearColor]];
//	self.navigationItem.titleView =titleLabel;
//	[titleLabel release];
	
	[self.description setText:self.item.description];
	[self.nameLabel setText:self.item.name];
	[self.typeLabel setText:self.item.type];
	[self.regionLabel setText:self.item.region];
	[self.priceLabel setText:[NSString stringWithFormat:@"RMB %@",self.item.price]];
	
	[self performSelectorInBackground:@selector(loadImage:) withObject:nil];
}
- (IBAction)loadImage:(id)sender{
	NSAutoreleasePool * pool = [[NSAutoreleasePool alloc] init];
	NSLog(@"%@",self.item.img_url);
//	UIImage * image = [UIImage imageWithData:[NSData dataWithContentsOfURL:[NSURL URLWithString:self.item.img_url]]];
	
	[self.imageView setImageWithURL:[NSURL URLWithString:self.item.img_url]
				placeholderImage:[UIImage imageNamed:@"logo.png"]];
//	UIImageView * iView = [[[UIImageView alloc] initWithImage:image] autorelease];
//	[self performSelectorOnMainThread:@selector(updateImageView:) withObject:image waitUntilDone:YES];
	[pool release];
}
//
//- (void)updateImageView:(UIImage * )image{
//	self.imageView.image = image;
//}
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
    [imageView release], imageView = nil;
    [goButton release], goButton = nil;
    [description release], description = nil;
    [nameLabel release], nameLabel = nil;
    [typeLabel release], typeLabel = nil;
    [regionLabel release], regionLabel = nil;
    [priceLabel release], priceLabel = nil;
    [item release], item = nil;
    [super dealloc];
}
- (IBAction) actionToWeb:(id)sender{
	GMWebViewController * webVC = [[[GMWebViewController alloc] initWithNibName:@"GMWebViewController" bundle:[NSBundle mainBundle]] autorelease];
	webVC.modalPresentationStyle = UIModalPresentationPageSheet;
	webVC.url = self.item.link;
	[self presentModalViewController:webVC animated:YES];
}

@end








