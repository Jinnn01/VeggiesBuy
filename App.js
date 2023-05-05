import React, {useState, useEffect} from 'react';
import {SafeAreaView, Text, StyleSheet, View, Button, useColorScheme} from 'react-native';
import Navigation from 'src/navigation';
import { Amplify } from 'aws-amplify';
import config from 'src/aws-exports';
import { DarkTheme, DefaultTheme, NavigationContainer } from '@react-navigation/native';
import { FlashList } from '@shopify/flash-list';
import { createStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import Ionicons from 'react-native-vector-icons/Ionicons';
import Home from './app/screens/Home';
import Map from './app/screens/Map';
import Upload from './app/screens/Upload';
import MapView, {Callout, Marker} from 'react-native-maps';
import { GooglePlacesAutocomplete } from 'react-native-google-places-autocomplete';
import { StatusBar } from 'expo-status-bar';
import 'react-native-gesture-handler';



Amplify.configure(config);

const App = () => {
  //Auth.signOut(); //To Sign-up and try it again
  return (
    <SafeAreaView style={styles.root}>
      <Navigation />
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  root: {
    flex: 1,
    backgroundColor: '#F9FBFC',
  },
});



export default App;