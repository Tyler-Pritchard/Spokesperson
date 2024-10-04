import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, Button, StyleSheet, FlatList } from 'react-native';
import io from 'socket.io-client';

export default function SpokespersonCreation({ navigation }) {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [socket, setSocket] = useState(null);

  // Establish WebSocket connection and handle messages
  useEffect(() => {
    const socket = io("http://10.0.0.50:5000", {
      transports: ["websocket"],
      reconnectionAttempts: 5,
      timeout: 20000,
      reconnectionDelayMax: 10000,
    });
    setSocket(socket);

    socket.on('connect', () => {
      console.log("Connected to WebSocket server");
      // Emit a test message to initialize the connection
      socket.emit('message', 'Hello, server!');
    });

    socket.on('response', (data) => {
      console.log("AI Response received from server: ", data);
      if (data && typeof data === 'object' && data.message) {
        setMessages((prevMessages) => [
          ...prevMessages,
          { id: prevMessages.length.toString(), message: data.message }
        ]);
      }
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  const handleSend = () => {
    if (inputText.trim()) {
      // Add the user's message to the local state
      setMessages((prevMessages) => [
        ...prevMessages,
        { id: prevMessages.length.toString(), message: `User: ${inputText}` },
      ]);
  
      // Send the message through the WebSocket
      socket.emit("message", inputText);
      setInputText('');  // Clear the input field
    }
  };
  

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Spokesperson Creation</Text>
      <FlatList
        data={messages}
        renderItem={({ item }) => (
          <Text style={styles.message} key={item.id}>
            {item.message}
          </Text>
        )}
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
    marginTop: 20,
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
