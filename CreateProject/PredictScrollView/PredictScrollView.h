
#import <UIKit/UIKit.h>


//
@class PredictScrollView;
@protocol PredictScrollViewDelegate <NSObject>
@required
- (UIView *)scrollView:(PredictScrollView *)scrollView viewForPage:(NSUInteger)index inFrame:(CGRect)frame;
- (void)scrollView:(PredictScrollView *)scrollView scrollToPage:(NSUInteger)index;
@end


//
@interface PredictScrollView : UIScrollView <UIScrollViewDelegate>
{
	BOOL _bIgnore;
	NSUInteger _itemPage;
	NSUInteger _numberOfPages;
}

- (void)freePages:(BOOL)force;
//doing :
- (void)loadPage:(NSUInteger)index;
@property(nonatomic,readonly) UIView * __autoreleasing *pages;
@property(nonatomic,assign) NSUInteger currentPage;
@property(nonatomic,assign) NSUInteger numberOfPages;
@property(nonatomic,weak) id<PredictScrollViewDelegate> delegate2;

@end


//
@interface PageControlScrollView : PredictScrollView
{
	BOOL _hasParent;
	UIPageControl *_pageCtrl;
}

- (void) updateDots;



@property(nonatomic,readonly) UIPageControl *pageCtrl;
@end
