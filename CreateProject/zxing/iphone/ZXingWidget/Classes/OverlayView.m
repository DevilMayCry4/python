// -*- Mode: ObjC; tab-width: 2; indent-tabs-mode: nil; c-basic-offset: 2 -*-

/**
 * Copyright 2009 Jeff Verkoeyen
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#import "OverlayView.h"

static const CGFloat kPadding = 50;
static const CGFloat kLicenseButtonPadding = 10;

@interface OverlayView()
@property (nonatomic,assign) UIButton *cancelButton;
@property (nonatomic,assign) UIButton *licenseButton;
@property (nonatomic,retain) UILabel *instructionsLabel;
@end


@implementation OverlayView

@synthesize delegate, oneDMode;
@synthesize points = _points;
@synthesize cancelButton;
@synthesize licenseButton;
@synthesize cropRect;
@synthesize instructionsLabel;
@synthesize displayedMessage;
@synthesize cancelButtonTitle;
@synthesize cancelEnabled;

#define kScaneWidth 400
#define kOffy (self.frame.size.height - kScaneWidth)/2
#define kOffx (self.frame.size.width - kScaneWidth)/2
////////////////////////////////////////////////////////////////////////////////////////////////////
- (id)initWithFrame:(CGRect)theFrame cancelEnabled:(BOOL)isCancelEnabled oneDMode:(BOOL)isOneDModeEnabled {
  return [self initWithFrame:theFrame cancelEnabled:isCancelEnabled oneDMode:isOneDModeEnabled showLicense:YES];
}

- (id) initWithFrame:(CGRect)theFrame cancelEnabled:(BOOL)isCancelEnabled oneDMode:(BOOL)isOneDModeEnabled showLicense:(BOOL)showLicenseButton {
  self = [super initWithFrame:theFrame];
  if( self ) {

    CGFloat rectSize = self.frame.size.width - kPadding * 2;
    if (!oneDMode) {
      cropRect = CGRectMake(kPadding, kPadding*2 , rectSize, rectSize);
    } else {
      CGFloat rectSize2 = self.frame.size.height - kPadding * 2;
      cropRect = CGRectMake(kPadding, kPadding, rectSize, rectSize2);
    }
      self.backgroundColor = [UIColor colorWithWhite:0 alpha:0.6];
    self.oneDMode = isOneDModeEnabled;
      
    if (showLicenseButton) {
        self.licenseButton = [UIButton buttonWithType:UIButtonTypeInfoLight];
        
        CGRect lbFrame = [licenseButton frame];
        lbFrame.origin.x = self.frame.size.width - licenseButton.frame.size.width - kLicenseButtonPadding;
        lbFrame.origin.y = self.frame.size.height - licenseButton.frame.size.height - kLicenseButtonPadding;
        [licenseButton setFrame:lbFrame];
        [licenseButton addTarget:self action:@selector(showLicenseAlert:) forControlEvents:UIControlEventTouchUpInside];
        
        [self addSubview:licenseButton];
    }
    self.cancelEnabled = isCancelEnabled;

    if (self.cancelEnabled) {
      UIButton *butt = [UIButton buttonWithType:UIButtonTypeRoundedRect];
      self.cancelButton = butt;
      if ([self.cancelButtonTitle length] > 0 ) {
        [cancelButton setTitle:self.cancelButtonTitle forState:UIControlStateNormal];
      } else {
        [cancelButton setTitle:NSLocalizedStringWithDefaultValue(@"OverlayView cancel button title", nil, [NSBundle mainBundle], @"Cancel", @"Cancel") forState:UIControlStateNormal];
      }
      [cancelButton addTarget:self action:@selector(cancel:) forControlEvents:UIControlEventTouchUpInside];
      [self addSubview:cancelButton];
    }
      
      _infoLabel = [[UILabel alloc] initWithFrame:CGRectMake(0,kOffy + kScaneWidth + 30, CGRectGetWidth(self.frame), 14)];
      _infoLabel.textAlignment = NSTextAlignmentCenter;
      _infoLabel.backgroundColor = [UIColor clearColor];
      _infoLabel.textColor = [UIColor whiteColor];
      _infoLabel.adjustsFontSizeToFitWidth = YES;
      _infoLabel.font = [UIFont systemFontOfSize:16];
      _infoLabel.text = _infoString;
      [self addSubview:_infoLabel];
      [_infoLabel release];
    
      _lineView = [[UIView alloc] initWithFrame:CGRectMake(kOffx, kOffy,  kScaneWidth, 2)];
      _lineView.backgroundColor = [UIColor greenColor];
      [self addSubview:_lineView];
      [_lineView release];
      
  }
  return self;
}

- (void)didMoveToSuperview
{
    [self startAnimation];
}

- (void)startAnimation
{
    [UIView animateWithDuration:1
                     animations:^{
                         CGRect frame = _lineView.frame;
                         if (frame.origin.y == kOffy)
                         {
                             frame.origin.y = kOffy  + frame.size.width;
                         }
                         else
                         {
                             frame.origin.y = kOffy ;
                         }
                         _lineView.frame = frame;
                     }
                     completion:^(BOOL finish){
                         if (self.superview)
                         {
                             [self startAnimation];
                         }
                     }];
}

- (void)cancel:(id)sender {
	// call delegate to cancel this scanner
	if (delegate != nil) {
		[delegate cancelled];
	}
}

- (void)showLicenseAlert:(id)sender {
    NSString *title =
        NSLocalizedStringWithDefaultValue(@"OverlayView license alert title", nil, [NSBundle mainBundle], @"License", @"License");

    NSString *message =
        NSLocalizedStringWithDefaultValue(@"OverlayView license alert message", nil, [NSBundle mainBundle], @"Scanning functionality provided by ZXing library, licensed under Apache 2.0 license.", @"Scanning functionality provided by ZXing library, licensed under Apache 2.0 license.");

    NSString *cancelTitle =
        NSLocalizedStringWithDefaultValue(@"OverlayView license alert cancel title", nil, [NSBundle mainBundle], @"OK", @"OK");

    NSString *viewTitle =
        NSLocalizedStringWithDefaultValue(@"OverlayView license alert view title", nil, [NSBundle mainBundle], @"View License", @"View License");

    UIAlertView *av =
        [[UIAlertView alloc] initWithTitle:title message:message delegate:self cancelButtonTitle:cancelTitle otherButtonTitles:viewTitle, nil];

    [av show];
    [self retain]; // For the delegate callback ...
    [av release];
}

- (void)alertView:(UIAlertView *)alertView clickedButtonAtIndex:(NSInteger)buttonIndex {
  if (buttonIndex == [alertView firstOtherButtonIndex]) {
    [[UIApplication sharedApplication] openURL:[NSURL URLWithString:@"http://www.apache.org/licenses/LICENSE-2.0.html"]];
  }
  [self release];
}

////////////////////////////////////////////////////////////////////////////////////////////////////
- (void) dealloc {
    
    [_infoString release];
  [_points release];
  [instructionsLabel release];
  [displayedMessage release];
  [cancelButtonTitle release],
	[super dealloc];
}


- (void)drawRect:(CGRect)rect inContext:(CGContextRef)context {
	CGContextBeginPath(context);
	CGContextMoveToPoint(context, rect.origin.x, rect.origin.y);
	CGContextAddLineToPoint(context, rect.origin.x + rect.size.width, rect.origin.y);
	CGContextAddLineToPoint(context, rect.origin.x + rect.size.width, rect.origin.y + rect.size.height);
	CGContextAddLineToPoint(context, rect.origin.x, rect.origin.y + rect.size.height);
	CGContextAddLineToPoint(context, rect.origin.x, rect.origin.y);
	CGContextStrokePath(context);
}

- (CGPoint)map:(CGPoint)point {
    CGPoint center;
    center.x = cropRect.size.width/2;
    center.y = cropRect.size.height/2;
    float x = point.x - center.x;
    float y = point.y - center.y;
    int rotation = 90;
    switch(rotation) {
    case 0:
        point.x = x;
        point.y = y;
        break;
    case 90:
        point.x = -y;
        point.y = x;
        break;
    case 180:
        point.x = -x;
        point.y = -y;
        break;
    case 270:
        point.x = y;
        point.y = -x;
        break;
    }
    point.x = point.x + center.x;
    point.y = point.y + center.y;
    return point;
}

#define kTextMargin 10

////////////////////////////////////////////////////////////////////////////////////////////////////
- (void)drawRect:(CGRect)rect {
	[super drawRect:rect];
   
    CGContextRef context = UIGraphicsGetCurrentContext();
    CGRect drawFrame = CGRectMake(kOffx, kOffy, kScaneWidth, kScaneWidth);
    CGContextSetStrokeColorWithColor(context, [UIColor greenColor].CGColor);
    CGContextAddRect(context, drawFrame);
    CGContextSetLineWidth(context, 0.5);
 
    CGContextClearRect(context,  drawFrame);
 
    CGContextSetFillColorWithColor(context, [UIColor greenColor].CGColor);
    for (int a = 0; a < 4; a ++)
    {
        CGRect frame = CGRectMake(0, 0, 16, 16);
        frame.origin.x = a%2 == 0 ? CGRectGetMinX(drawFrame) : CGRectGetMaxX(drawFrame) - 16;
        frame.origin.y = a/2 == 0 ?  CGRectGetMinY(drawFrame) : CGRectGetMaxY(drawFrame) - 16;
        
        CGContextFillRect(context, frame);
        
        frame.origin.x  += a%2 == 0 ? 4 : 0;
        frame.origin.y  += a/2 == 0 ? 4 : 0;
        frame.size.width -= 4;
        frame.size.height -= 4;
        CGContextClearRect(context, frame);
    }
}


////////////////////////////////////////////////////////////////////////////////////////////////////
- (void) setPoints:(NSMutableArray*)pnts {
    [pnts retain];
    [_points release];
    _points = pnts;
	
    if (pnts != nil) {
        self.backgroundColor = [UIColor colorWithWhite:1.0 alpha:0.25];
    }
    [self setNeedsDisplay];
}

- (void) setPoint:(CGPoint)point {
    if (!_points) {
        _points = [[NSMutableArray alloc] init];
    }
    if (_points.count > 3) {
        [_points removeObjectAtIndex:0];
    }
    [_points addObject:[NSValue valueWithCGPoint:point]];
    [self setNeedsDisplay];
}


- (void)layoutSubviews {
  [super layoutSubviews];
    _infoLabel.text = _infoString;
  if (cancelButton) {
    if (oneDMode) {
      [cancelButton setTransform:CGAffineTransformMakeRotation(M_PI/2)];
      [cancelButton setFrame:CGRectMake(20, 175, 45, 130)];
    } else {
      CGSize theSize = CGSizeMake(100, 50);
      CGRect rect = self.frame;
      CGRect theRect = CGRectMake((rect.size.width - theSize.width) / 2, cropRect.origin.y + cropRect.size.height + 20, theSize.width, theSize.height);
      [cancelButton setFrame:theRect];
    }
  }
}

@end
