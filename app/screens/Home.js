import { StatusBar } from "expo-status-bar";
import { StyleSheet, Text, SafeAreaView } from "react-native";
import { FlashList } from '@shopify/flash-list';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { useTheme } from '@react-navigation/native';
import FoodItems from "../../FoodItems";
import { SearchBar } from '@rneui/themed';

const data = [
  { title: "Apples", price: "$9.99" },
  { title: "Bananas", price: "$9.99" },
  { title: "Mangoes", price: "$9.99" },
  { title: "Pears", price: "$9.99" },
];

export default function Home() {
  const { colors } = useTheme();

  return (
    <SafeAreaView style={styles.container}>
      
      <Text style={{ fontWeight: '700', fontSize: 32, paddingBottom: 18, paddingTop: 38, paddingHorizontal: 10, color: colors.text}}>Welcome</Text>
      <SearchBar
        placeholder="Search..." 
        containerStyle={{ backgroundColor: colors.background, marginHorizontal: 2, height: 42 }}
        round={true}
        platform={"ios"}
      />
      <FlashList contentContainerStyle={styles.list}
        data={data}
        renderItem={({ item }) => <FoodItems item={item} />}
        estimatedItemSize={200}
        horizontal={false}
        numColumns={2}
      />
      <StatusBar style='auto' />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1
  },
  list: {
    paddingTop: 30,
  },
  card: {
    flex: 1,
    height: 40,
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: 8,
  },
  search: {
    marginHorizontal: 30,
  },
  iosProp: {
    shadowColor: 'black',
    shadowOffset: { width: 5, height: 5 },
    shadowOpacity: 0.20,
    shadowRadius: 3,
  }
});