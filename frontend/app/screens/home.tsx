// HomeScreen.js
import { Link, useRouter } from "expo-router";
import React, { useState, useEffect } from "react";
import { Text, StyleSheet, TouchableOpacity, View, Image, ActivityIndicator, ScrollView } from "react-native";

export default function HomeScreen() {
    const [userId, setUserId] = useState(0);
    const [username, setUsername] = useState('');
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState('');
    const router = useRouter();

    return (
        <ScrollView style={styles.container}>
            <Image source={require('../../assets/logo.png')} style={styles.logo} />
            
            {userId ? (
                <View style={styles.userInfo}>
                    <Text style={styles.welcome}>¡Bienvenido, {username}!</Text>
                    
                    <View style={styles.infoSection}>
                        <Text style={styles.sectionTitle}>Información del Usuario</Text>
                        <Text style={styles.infoText}>Email: {email}</Text>
                        {birth_date && (
                            <Text style={styles.infoText}>Fecha de nacimiento: {birth_date}</Text>
                        )}
                        <Text style={styles.infoText}>
                            Amigos: {friends ? friends.length : 0}
                        </Text>
                    </View>

                    {/* Add more sections for your app features */}
                    <View style={styles.actions}>
                        <TouchableOpacity style={styles.actionButton}>
                            <Text style={styles.actionButtonText}>Ver Perfil</Text>
                        </TouchableOpacity>
                        
                        <TouchableOpacity style={styles.actionButton}>
                            <Text style={styles.actionButtonText}>Buscar Amigos</Text>
                        </TouchableOpacity>
                    </View>
                </View>
            ) : (
                <View style={styles.errorSection}>
                    <Text style={styles.errorText}>{error}</Text>
                    <TouchableOpacity style={styles.button} onPress={() => router.replace('./login')}>
                        <Text style={styles.buttonText}>Volver al Login</Text>
                    </TouchableOpacity>
                </View>
            )}

            <TouchableOpacity style={styles.logoutButton} onPress={handleLogout}>
                <Text style={styles.logoutButtonText}>Cerrar Sesión</Text>
            </TouchableOpacity>
        </ScrollView>
    );
}

// Updated styles for Home Screen
const styles = StyleSheet.create({
    container: {
        flex: 1,
        padding: 20,
        backgroundColor: '#dcda6dff',
    },
    logo: {
        width: 200,
        height: 100,
        marginBottom: 20,
        resizeMode: 'contain',
        alignSelf: 'center',
    },
    welcome: {
        fontSize: 24,
        fontWeight: 'bold',
        textAlign: 'center',
        marginBottom: 20,
        color: '#000000',
    },
    userInfo: {
        width: '100%',
    },
    infoSection: {
        backgroundColor: 'white',
        padding: 15,
        borderRadius: 10,
        marginBottom: 20,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.1,
        shadowRadius: 4,
        elevation: 3,
    },
    sectionTitle: {
        fontSize: 18,
        fontWeight: 'bold',
        marginBottom: 10,
        color: '#000000',
    },
    infoText: {
        fontSize: 16,
        marginBottom: 5,
        color: '#333',
    },
    actions: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        marginBottom: 20,
    },
    actionButton: {
        flex: 1,
        backgroundColor: '#000000',
        padding: 15,
        borderRadius: 8,
        marginHorizontal: 5,
        alignItems: 'center',
    },
    actionButtonText: {
        color: 'white',
        fontWeight: 'bold',
    },
    logoutButton: {
        backgroundColor: '#ff4444',
        padding: 15,
        borderRadius: 8,
        alignItems: 'center',
        marginTop: 20,
    },
    logoutButtonText: {
        color: 'white',
        fontWeight: 'bold',
        fontSize: 16,
    },
    errorSection: {
        alignItems: 'center',
        marginVertical: 20,
    },
    errorText: {
        color: 'red',
        textAlign: 'center',
        marginBottom: 20,
        fontSize: 16,
    },
    button: {
        backgroundColor: '#000000',
        padding: 15,
        borderRadius: 8,
        width: '100%',
        alignItems: 'center',
    },
    buttonText: {
        color: 'white',
        fontWeight: 'bold',
    },
});