import { Link } from "expo-router";
import React, { useState, useEffect } from "react";
import { Text, StyleSheet, TextInput, TouchableOpacity, View, Image } from "react-native";

export default function PasswordResetScreen() {
    return (
        <View style={styles.container}>
            <Image source={require('../../assets/logo.png')} style={styles.logo} />

            <Text style={styles.title}>Nueva contraseña</Text>
            <Text style={styles.body}>Escriba su nueva contraseña</Text>

            <TextInput
                style={styles.input}
                placeholder="Contraseña"
                autoCapitalize="none"
            />
            
            <TextInput
                style={styles.input}
                placeholder="Confirmar contraseña"
                autoCapitalize="none"
            />

            <TouchableOpacity style={styles.button}>
                <Text style={styles.buttonText}>Continuar</Text>
            </TouchableOpacity>
        </View>
    );
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
