import React from 'react';
import { StyleSheet, Text, View } from 'react-native';
import { Constants } from 'expo';
import { NetInfo } from 'react-native';
import WebService from './WebService'

export default class App extends React.Component {

  render() {
    return (
      <View style={styles.container}>
          <WebService />
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
});
