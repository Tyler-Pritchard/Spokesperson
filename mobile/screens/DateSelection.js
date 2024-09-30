import React from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';

export default function DateSelection({ navigation }) {
  return (
    <View style={styles.container}>
      <Text>Date Selection Page</Text>
      <Button title="Next" onPress={() => navigation.navigate('ResultsPage')} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
});
