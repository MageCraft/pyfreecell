//
//  GMDetailViewController.h
//  GoMagz
//
//  Created by Aladdin on 11/20/10.
//  Copyright 2010 innovation-works. All rights reserved.
//

#import <UIKit/UIKit.h>
@class GMItemModel;

@interface GMDetailViewController : UIViewController <UITextViewDelegate>{
	GMItemModel * item;
	
	UILabel		* priceLabel;
	UILabel		* regionLabel;
	UILabel		* typeLabel;
	UILabel		* nameLabel;
	UITextView	* description;
	UIButton	* goButton;
	UIImageView	* imageView;
}

@property (nonatomic, retain) IBOutlet UIImageView *imageView;
@property (nonatomic, retain) IBOutlet UIButton *goButton;
@property (nonatomic, retain) IBOutlet UITextView *description;
@property (nonatomic, retain) IBOutlet UILabel *nameLabel;
@property (nonatomic, retain) IBOutlet UILabel *typeLabel;
@property (nonatomic, retain) IBOutlet UILabel *regionLabel;
@property (nonatomic, retain) IBOutlet UILabel *priceLabel;
@property (nonatomic, retain) GMItemModel *item;

- (IBAction) actionToWeb:(id)sender;
@end


