import React, {useState, useEffect} from 'react';
import MapView, {Callout, Marker} from 'react-native-maps';
import { StyleSheet, View, Text, Button, useColorScheme } from 'react-native';
import { GooglePlacesAutocomplete } from 'react-native-google-places-autocomplete';
import { StatusBar } from 'expo-status-bar';
import 'react-native-gesture-handler';
import { DarkTheme, DefaultTheme, NavigationContainer } from '@react-navigation/native';
import { FlashList } from '@shopify/flash-list';
import { createStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { BarCodeScanner } from 'expo-barcode-scanner';
import Ionicons from 'react-native-vector-icons/Ionicons';
import Home from './app/screens/Home';
import Map from './app/screens/Map';
import Upload from './app/screens/Upload';

const Tab = createBottomTabNavigator();

const MyTheme = {
  dark: false,
  colors: {
    primary: 'rgb(255, 45, 85)',
    background: 'rgb(242, 242, 242)',
    card: 'rgb(255, 255, 255)',
    text: 'rgb(28, 28, 30)',
    border: 'rgb(199, 199, 204)',
    notification: 'rgb(255, 69, 58)',
  },
};

export default function App() {

  const scheme = useColorScheme();
  console.log(scheme);

  return (
    <NavigationContainer theme={scheme === 'dark' ? DarkTheme : MyTheme}>
      <Tab.Navigator
        screenOptions={({ route }) => ({
          tabBarIcon: ({ focused, color, size }) => {
            let iconName;

            if (route.name === 'Home') {
              iconName = focused ? 'home': 'home';
            } else if (route.name === 'Map') {
              iconName = focused ? 'map' : 'map';
            }
            else if (route.name === 'Upload') {
              iconName = focused ? 'camera' : 'camera';
            }

            // You can return any component that you like here!
            return <Ionicons name={iconName} size={size} color={color} />;
          },
          tabBarActiveTintColor: '#19aa5c', 
          tabBarInactiveTintColor: 'gray',
        })}
      >
        <Tab.Screen name="Home" component={Home} options={{ headerShown: false }} />
        <Tab.Screen name="Map" component={Map} options={{ headerShown: false }} />
        <Tab.Screen name="Upload" component={Upload} options={{ headerShown: false }} />
      </Tab.Navigator>
    </NavigationContainer>
  );
}
