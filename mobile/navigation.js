import React from 'react';
import { Image, TouchableOpacity } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import SpokespersonCreation from './screens/SpokespersonCreation';
import DateSelection from './screens/DateSelection';
import ResultsPage from './screens/ResultsPage';

const Stack = createStackNavigator();

export default function Navigation() {
  return (
    <NavigationContainer>
      <Stack.Navigator
        screenOptions={({ navigation }) => ({
          headerLeft: () => (
            <TouchableOpacity onPress={() => navigation.goBack()}>
              <Image source={require('./assets/back-icon.png')} style={{ width: 25, height: 25 }} />
            </TouchableOpacity>
          ),
        })}
      >
        <Stack.Screen name="SpokespersonCreation" component={SpokespersonCreation} />
        <Stack.Screen name="DateSelection" component={DateSelection} />
        <Stack.Screen name="ResultsPage" component={ResultsPage} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
