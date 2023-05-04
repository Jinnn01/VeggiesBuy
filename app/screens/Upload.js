import React, { useEffect, useState } from 'react';
import { BarCodeScanner } from 'expo-barcode-scanner';
import { StatusBar } from "expo-status-bar";
import { StyleSheet, Text, View, Button, TextInput } from "react-native";
import { useTheme } from '@react-navigation/native';


export default function Upload() {
  const { colors } = useTheme();
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
    <View style={styles.container}>

      <Text style={{ fontWeight: '700', fontSize: 32, paddingBottom: 18, paddingTop: 38, paddingHorizontal: 10, color: colors.text}}>Upload</Text>
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


      <Text style={styles.captionTop}>Supermarket location: </Text>
      <TextInput
        style={styles.input}
        placeholder="Supermarket location"
        onChangeText={text => setText(text)}
        //defaultValue={text}
      />

      <Text style={styles.caption}>Vegetable name: </Text>
      <TextInput
        style={styles.input}
        placeholder="Vegetable name"
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
      
    </View>
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
  captionTop: {
    fontSize: 16,
    marginTop: 140,
    marginBottom: 12,
  },
  caption: {
    fontSize: 16,
    marginTop: 16,
    marginBottom: 12,
  },
  input: {
    borderWidth: 1,
    alignSelf: "stretch",
    padding: 8,
    fontSize: 14,
    height: 44,
    borderRadius: 4,
  }
});