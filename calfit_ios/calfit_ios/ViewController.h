//
//  ViewController.h
//  Calfit_iOS
//
//  Created by Shixuan Li on 4/4/19.
//  Copyright © 2019 Shixuan Li. All rights reserved.
//

#import <UIKit/UIKit.h>
#import <WebKit/WebKit.h>

@interface ViewController : UIViewController <WKNavigationDelegate>

@property (weak, nonatomic) IBOutlet WKWebView *webView;
@property (weak, nonatomic) IBOutlet UIActivityIndicatorView *activityIndicator;
@property (weak, nonatomic) IBOutlet UIImageView *imageView;
@property (weak, nonatomic) IBOutlet UIButton *reloadButton;

- (void)operate;
- (BOOL)IsConnectionAvailable;

@end

