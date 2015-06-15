

//
//  PullController.m
//  InfoClouds
//
//  Created by virgil on 13-6-25.
//  Copyright (c) 2013年 XtownMobile. All rights reserved.
//

#import "PullController.h"
#import "EGORefreshTableHeaderView.h"
#import "EGORefreshTableFooterView.h"

#define Load_Height 20
#define OFF 5.0
#define LoadingMoreString @"正在加载更多"

@implementation LoadingFooter

- (id)initWithFrame:(CGRect)frame
{
    self = [super initWithFrame:frame];
    if(self)
    {
        self.backgroundColor =  [UIColor clearColor];
        
        _indicator = [[UIActivityIndicatorView alloc] initWithActivityIndicatorStyle:UIActivityIndicatorViewStyleGray];
        [self addSubview:_indicator];
        CGSize size = [LoadingMoreString boundingRectWithSize:CGSizeMake(CGRectGetWidth(frame), 100) options:NSStringDrawingUsesLineFragmentOrigin attributes:@{NSFontAttributeName:[UIFont systemFontOfSize:16]} context:nil].size;
        CGRect tmp = _indicator.frame;
        tmp.origin.x =( CGRectGetWidth(frame) -  tmp.size.width - size.width - OFF)/2 ;
        tmp.origin.y = 10;
        _indicator.frame = tmp;
        _indicator.hidesWhenStopped = YES;
        [_indicator startAnimating];
        
        _infoLabel = [[UILabel alloc] initWithFrame:CGRectMake(CGRectGetMaxX(_indicator.frame) + OFF, 10, CGRectGetWidth(frame)/2, 20)];
        _infoLabel.text = LoadingMoreString;
        _infoLabel.backgroundColor = [UIColor clearColor];
        _infoLabel.textColor = [UIColor grayColor];
        _infoLabel.font = [UIFont systemFontOfSize:16];
        [self addSubview:_infoLabel];
        
        
    }
    return self;
}
@end

@interface PullController ()

@property (nonatomic,retain) id result;

@end

@implementation PullController

- (id)init
{
    self = [super init];
    if (self)
    {
        _refreshIfViewAppear = YES;
    }
    return self;
}

- (id)initAsScroll:(BOOL)scroll
{
    self = [super init];
    if (self)
    {
        _scroll = scroll;
    }
    return self;
}

- (void)viewDidLoad
{
    [super viewDidLoad];
    if (_scroll)
    {
        _tableView = (id)[[UIScrollView alloc] initWithFrame:CGRectMake(0, 0, CGRectGetWidth(self.view.frame), CGRectGetHeight(self.view.frame) )];
        _tableView.alwaysBounceVertical = YES;
    }
    else
    {
        _tableView = [[UITableView alloc] initWithFrame:CGRectMake(0, 0, CGRectGetWidth(self.view.frame), CGRectGetHeight(self.view.frame) )];
        _tableView.dataSource = self;
    }
    
    _tableView.delegate  = self;
    _tableView.autoresizingMask = UIViewAutoresizingFlexibleHeight | UIViewAutoresizingFlexibleWidth;
    [self.view addSubview:_tableView];
    
    [self createHeaderView];
    [_tableView addObserver:self forKeyPath:@"frame" options:NSKeyValueObservingOptionNew context:NULL];
    
}

- (void)observeValueForKeyPath:(NSString *)keyPath ofObject:(id)object change:(NSDictionary *)change context:(void *)context
{
    if (object == _tableView && [keyPath isEqualToString: @"frame"])
    {
        if (_more)
        {
            [self setFooterView];
        }
    }
}

//页面重新出现的时候、判断是否需要刷新
- (void)viewDidAppear:(BOOL)animated
{
    [super viewDidAppear:animated];
    if (!_reloading && _refreshIfViewAppear && !_disappear)
    {
        [self showRefreshHeader:YES];
    }
    _disappear = NO;
}

- (void)viewWillDisappear:(BOOL)animated
{
    [super viewWillDisappear:animated];
    _disappear = YES;
}

