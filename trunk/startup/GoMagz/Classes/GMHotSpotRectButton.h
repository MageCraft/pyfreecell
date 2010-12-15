//
//  GMHotSpotRectButton.h
//  GoMagz
//
//  Created by Aladdin on 11/21/10.
//  Copyright 2010 innovation-works. All rights reserved.
//

#import <UIKit/UIKit.h>
@class 	GMItemModel;

@interface GMHotSpotRectButton : UIButton {
		GMItemModel * item;
}

@property (nonatomic, retain) GMItemModel *item;

+ (id)rectButtonCellWithModel:(GMItemModel*)model andFrame:(CGRect)rect;
@end

