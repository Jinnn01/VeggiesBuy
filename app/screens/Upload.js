import React, { useEffect } from 'react';
import { BarCodeScanner } from 'expo-barcode-scanner';
import { StatusBar } from "expo-status-bar";
import { StyleSheet, Text, View, Button } from "react-native";


export default function Upload() {
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
  };

  return (
    <View style={styles.container}>
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
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
    alignItems: "center",
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