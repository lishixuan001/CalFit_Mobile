/**import React from 'react';
import { StyleSheet, Text, View } from 'react-native';

export default class App extends React.Component {
  render() {
    return (
      <View style={styles.container}>
        <Text>This is calfit!!!</Text>
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});*/

import React, { Component } from 'react';
import { View, StyleSheet, Button, Text, Linking } from 'react-native';
import { Constants } from 'expo';
import { NetInfo } from 'react-native';
import OfflineNotice from './OfflineNotice'

export default class App extends Component {

    render() {

    return (
      <View style={styles.container}>
        <OfflineNotice />
        <Text style={styles.welcome}>Welcome to CalFit!</Text>
        <Button title="ENTER" onPress={ ()=>{ Linking.openURL('https://google.com')}} />
      </View>
    );
  }}




const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    paddingTop: Constants.statusBarHeight,
    backgroundColor: '#ecf0f1',
  },
  welcome: {
    fontWeight: 'bold',
    fontSize: 30,
  }
});
