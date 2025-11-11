import { Link, useRouter } from "expo-router";
import React, { useState, useEffect } from "react";
import { Text, StyleSheet, TextInput, TouchableOpacity, View, Image } from "react-native";

export default function PasswordRecoverScreen() {
    // Variables
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [loginError, setLoginError] = useState(false);
    const router = useRouter();

    // Función de gestión de login
    const handleLogin = () => {
        // --- Dummy Validation Logic (Replace with real API call later) ---
        
        // Example of a hardcoded "correct" user/pass (for demonstration)
        const CORRECT_USER = 'admin';
        const CORRECT_PASS = '12345';
        
        if (username === CORRECT_USER && password === CORRECT_PASS) {
            // Success: Clear any previous error and navigate (e.g., to the home screen)
            setLoginError(false);
            router.push('./home');
        } else {
            // Failure: Set error state to true
            setLoginError(true);
        }
    };

    return (
        <View style={styles.container}>
          <Image source={require('../../assets/logo.png')} style={styles.logo} />
          
          <View style={styles.loginSection}>
            <Text style={styles.title}>Iniciar Sesión</Text>
            <Text style={styles.body}>Introduczca su nombre de usuario y contraseña para iniciar sesión</Text>
    
            <TextInput
              style={styles.input}
              placeholder="Nombre de usuario"
              autoCapitalize="none"
              value={username}
              onChangeText={setUsername}
            />
    
            <TextInput
              style={styles.input}
              placeholder="Contraseña"
              autoCapitalize="none"
              value={password}
              onChangeText={setPassword}
            />
    
            <TouchableOpacity style={styles.button} onPress={handleLogin}>
              <Text style={styles.buttonText}>Continuar</Text>
            </TouchableOpacity>
            
            {loginError && (
                <Text style={styles.errorText}>ERROR: Usuario o contraseña incorrecta</Text>
            )}
        </View>

        <View style={styles.separatorContainer}>
            <View style={styles.separatorLine} />
            <Text style={styles.separatorText}>o</Text>
            <View style={styles.separatorLine} />
        </View>
    
        <View style={styles.forgotPasswordContainer}>
            <Text style={styles.forgotPasswordText}>¿Olvidó su contraseña?</Text>
            
            <Link href="./pwd_recover" asChild>
              <TouchableOpacity>
                <Text style={styles.forgotPasswordLink}>
                  Haga click en este enlace para cambiar su contraseña
                </Text>
              </TouchableOpacity>
            </Link>
        </View>
    </View>);
}

// Estilos
const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'flex-start',
        alignItems: 'center',
        padding: 20,
        backgroundColor: '#dcda6dff',
    },
    logo: {
        width: 200,
        height: 100,
        marginBottom: 20,
        resizeMode: 'contain',
    },
    loginSection: {
        alignItems: 'center',
        width: '100%',
    },
    title: {
        fontSize: 20,
        fontWeight: 'bold',
        marginBottom: 10,
        color: '#000000ff',
    },
    body: {
        fontSize: 16,
        color: 'black',
        textAlign: 'center',
        marginBottom: 20,
        paddingHorizontal: 5,
    },
    input: {
        width: '100%',
        height: 45,
        borderWidth: 1,
        borderColor: '#ddd',
        borderRadius: 8,
        paddingHorizontal: 15,
        marginBottom: 10,
        backgroundColor: 'white',
        fontSize: 16,
    },
    button: {
        width: '100%',
        height: 45,
        backgroundColor: '#000000ff',
        borderRadius: 8,
        justifyContent: 'center',
        alignItems: 'center',
        marginTop: 10,
    },
    buttonText: {
        color: 'white',
        fontSize: 18,
        fontWeight: 'bold',
    },
    errorText: {
        color: 'rgba(255, 0, 0, 0.7)',
        marginHorizontal: 10,
        fontSize: 16,
        fontWeight: 'bold',
        marginTop: 10
    },
    separatorContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        marginVertical: 30,
        width: '100%',
    },
    separatorLine: {
        flex: 1,
        height: 1,
        backgroundColor: 'rgba(0, 0, 0, 0.3)',
    },
    separatorText: {
        color: 'rgba(0, 0, 0, 0.7)',
        marginHorizontal: 10,
        fontSize: 16,
    },
    forgotPasswordContainer: {
        alignItems: 'center',
    },
    forgotPasswordText: {
        fontSize: 14,
        color: 'rgba(0, 0, 0, 0.7)',
        marginBottom: 5,
    },
    forgotPasswordLink: {
        fontSize: 14,
        color: 'rgba(0, 0, 0, 0.7)',
        textAlign: 'center',
        textDecorationLine: 'underline',
    },
});
