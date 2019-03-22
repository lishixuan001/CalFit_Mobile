import React, {Component} from 'react';
import {
    View,
    ImageBackground,
    Text,
    NetInfo,
    Dimensions,
    StyleSheet,
    Linking,
    WebView
} from 'react-native';
// import BackgroundTask from 'react-native-background-task'
import CustomTabs from "react-native-custom-tabs";
import { Constants, WebBrowser } from 'expo';
const { height, width } = Dimensions.get('window');


class WebService extends Component {

    state = {
        isConnected: false
    };

    componentDidMount() {
        NetInfo.isConnected.addEventListener('connectionChange', this.handleConnectivityChange);
    }

    componentWillUnmount() {
        NetInfo.isConnected.removeEventListener('connectionChange', this.handleConnectivityChange);
    }

    handleConnectivityChange = isConnected => {
        if (isConnected) {
            this.setState({ isConnected });
        } else {
            this.setState({ isConnected });
        }
    };

    render() {
        if (!this.state.isConnected) {
            return (
                <NoInternetDisplay />
            )
        }

        // CustomTabs.openURL('https://www.google.com');
        WebBrowser.openBrowserAsync('https://google.com');

        return null
    }
}

export default WebService;



// BackgroundTask.define( () => {
//     Linking.openURL('https://google.com');
//     BackgroundTask.finish()
// });


function NoInternetDisplay() {
    return (
        <View>
            <ImageBackground source={require('./assets/logo.png')} style={styles.backgroundImage}>
                <View style={styles.offlineContainer}>
                    <Text style={styles.offlineText}>No Internet Connection :(</Text>
                </View>
            </ImageBackground>
        </View>
    );
}

const styles = StyleSheet.create({
    backgroundImage: {
        height: height,
        width: width,
    },
    offlineContainer: {
        backgroundColor: '#b52424',
        height: 30,
        width: width,
        justifyContent: 'center',
        alignItems: 'center',
        flexDirection: 'row',
        position: 'absolute',
        top: 30
    },
    offlineText: {
        color: '#fff'
    }
});