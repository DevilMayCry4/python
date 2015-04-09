
#import <UIKit/UIKit.h>
@class AFHTTPRequestOperation;
@class AFImageResponseSerializer;

//
@interface DelayImageView: UIImageView
{
    AFHTTPRequestOperation *_request;
    AFImageResponseSerializer *_serializer;
	BOOL _force;
	BOOL _loaded;
	NSString *_url;
	NSString *_def;
	UIActivityIndicatorView *_activityView;
    
    BOOL _down;
	id _target;
	SEL _action;
    UIImageView *overlay;
    BOOL _selected;
    
}

- (id)initWithUrl:(NSString *)url frame:(CGRect)frame;
- (void)addTarget:(id)target action:(SEL)action;
- (void)setClickOverlayMask:(UIImage *)mask;

@property (nonatomic,retain) NSString *url;
@property (nonatomic,retain) NSString *def; 
@property (nonatomic) BOOL down;
@property (nonatomic) BOOL selected;
@property (nonatomic,assign) UIButton *sender;
@end

