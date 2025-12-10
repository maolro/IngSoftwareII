import { Link, useRouter } from "expo-router";
import React, { useState, useEffect } from "react";
import { Text, StyleSheet, TextInput, TouchableOpacity, View, Image, Alert } from "react-native";
import api from "../home_components/api";

export default function RegisterScreen() {
    // Variables
    const router = useRouter();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [email, setEmail] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [birthDate, setBirthDate] = useState('');
    const [errorMsg, setErrorMsg] = useState('');
    const [regError, setRegError] = useState(false);
    const [loading, setLoading] = useState(false);

    // Función de validación de correos
    const isValidEmail = (email: string) => {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(email);
    };

    // Gestión de registro
    const handleRegistration = async () => {
        // Elimina mensaje de error
        setErrorMsg('');

        if (!username.trim()) {
            setErrorMsg('ERROR: El nombre de usuario es obligatorio.');
            setRegError(true);
            return;
        }

        if (!isValidEmail(email)) {
            setErrorMsg('ERROR: Correo electrónico inválido.');
            setRegError(true);
            return;
        }

        if (password.length < 6) {
            setErrorMsg('ERROR: La contraseña debe tener por lo menos 6 caracteres.');
            setRegError(true);
            return;
        }

        if (password !== confirmPassword) {
            setErrorMsg('ERROR: Las contraseñas no coinciden.');
            setRegError(true);
            return;
        }

        const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
        if (!dateRegex.test(birthDate)) {
                setErrorMsg('ERROR: La fecha debe ser YYYY-MM-DD (Ej: 1990-01-31).');
                setRegError(true);
                return;
        }
        
        try {
            setLoading(true); // Empieza a cargar
            
            const user = await api.users.create({
                username: username,
                email: email,
                password: password,
                birth_date: birthDate
            });
            console.log(user);
            // Lógica en caso de éxito
            if (user && user.id) {
                router.replace({ pathname: './home',params: { userId: user.id }})
            }
        } 
        catch (error: any) {
            console.error("Registration error:", error);
            setRegError(true);
            setErrorMsg(error.message || 'ERROR: No se pudo crear el usuario.');
        } 
        finally {
            setLoading(false);
        }
    };

    const ErrorMessage = ({ message }: { message: string }) => {
        if (!message) return null;
        return <Text style={styles.errorText}>{message}</Text>;
    };

    return (
        <View style={styles.container}>
            <Image source={require('../../assets/logo.png')} style={styles.logo} />

            <Text style={styles.title}>Crea una cuenta</Text>
            <Text style={styles.body}>Ingrese su correo electrónico para registrarse en esta aplicación
            </Text>

            <TextInput
                style={styles.input}
                placeholder="Nombre de usuario"
                autoCapitalize="none"
                value={username}
                onChangeText={setUsername}
            />

            <TextInput
                style={styles.input}
                placeholder="correoelectronico@dominio.com"
                autoCapitalize="none"
                value={email}
                onChangeText={setEmail}
            />

            <TextInput
                style={styles.input}
                placeholder="Fecha de nacimiento (YYYY-MM-DD)"
                value={birthDate}
                onChangeText={setBirthDate}
            />

            <TextInput
                style={styles.input}
                placeholder="Contraseña"
                autoCapitalize="none"
                secureTextEntry={true} 
                value={password}
                onChangeText={setPassword}
            />

                <TextInput
                    style={styles.input}
                    placeholder="Confirmar contraseña"
                    autoCapitalize="none"
                    secureTextEntry={true} // Added for security
                    value={confirmPassword}
                    onChangeText={setConfirmPassword}
                />

            <TouchableOpacity style={styles.button} onPress={handleRegistration}>
                <Text style={styles.buttonText}>Continuar</Text>
            </TouchableOpacity>

            {regError && (
                <Text style={styles.errorText}>{errorMsg}</Text>
            )}

            <View style={styles.separatorContainer}>
                    <View style={styles.separatorLine} />
            </View>

            <Text style={styles.forgotPasswordText}>Al hacer clic en continuar acepta nuestros</Text>
                        
            <TouchableOpacity>
                <Text style={styles.forgotPasswordLink}>
                    términos de servicio y política de privacidad
                </Text>
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
    errorText: {
        color: 'rgba(255, 0, 0, 0.7)',
        marginHorizontal: 10,
        fontSize: 16,
        fontWeight: 'bold',
        marginTop: 10
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