- (NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section
{
    return 0;
}

- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath
{
    return nil;
}

- (void)tableView:(UITableView *)tableView didSelectRowAtIndexPath:(NSIndexPath *)indexPath
{
    [tableView deselectRowAtIndexPath:indexPath animated:YES];
}

#pragma mark
#pragma methods for creating and removing the header view

//添加下拉刷新
- (void)createHeaderView
{
    if (_refreshHeaderView && [_refreshHeaderView superview])
    {
        [_refreshHeaderView removeFromSuperview];
    }
    
    _refreshHeaderView = [[EGORefreshTableHeaderView alloc] initWithFrame:
                          CGRectMake(0.0f, 0.0f - self.view.bounds.size.height,
                                     self.view.frame.size.width, self.view.bounds.size.height)];
    _refreshHeaderView.delegate = self;
    
    
    [_tableView addSubview:_refreshHeaderView];
    [_refreshHeaderView refreshLastUpdatedDate];
}

- (void)removeHeaderView
{
    if (_refreshHeaderView && [_refreshHeaderView superview])
    {
        [_refreshHeaderView removeFromSuperview];
    }
    
    _refreshHeaderView = nil;
}

//在列表底部显示正在加载更多
- (void)setFooterView
{
    CGFloat height = MAX(_tableView.contentSize.height, _tableView.frame.size.height);
    
    if (_refreshFooterView && [_refreshFooterView superview])
    {
        // reset position
        _refreshFooterView.frame = CGRectMake(0.0f,height,
                                              _tableView.frame.size.width,
                                              self.view.bounds.size.height);
    }
    else
    {
        _refreshFooterView = [[LoadingFooter alloc] initWithFrame:
                              CGRectMake(0.0f, height,
                                         _tableView.frame.size.width, self.view.bounds.size.height)];
        
        [_tableView addSubview:_refreshFooterView];
    }
    
}

//当没有更多的数据的时候、去掉列表底部的加载更多
- (void)removeFooterView
{
    if (_refreshFooterView && [_refreshFooterView superview])
    {
        [_refreshFooterView removeFromSuperview];
    }
    
    _refreshFooterView = nil;
}
#pragma mark-
#pragma mark force to show the refresh headerView
//手动调用下拉刷新
-(void)showRefreshHeader:(BOOL)animated
{
    if (!_reloading)
    {
        _tableView.contentSize = CGSizeZero;
        [UIView animateWithDuration:0.3 animations:^{
            _tableView.contentInset = UIEdgeInsetsMake(65, 0.0f, 0.0f, 0.0f);
            [_tableView scrollRectToVisible:CGRectMake(0, 0.0f, 1, 1) animated:NO];
            
        } completion:^(BOOL finish){
            [_refreshHeaderView egoRefreshScrollViewDidEndDragging:_tableView];
        }];
    }
}

#pragma mark -ScrollViewDelegate

- (void)scrollViewDidScroll:(UIScrollView *)scrollView
{
    if (_refreshHeaderView)
    {
        [_refreshHeaderView egoRefreshScrollViewDidScroll:scrollView];
    }
    
    if ( (scrollView.contentOffset.y+scrollView.frame.size.height) > scrollView.contentSize.height+Load_Height &&
        scrollView.contentOffset.y > 0.0f && !_reloading && _more && scrollView.dragging)
    {
        
        [_refreshFooterView.indicator startAnimating];
        _refreshFooterView.infoLabel.hidden = NO;
        _reloading = YES;
        scrollView.contentInset = UIEdgeInsetsMake(0.0f, 0.0f, 2*Load_Height, 0.0f);
        [self loadNextPage];
    }
}

- (void)scrollViewDidEndDragging:(UIScrollView *)scrollView willDecelerate:(BOOL)decelerate
{
    if (_refreshHeaderView)
    {
        [_refreshHeaderView egoRefreshScrollViewDidEndDragging:scrollView];
    }
}

#pragma mark -
#pragma mark EGORefreshTableDelegate Methods

- (void)egoRefreshTableDidTriggerRefresh:(EGORefreshPos)aRefreshPos
{
    [self beginToReloadData:aRefreshPos];
}

- (BOOL)egoRefreshTableDataSourceIsLoading:(UIView *)view
{
    return _reloading;
}

//显示上次刷新的时间
- (NSDate*)egoRefreshTableDataSourceLastUpdated:(UIView*)view
{
    return  [NSDate date];
}

#pragma mark -
#pragma mark data reloading methods that must be overide by the subclass

- (void)beginToReloadData:(EGORefreshPos)aRefreshPos
{
    _reloading = YES;
    if (aRefreshPos == EGORefreshHeader)
    {
        _loadNext = NO;
        _currentPage = 0;
        [self performSelector:@selector(refreshData) withObject:nil afterDelay:0.1];
    }
    else if (aRefreshPos == EGORefreshFooter)
    {
        [self loadNextPage];
    }
}

- (void)refreshData
{
    [self performSelector:@selector(finishReloadingData) withObject:nil afterDelay:1];
}

- (void)loadNextPage
{
    _loadNext = YES;
    _currentPage++;
}
#pragma mark -
#pragma mark method that should be called when the refreshing is finished
- (void)finishReloadingData
{
    [self hasMore];
    _reloading = NO;
    _loadNext = NO;
}

- (void)hasMore
{
    if (_refreshHeaderView)
    {
        [_refreshHeaderView egoRefreshScrollViewDataSourceDidFinishedLoading:_tableView];
    }
    if (_refreshFooterView)
    {
        [_refreshFooterView.indicator stopAnimating];
        _refreshFooterView.infoLabel.hidden = YES;
    }
    
    if(_more)
    {
        [self setFooterView];
    }
    else
    {
        [self removeFooterView];
    }
}

- (void)viewDidUnload
{
    _refreshFooterView = nil;
    _refreshHeaderView = nil;
    _reloading = NO;
    _loadNext = NO;
    [super viewDidUnload];
}

- (void)dealloc
{
    [_tableView removeObserver:self forKeyPath:@"frame"];
}
@end
