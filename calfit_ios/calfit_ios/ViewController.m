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

BOOL isGrantedNotificationAccess;

@implementation ViewController
@synthesize ActiLabel, ActiInput, ActiVerify;

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view, typically from a nib.
    
    isGrantedNotificationAccess = false;
    UNUserNotificationCenter * center = [UNUserNotificationCenter currentNotificationCenter];
    UNAuthorizationOptions options = UNAuthorizationOptionAlert + UNAuthorizationOptionSound;
    
    [center requestAuthorizationWithOptions:options completionHandler:^(BOOL granted, NSError * _Nullable error) {
        isGrantedNotificationAccess = granted;
    }];
    
    // NSUserDefaults *userDefaults = [NSUserDefaults standardUserDefaults];
    // [userDefaults removeObjectForKey:@"ActiGraphID"];
    
    // Bond Navigation Delegate
    self.webView.navigationDelegate = self;
    
    // Main Method
    [self operate];
    
}


- (void)operate {
    // Button/Image Init
    self.reloadButton.hidden = YES;
    self.imageView.hidden = YES;
    self.ActiLabel.hidden = YES;
    self.ActiInput.hidden = YES;
    self.ActiVerify.hidden = YES;
    self.ActiButton.hidden = YES;
    
    // Check if ActiGraphID exist
    NSUserDefaults *userDefaults = [NSUserDefaults standardUserDefaults];
    NSString *ActiGraphID = [userDefaults objectForKey:@"ActiGraphID"];
    BOOL hasID = ActiGraphID != nil;
    
    // Check Internet
    BOOL isConnected = [self IsConnectionAvailable];
    if (isConnected && hasID) {
        // Load WebView
        NSString *stringURL = [NSString stringWithFormat:@"http://128.32.192.76/calfit/index/%@", ActiGraphID];
        NSURL *URL = [NSURL URLWithString:stringURL];
        NSURLRequest *requestURL = [NSURLRequest requestWithURL:URL];
        [self.webView loadRequest:requestURL];
        // [self needUpdate];
        [self notification];
    }
    else {
        // Background Image Notice
        UIImage *image = [UIImage imageNamed: @"logo"];
        self.imageView.contentMode = UIViewContentModeScaleAspectFit;
        self.view.layer.contents = (__bridge id _Nullable)(image.CGImage);
        [self.imageView setImage:image];
        self.imageView.hidden = NO;
        
        if (hasID) {
            // Reload Button ShowUp
            [self.reloadButton setTitle:@"Reload" forState:UIControlStateNormal];
            self.reloadButton.hidden = NO;
        }
        else {
            // Show TextBox for Actigraph ID
            self.ActiLabel.hidden = NO;
            self.ActiInput.hidden = NO;
            self.ActiVerify.hidden = NO;
            self.ActiButton.hidden = NO;
        }
    }
}

- (BOOL) needUpdate {
    
    NSUserDefaults * userDefaults = [NSUserDefaults standardUserDefaults];
    NSString * ActiGraphID = [userDefaults objectForKey:@"ActiGraphID"];
    
    NSString * queryString = [NSString stringWithFormat:@"http://128.32.192.76/calfit/api/check_user/%@", ActiGraphID];
    
    NSURL * url = [NSURL URLWithString: queryString];
    
    NSURLSession *session = [NSURLSession sharedSession];
    
    NSURLSessionDataTask * task = [session dataTaskWithURL:url completionHandler: ^(NSData * data, NSURLResponse * response, NSError * error) {
        NSMutableArray *json = [NSJSONSerialization JSONObjectWithData:data options:kNilOptions error:&error];
        
        // print as json
        NSData * jsonData = [NSJSONSerialization dataWithJSONObject:json options:NSJSONWritingPrettyPrinted error:&error];
        NSString * jsonString = [[NSString alloc] initWithData:jsonData encoding:NSUTF8StringEncoding];
        
        NSLog(@"%@", jsonString);
    }];
    [task resume];
    return YES;
    
}


- (void) notification {
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
    else {
        NSLog(@"isGrantedNotificationAccess=False");
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


// Get Text Input when Button clicked
- (IBAction)ActiButton:(id)sender {
    NSString * ActiGraphID = self.ActiInput.text;
    NSString * ActiGraphVerify = self.ActiVerify.text;
    
    if (ActiGraphID == ActiGraphVerify) {
        NSUserDefaults *userDefaults = [NSUserDefaults standardUserDefaults];
        [userDefaults setObject:ActiGraphID forKey:@"ActiGraphID"];
        [userDefaults synchronize];
        // NSLog(@"%@", NSSearchPathForDirectoriesInDomains(NSLibraryDirectory, NSUserDomainMask, YES).firstObject);
        [self operate];
    }
    else {
        self.ActiInput.text = nil;
        self.ActiVerify.text = nil;
    }
}

@end
