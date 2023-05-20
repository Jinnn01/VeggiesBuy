import React from 'react';
import {SafeAreaView, StyleSheet, Text} from 'react-native';
import Navigation from 'C:/Users/kotla/Authentication/src/navigation';
import { Amplify } from 'aws-amplify';
import config from 'C:/Users/kotla/Authentication/src/aws-exports';

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