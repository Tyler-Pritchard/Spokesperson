import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet, FlatList } from 'react-native';

export default function SpokespersonCreation({ navigation }) {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');

  const handleSend = () => {
    if (inputText.trim()) {
      setMessages([...messages, { id: messages.length.toString(), text: inputText }]);
      setInputText('');
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Spokesperson Creation</Text>
      <FlatList
        data={messages}
        renderItem={({ item }) => <Text style={styles.message}>{item.text}</Text>}
        keyExtractor={(item) => item.id}
        style={styles.messageList}
      />
      <View style={styles.inputContainer}>
        <TextInput
          style={styles.input}
          value={inputText}
          onChangeText={setInputText}
          placeholder="Type a message..."
        />
        <Button title="Send" onPress={handleSend} />
      </View>
      <Button title="Next" onPress={() => navigation.navigate('DateSelection')} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 10,
    justifyContent: 'flex-end',
  },
  title: {
    fontSize: 20,
    marginBottom: 10,
  },
  messageList: {
    flex: 1,
  },
  message: {
    backgroundColor: '#f0f0f0',
    padding: 10,
    borderRadius: 10,
    marginVertical: 5,
  },
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 10,
    borderTopWidth: 1,
    borderColor: '#ddd',
  },
  input: {
    flex: 1,
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 5,
    padding: 10,
    marginRight: 10,
  },
});
