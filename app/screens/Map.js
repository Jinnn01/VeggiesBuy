import React, {useState, useEffect} from 'react';
import MapView, {Callout, Marker} from 'react-native-maps';
import { StyleSheet, View, Text, Button } from 'react-native';
import { GooglePlacesAutocomplete } from 'react-native-google-places-autocomplete';
import { StatusBar } from 'expo-status-bar';

let locationsALDI = [
  {
    //title: "Aldi Wollongong",
    location: {
      latitude: -34.4280,
      longitude: 150.8991
    },
    priceALDI: "$6.99"
    //description: "25 Stewart St, Wollongong"
  },
  {
    location: {
      latitude: -34.3938,
      longitude: 150.8932
    },
    priceALDI: "$6.99"
  },
]

let locationsColes = [
  {
    //title: "Coles Wollongong",
    location: {
      latitude: -34.4243,
      longitude: 150.8926
    },
    priceColes: "$5.49"
    //description: "200 Crown St, Wollongong"
  },
  {
    location: {
      latitude: -34.3947,
      longitude: 150.8932
    },
    priceColes: "$5.49"
  },
]

let locationsWoolies = [
  {
    //title: "Woolworths Wollongong",
    location: {
      latitude: -34.42703,
      longitude: 150.89611
    },
    priceWoolies: "$2.99"
    //description: "63 Burelli St, Wollongong"
  },
  {
    location: {
      latitude: -34.3917,
      longitude: 150.8937
    },
    priceWoolies: "$2.99"
  },
]


/*
let supermarketLocations = [
  {
    //title: "Woolworths Wollongong",
    location: {
      latitude: -34.42703,
      longitude: 150.89611
    },
    price: "$2.99"
    //description: "63 Burelli St, Wollongong"
  },
  {
    //title: "Coles Wollongong",
    location: {
      latitude: -34.4243,
      longitude: 150.8926
    },
    price: "$5.49"
    //description: "200 Crown St, Wollongong"
  },
  {
    //title: "Aldi Wollongong",
    location: {
      latitude: -34.4280,
      longitude: 150.8991
    },
    price: "$6.99"
    //description: "25 Stewart St, Wollongong"
  },
]*/

export default function Map() {
  const [ region, setRegion ] =  React.useState({
    latitude: -34.4243,
    longitude: 150.8926,
    latitudeDelta: 0.0922,
    longitudeDelta: 0.0421
  })

  const showLocationsALDI = () => {
    return locationsALDI.map((item, index) => {
      return (
        <Marker
          key={index}
          coordinate={item.location}
        >
        <View style={styles.markerALDI}>
              {/*<Text style={styles.markerText}>$3.99</Text>*/}
              <Text style={styles.markerText}>{item.priceALDI}</Text>
            </View>
        </Marker>
      )
    });
  };

  const showLocationsColes = () => {
    return locationsColes.map((item, index) => {
      return (
        <Marker
          key={index}
          coordinate={item.location}
        >
        <View style={styles.markerColes}>
              {/*<Text style={styles.markerText}>$3.99</Text>*/}
              <Text style={styles.markerText}>{item.priceColes}</Text>
            </View>
        </Marker>
      )
    });
  };

  const showLocationsWoolies = () => {
    return locationsWoolies.map((item, index) => {
      return (
        <Marker
          key={index}
          coordinate={item.location}
        >
        <View style={styles.markerWoolies}>
              {/*<Text style={styles.markerText}>$3.99</Text>*/}
              <Text style={styles.markerText}>{item.priceWoolies}</Text>
            </View>
        </Marker>
      )
    });
  };


  const showSupermarketLocations = () => {
    return supermarketLocations.map((item, index) => {
      return (
        <Marker 
          key={index}
          pinColor='blue'
          coordinate={item.location}
          //title={item.title}
          //description={item.description}
          //price={item.price} 
        >
          {/*}
          <View style={styles.customMarker}>
              <Text style={styles.markerText}>$3.99</Text>
          </View>*/}
        </Marker>
      )
    });
  };

  return (
    <View style={{flex: 1}}>
      <MapView 
        style={styles.map}
        showsUserLocation={true} 
        zoomEnabled={true}
        initialRegion={{
          latitude: -34.4243,
          longitude: 150.8926,
          latitudeDelta: 0.0922,
          longitudeDelta: 0.0421
        }}
        provider="google"
        >
          {showLocationsALDI()}
          {showLocationsColes()}
          {showLocationsWoolies()}

        {/*}
          <Marker 
            coordinate={{
              latitude: region.latitude,
              longitude: region.longitude
            }}
          />*/}
      </MapView>
      <StatusBar style='auto' />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  map: {
    width: '100%',
    height: '100%',
  },
  customMarker: {
    width: 60,
    height: 60,
    borderRadius: 35,
    backgroundColor: 'green',
    justifyContent: 'center',
    alignItems: 'center',
  },
  markerALDI: {
    width: 60,
    height: 60,
    borderRadius: 35,
    backgroundColor: 'blue',
    justifyContent: 'center',
    alignItems: 'center',
  },
  markerColes: {
    width: 60,
    height: 60,
    borderRadius: 35,
    backgroundColor: 'red',
    justifyContent: 'center',
    alignItems: 'center',
  },
  markerWoolies: {
    width: 60,
    height: 60,
    borderRadius: 35,
    backgroundColor: 'green',
    justifyContent: 'center',
    alignItems: 'center',
  },
  markerText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
  },
});
