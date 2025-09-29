import React, { useState, useEffect } from "react";
import { StyleSheet, Text, View } from "react-native";

// Main
export default function App() {
  const [message, setMessage] = useState("Loading...");

  // Obtiene el mensaje del back-end
  useEffect(() => {
    fetch("http://localhost:5000/api/hello")
      .then((res) => res.json())
      .then((data) => setMessage(data.message))
      .catch(() => setMessage("Error connecting to backend"));
  }, []);

  // Crea la app
  return (
    <View style={styles.container}>
      <Text style={styles.text}>{message}</Text>
    </View>
  );
}

// Estilos de la app
const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: "center", alignItems: "center" },
  text: { fontSize: 20 },
});
