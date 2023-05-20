import React from 'react';
import {View, Text} from 'react-native';
import {Auth} from 'aws-amplify'
import Background from '../ScreenBackground/Background';

const index = () => {
  const signOut = () => {
    Auth.signOut();
  };

  return (
    <Background>
    <View style={{flex: 1}}>
      <Text style={{color: 'white', fontSize: 24, alignSelf: 'center'}}>Home, sweet home</Text>
      <Text
        onPress={signOut}
        style={{
          textAlign: 'center',
          color: 'red',
          marginTop: 'auto',
          marginVertical: 20,
          fontSize: 20,
          paddingHorizontal: 25,
          paddingVertical:25
        }}>
        Sign out
      </Text>
    </View>
    </Background>
  );
};

export default index;