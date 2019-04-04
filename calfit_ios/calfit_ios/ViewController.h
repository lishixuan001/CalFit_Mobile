//
//  ViewController.h
//  Calfit_iOS
//
//  Created by Shixuan Li on 4/3/19.
//  Copyright © 2019 Shixuan Li. All rights reserved.
//

#import <UIKit/UIKit.h>
#import <WebKit/WebKit.h>
#import <sys/socket.h>
#import <netinet/in.h>
#import <SystemConfiguration/SystemConfiguration.h>

@interface ViewController : UIViewController <WKNavigationDelegate>

@property (weak, nonatomic) IBOutlet WKWebView *webView;
@property (weak, nonatomic) IBOutlet UIActivityIndicatorView *activityIndicator;

/*
 Connectivity testing code pulled from Apple's Reachability Example: https://developer.apple.com/library/content/samplecode/Reachability
 */
+ (BOOL)hasConnectivity;

@end

