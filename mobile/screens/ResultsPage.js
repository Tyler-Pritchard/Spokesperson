import React from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';

export default function ResultsPage({ navigation }) {
  return (
    <View style={styles.container}>
      <Text>Results Page</Text>
      <Button title="Back to Spokesperson Creation" onPress={() => navigation.navigate('SpokespersonCreation')} />
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
