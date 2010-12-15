//
//  GMItemCell.h
//  GoMagz
//
//  Created by Aladdin on 11/20/10.
//  Copyright 2010 innovation-works. All rights reserved.
//

#import <UIKit/UIKit.h>
@class GMItemModel;

@interface GMItemCell : UIButton {
	GMItemModel * item;
}

@property (nonatomic, retain) GMItemModel *item;

+ (id)itemCellWithModel:(GMItemModel*)model;

@end

