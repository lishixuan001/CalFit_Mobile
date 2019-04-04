//
//  ViewController.m
//  Calfit_iOS
//
//  Created by Shixuan Li on 4/4/19.
//  Copyright © 2019 Shixuan Li. All rights reserved.
//

#import "ViewController.h"
#import "Reachability.h"

@interface ViewController ()

@end

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view, typically from a nib.
    
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
        NSString *stringURL = @"https://www.youtube.com";
        NSURL *URL = [NSURL URLWithString:stringURL];
        NSURLRequest *requestURL = [NSURLRequest requestWithURL:URL];
        [self.webView loadRequest:requestURL];
    }
    else {
        // Background Image Notice
        UIImage *image = [UIImage imageNamed: @"logo.png"];
        self.imageView.contentMode = UIViewContentModeScaleAspectFit;
        [self.imageView setImage:image];
        self.imageView.hidden = NO;
        
        // Button ShowUp
        [self.reloadButton setTitle:@"ReLoad" forState:UIControlStateNormal];
        self.reloadButton.hidden = NO;
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
