import React, { useEffect, useState } from 'react';
import { BarCodeScanner } from 'expo-barcode-scanner';
import { StatusBar } from "expo-status-bar";
import { StyleSheet, Text, SafeAreaView, Button, TextInput } from "react-native";


export default function Upload() {
  const [text, setText] = useState('');
  //const [text2, setText] = useState('');
  //const [text3, setText] = useState('');
  /*
  const [hasPermission, setHasPermission] = React.useState(false);
  const [scanData, setScanData] = React.useState();

  useEffect(() => {
    (async() => {
      const {status} = await BarCodeScanner.requestPermissionsAsync();
      setHasPermission(status === "granted");
    })();
  }, []);

  if (!hasPermission) {
    return (
      <View style={styles.container}>
        <Text>Please grant camera permission to scan the barcode</Text>
      </View>
    )
  }

  const handleBarCodeScanned = ({type, data}) => {
    setScanData(data);
    console.log(`Data: ${data}`);
    console.log(`Type: ${type}`);
  };*/

  return (
    <SafeAreaView style={styles.container}>
      {/*}
      <BarCodeScanner 
        style={styles.barCodeScanner}
        onBarCodeScanned={scanData ? undefined : handleBarCodeScanned}
      />
      {scanData && 
        <Button 
          title='Scan again' 
          onPress={() => setScanData(undefined)} 
        />
      }
      <Text style={{ fontWeight: '700', fontSize: 24, paddingTop: 18}}>Scan Receipt</Text>
      <Text style={{ fontWeight: '400', fontSize: 14, paddingTop: 8}}>Simply place your supermarket receipt within the frame.</Text>
    <StatusBar style='auto' />*/}


      <Text>Supermarket location: </Text>
      
      <TextInput
        style={{height: 40, borderColor: 'blue', marginTop: 140, fontSize: 22}}
        placeholder="Supermarket location"
        onChangeText={text => setText(text)}
        //defaultValue={text}
      />
      {/*}
      <TextInput
        style={{height: 40, marginTop: 40}}
        placeholder="Vegetable name"
        onChangeText={text2 => setText(text2)}
        defaultValue={text2}
      />
      <TextInput
        style={{height: 40, marginTop: 40}}
        placeholder="Vegetable price"
        onChangeText={text3 => setText(text3)}
        defaultValue={text3}
      />*/}
      
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
    alignItems: "left",
    padding: 10
    //justifyContent: "center",
  },
  /*
  barCodeScanner: {
    width: '90%',
    height: '60%',
    borderRadius: '24',
    marginTop: '18%',
  },*/
});