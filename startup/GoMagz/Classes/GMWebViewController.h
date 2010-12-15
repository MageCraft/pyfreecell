//
//  GMWebViewController.h
//  GoMagz
//
//  Created by Aladdin on 11/21/10.
//  Copyright 2010 innovation-works. All rights reserved.
//

#import <UIKit/UIKit.h>


@interface GMWebViewController : UIViewController <UIWebViewDelegate>{
	UIWebView * webView;
	NSString * url;
}

@property (nonatomic, copy) NSString *url;
@property (nonatomic, retain) IBOutlet UIWebView *webView;

- (IBAction)closeWeb:(id)sender;
@end


