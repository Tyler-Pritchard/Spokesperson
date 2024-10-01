import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, Button, StyleSheet, FlatList } from 'react-native';
import io from 'socket.io-client';

export default function SpokespersonCreation({ navigation }) {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [socket, setSocket] = useState(null);

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

      // Fetch conversation history from the backend
      fetch('http://10.0.0.50:5000/generate_response', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_input: "Your sample input here" }),
      })
        .then((response) => response.json())
        .then((data) => console.log("Response from /generate_response: ", data))
        .catch((error) => console.error("Error calling /generate_response: ", error));      
    });

    // Listen for incoming messages from the server
    socket.on("message", (message) => {
      console.log("Message received from server: ", message);
      setMessages((prevMessages) => [
        ...prevMessages,
        { id: prevMessages.length.toString(), message }  // Keep the 'message' key to match the backend
      ]);
    });

    socket.on("response", (data) => {
      console.log("AI Response received from server: ", data.message);
      setMessages((prevMessages) => [
        ...prevMessages,
        { id: prevMessages.length.toString(), message: data.message }  // Append AI message
      ]);
    });    

    return () => {
      socket.disconnect();
    };
  }, []);

  const handleSend = () => {
    if (inputText.trim()) {
      // Send the input text as a message to the server
      socket.emit("message", inputText);
      setMessages([...messages, { id: messages.length.toString(), message: inputText }]);  // Correct the key here
      setInputText('');
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Spokesperson Creation</Text>
      <FlatList
        data={messages}
        renderItem={({ item }) => (
          <Text style={styles.message}>{item.message}</Text>  // Use 'item.message' instead of passing the whole object
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
