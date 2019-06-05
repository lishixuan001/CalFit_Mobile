//
//  ViewController.h
//  Calfit_iOS
//
//  Created by Shixuan Li on 4/4/19.
//  Copyright © 2019 Shixuan Li. All rights reserved.
//

#import <UIKit/UIKit.h>
#import <WebKit/WebKit.h>
#import <UserNotifications/UserNotifications.h>
// #import <Crittercism/Crittercism.h>

@interface ViewController : UIViewController <WKNavigationDelegate>


@property (weak, nonatomic) IBOutlet WKWebView *webView;
@property (weak, nonatomic) IBOutlet UIActivityIndicatorView *activityIndicator;
@property (weak, nonatomic) IBOutlet UIImageView *imageView;
@property (weak, nonatomic) IBOutlet UIButton *reloadButton;

@property (weak, nonatomic) IBOutlet UILabel *ActiLabel;
@property (weak, nonatomic) IBOutlet UITextField *ActiInput;
@property (weak, nonatomic) IBOutlet UIButton *ActiButton;
@property (weak, nonatomic) IBOutlet UITextField *ActiVerify;


- (void)operate;
- (BOOL)IsConnectionAvailable;
- (void)notification;
- (BOOL)needUpdate;


@end

