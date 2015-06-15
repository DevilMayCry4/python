//
//  Draw.m
//  test
//
//  Created by virgil on 15-6-1.
//  Copyright (c) 2015年 xtownmobile. All rights reserved.
//

#import "Draw.h"

@implementation Draw

#define ToRadian(radian)            (radian*(M_PI/180.0))
 
- (void)drawRect:(CGRect)rect{
    CGContextRef ctx = UIGraphicsGetCurrentContext();
    CGPoint center = CGPointMake(self.bounds.size.width/2, self.bounds.size.height/2);
    CGFloat radius = MIN(center.x, center.y) - 5;
     CGContextSetLineWidth(ctx, 10);
    CGContextBeginPath(ctx);
    
    CGContextAddArc(ctx, center.x, center.y, radius, 0, ToRadian(45), NO);
    CGContextSetStrokeColorWithColor(ctx, [UIColor redColor].CGColor);
    CGContextDrawPath(ctx, kCGPathStroke);
    CGContextAddArc(ctx, center.x, center.y, radius, ToRadian(45) + ToRadian(2), ToRadian(90), NO);
    CGContextSetStrokeColorWithColor(ctx, [UIColor blueColor].CGColor);
     CGContextDrawPath(ctx, kCGPathStroke);
    
    CGContextAddArc(ctx, center.x, center.y, radius, ToRadian(90) + ToRadian(2), ToRadian(270), NO);
    CGContextSetStrokeColorWithColor(ctx, [UIColor greenColor].CGColor);
    
    CGContextDrawPath(ctx, kCGPathStroke);
    
    CGContextAddArc(ctx, center.x, center.y, radius, ToRadian(270) + ToRadian(2), ToRadian(290), NO);
    CGContextSetStrokeColorWithColor(ctx, [UIColor greenColor].CGColor);
    
    CGContextDrawPath(ctx, kCGPathStroke);
}
@end
