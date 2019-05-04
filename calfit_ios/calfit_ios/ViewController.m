//
//  ViewController.m
//  Calfit_iOS
//
//  Created by Shixuan Li on 4/4/19.
//  Copyright © 2019 Shixuan Li. All rights reserved.
//

#import "ViewController.h"
#import "Reachability.h"

@interface ViewController () {
    BOOL isGrantedNotificationAccess;
}
@end

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view, typically from a nib.
    isGrantedNotificationAccess = false;
    UNUserNotificationCenter * center = [UNUserNotificationCenter currentNotificationCenter];
    UNAuthorizationOptions options = UNAuthorizationOptionAlert + UNAuthorizationOptionSound;
    [center requestAuthorizationWithOptions:options completionHandler:^(BOOL granted, NSError * _Nullable error) {
        self->isGrantedNotificationAccess = granted;
    }];
    // Bond Navigation Delegate
    self.webView.navigationDelegate = self;
    
    // Main Method
    [self operate];
    
}

- (void)operate {
    // Button/Image Init
    self.reloadButton.hidden = YES;
    self.imageView.hidden = YES;
    
    // Check Internet
    BOOL isConnected = [self IsConnectionAvailable];
    if (isConnected) {
        // Load WebView
        NSString *stringURL = @"http://128.32.192.76/calfit/index/";
        NSURL *URL = [NSURL URLWithString:stringURL];
        NSURLRequest *requestURL = [NSURLRequest requestWithURL:URL];
        [self.webView loadRequest:requestURL];
    }
    else {
        // Background Image Notice
        UIImage *image = [UIImage imageNamed: @"logo"];
        self.imageView.contentMode = UIViewContentModeScaleAspectFit;
        self.view.layer.contents = (__bridge id _Nullable)(image.CGImage);
        [self.imageView setImage:image];
        self.imageView.hidden = NO;
        
        // Button ShowUp
        [self.reloadButton setTitle:@"ReLoad" forState:UIControlStateNormal];
        self.reloadButton.hidden = NO;
    }
}

- (void)notification {
    if (isGrantedNotificationAccess) {
        UNUserNotificationCenter * center = [UNUserNotificationCenter currentNotificationCenter];
        UNMutableNotificationContent * mucontent = [[UNMutableNotificationContent alloc] init];
        mucontent.title = @"CalFit";
        mucontent.subtitle = @"Reminder";
        mucontent.body = @"Good Morning! Your goal today is ready!";
        mucontent.sound = [UNNotificationSound defaultSound];
        
        UNTimeIntervalNotificationTrigger * trigger = [UNTimeIntervalNotificationTrigger triggerWithTimeInterval:3 repeats:NO];
        UNNotificationRequest * request = [UNNotificationRequest requestWithIdentifier:@"CalFitLocalNotification" content:mucontent trigger:trigger];
        [center addNotificationRequest:request withCompletionHandler:nil];
    }
}

// Start Preparing Loading Page
//- (void)webView:(WKWebView *)webView didStartProvisionalNavigation:(WKNavigation *)navigation {
//
//}

// Start Loading Page
- (void)webView:(WKWebView *)webView didCommitNavigation:(WKNavigation *)navigation {
    [self.activityIndicator startAnimating];
}

// Finish Loading Page
- (void)webView:(WKWebView *)webView didFinishNavigation:(WKNavigation *)navigation {
    [self.activityIndicator stopAnimating];
    self.activityIndicator.hidesWhenStopped = YES;
}

// Fail Preparing Loading Page
//- (void)webView:(WKWebView *)webView didFailProvisionalNavigation:(WKNavigation *)navigation withError:(NSError *)error {
//
//}

// Fail Loading Page
//- (void)webView:(WKWebView *)webView didFailNavigation:(WKNavigation *)navigation withError:(NSError *)error {
//
//}

// Show If Internet Connection Is Available
- (BOOL)IsConnectionAvailable {
    Reachability *reachability = [Reachability reachabilityForInternetConnection];
    NetworkStatus networkStatus = [reachability currentReachabilityStatus];
    return !(networkStatus == NotReachable);
}

// Respond to Reload Button Click
- (IBAction)handleButtonClick:(UIButton *)sender {
    [self operate];
}


@end
