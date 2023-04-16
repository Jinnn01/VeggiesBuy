import { Text, View } from "react-native";
import { useState } from "react";
import { useTheme } from '@react-navigation/native';

export default function FoodItems(props) {
  const { colors } = useTheme();

  return <Text style={{ color: colors.text, paddingHorizontal: 10, paddingVertical: 8 }}>
    {props.item.title}{"\n"}
    {props.item.price}</Text>
}