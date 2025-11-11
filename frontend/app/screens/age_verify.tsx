import { Link, useRouter } from "expo-router";
import React, { useState, useEffect } from "react";
import { Text, StyleSheet, TextInput, TouchableOpacity, View, Image, Platform, Alert } from "react-native";
import DateTimePicker, { type DateTimePickerEvent } from "@react-native-community/datetimepicker";

export default function AgeVerify() {
    const [date, setDate] = useState<Date | undefined>(undefined);
    const [show, setShow] = useState(Platform.OS === 'web');
    const router = useRouter();

    const showDatePicker = () => {
        setShow(true);
    }

    const onChange = (event: DateTimePickerEvent, selectedDate?: Date) => {
        if (Platform.OS !== 'web') {
            setShow(false);
        }
        if (event.type === 'set' && selectedDate) {
            setDate(selectedDate);
        }
    }
    const handleCheckAge = () => {
        if (!date) {
            Alert.alert('Error', 'Por favor, ingrese su fecha de nacimiento.');
            return;
        }

        const today = new Date();
        let age = today.getFullYear() - date.getFullYear();
        const monthDiff = today.getMonth() - date.getMonth();
        if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < date.getDate())) {
            age--;
        }

        if (age >= 18) {
            Alert.alert('Verificación Exitosa', '¡Bienvenido!');
            router.push('./home'); 
        } 
        else {
            Alert.alert('Acceso Denegado', 'Debes ser mayor de 18 años.');
        }
    }

    return (
        <View style={styles.container}>
            <Image source={require('../../assets/logo.png')} style={styles.logo} />

            <Text style={styles.title}>¿Es usted mayor de edad?</Text>
            <Text style={styles.body}>Ingrese su fecha de nacimiento para verificar su edad</Text>

            <DateTimePicker
                testID="dateTimePicker"
                value={date || new Date()}
                mode="date"
                style={styles.webDatePickerTest}
                display="default"
                onChange={onChange}
                maximumDate={new Date()}
            />

            <TouchableOpacity style={styles.button}>
                <Text style={styles.buttonText}>Comprobar edad</Text>
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
    webDatePicker: {
        width: '100%',
        height: 45,
        marginBottom: 10,
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
    webDatePickerTest: {
        width: '80%',
        height: 50,
        backgroundColor: 'red', // Bright red background
        marginTop: 20,
    },
});
