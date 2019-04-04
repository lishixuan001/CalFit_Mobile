//
//  ViewController.m
//  Calfit_iOS
//
//  Created by Shixuan Li on 4/3/19.
//  Copyright © 2019 Shixuan Li. All rights reserved.
//

#import "ViewController.h"

@interface ViewController ()

@end

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view, typically from a nib.
    
    // Set Backgound Image
    // self.view.backgroundColor = [UIColor colorWithPatternImage:[UIImage imageNamed:@"Logo.png"]];
    
    // Boundle Delegate
    self.webView.navigationDelegate = self;
    
    // Check Internet Connectivity
    BOOL connected = [ViewController hasConnectivity];
    if (connected) {
        // Load WebView
        NSString *stringURL = @"https://www.google.com";
        NSURL *URL = [NSURL URLWithString:stringURL];
        NSURLRequest *requestURL = [NSURLRequest requestWithURL:URL];
        [self.webView loadRequest:requestURL];
    }
    else {
        
    }
    
}

// Start Preparing Loading Page
- (void)webView:(WKWebView *)webView didStartProvisionalNavigation:(WKNavigation *)navigation {
    return;
}

// Started Loading Page
- (void)webView:(WKWebView *)webView didCommitNavigation:(WKNavigation *)navigation {
    [self.activityIndicator startAnimating];
    self.activityIndicator.hidesWhenStopped = YES;
}

// Finished Loading Page
- (void)webView:(WKWebView *)webView didFinishNavigation:(WKNavigation *)navigation {
    [self.activityIndicator stopAnimating];
}

// Failed Preparing Loading Page
- (void)webView:(WKWebView *)webView didFailProvisionalNavigation:(WKNavigation *)navigation withError:(NSError *)error {
    return;
}

// Failed Loading Page
- (void)webView:(WKWebView *)webView didFailNavigation:(WKNavigation *)navigation withError:(NSError *)error {
    return;
}

+ (BOOL)hasConnectivity {
    struct sockaddr_in zeroAddress;
    bzero(&zeroAddress, sizeof(zeroAddress));
    zeroAddress.sin_len = sizeof(zeroAddress);
    zeroAddress.sin_family = AF_INET;
    
    SCNetworkReachabilityRef reachability = SCNetworkReachabilityCreateWithAddress(kCFAllocatorDefault, (const struct sockaddr*)&zeroAddress);
    if (reachability != NULL) {
        //NetworkStatus retVal = NotReachable;
        SCNetworkReachabilityFlags flags;
        if (SCNetworkReachabilityGetFlags(reachability, &flags)) {
            if ((flags & kSCNetworkReachabilityFlagsReachable) == 0)
            {
                // If target host is not reachable
                return NO;
            }
            
            if ((flags & kSCNetworkReachabilityFlagsConnectionRequired) == 0)
            {
                // If target host is reachable and no connection is required
                //  then we'll assume (for now) that your on Wi-Fi
                return YES;
            }
            
            
            if ((((flags & kSCNetworkReachabilityFlagsConnectionOnDemand ) != 0) ||
                 (flags & kSCNetworkReachabilityFlagsConnectionOnTraffic) != 0))
            {
                // ... and the connection is on-demand (or on-traffic) if the
                //     calling application is using the CFSocketStream or higher APIs.
                
                if ((flags & kSCNetworkReachabilityFlagsInterventionRequired) == 0)
                {
                    // ... and no [user] intervention is needed
                    return YES;
                }
            }
            
            if ((flags & kSCNetworkReachabilityFlagsIsWWAN) == kSCNetworkReachabilityFlagsIsWWAN)
            {
                // ... but WWAN connections are OK if the calling application
                //     is using the CFNetwork (CFSocketStream?) APIs.
                return YES;
            }
        }
    }
    
    return NO;
}

@end
