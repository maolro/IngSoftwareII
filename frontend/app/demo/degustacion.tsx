import React, { useState } from 'react';
import { View, Text, Modal, TextInput, TouchableOpacity, StyleSheet } from 'react-native';
import { theme } from './components';
import { Cerveza } from './objects';

interface ReviewFormProps {
    beer: Cerveza;
    onSubmit: (review: string, rating: number) => void;
    onCancel: () => void;
}

export const ReviewForm: React.FC<ReviewFormProps> = ({
    beer,
    onSubmit,
    onCancel,
}) => {
    const [reviewText, setReviewText] = useState('');
    const [rating, setRating] = useState(0);

    const handleSubmit = () => {
        // In a real app, you'd validate
        onSubmit(reviewText, rating);
    };

    return (
        <Modal
            animationType="slide"
            transparent={true}
            visible={true}
            onRequestClose={onCancel}>
            <View style={styles.modalBackdrop}>
                <View style={styles.modalContent}>
                    <Text style={styles.modalTitle}>Añadir Reseña para {beer.name}</Text>
                    <TextInput
                        style={styles.textInput}
                        placeholder="Escribe tu reseña..."
                        multiline
                        value={reviewText}
                        onChangeText={setReviewText}
                    />
                    {/* A real app would have a star rating component here */}
                    <TextInput
                        style={[styles.textInput, { height: 50, marginTop: 10 }]}
                        placeholder="Rating (0-5)"
                        keyboardType="numeric"
                        value={rating > 0 ? String(rating) : ''}
                        onChangeText={text => setRating(Number(text))}
                    />
                    <View style={styles.buttonRow}>
                        <TouchableOpacity
                            style={[styles.button, styles.buttonCancel]}
                            onPress={onCancel}>
                            <Text style={styles.buttonText}>Cancelar</Text>
                        </TouchableOpacity>
                        <TouchableOpacity style={styles.button} onPress={handleSubmit}>
                            <Text style={styles.buttonText}>Enviar</Text>
                        </TouchableOpacity>
                    </View>
                </View>
            </View>
        </Modal>
    );
};

const styles = StyleSheet.create({
    modalBackdrop: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: 'rgba(0,0,0,0.5)',
    },
    modalContent: {
        backgroundColor: theme.bgWhite,
        borderRadius: 12,
        padding: 20,
        width: '90%',
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.25,
        shadowRadius: 4,
        elevation: 5,
    },
    modalTitle: {
        fontSize: 20,
        fontWeight: '700',
        marginBottom: 16,
    },
    textInput: {
        borderWidth: 1,
        borderColor: theme.border,
        borderRadius: 8,
        padding: 12,
        fontSize: 16,
        height: 100,
        textAlignVertical: 'top',
    },
    button: {
        backgroundColor: theme.blue,
        padding: 16,
        borderRadius: 8,
        alignItems: 'center',
        marginBottom: 20,
    },
    buttonText: {
        color: theme.bgWhite,
        fontSize: 16,
        fontWeight: '700',
    },
    buttonCancel: {
        backgroundColor: theme.textLight,
        marginRight: 10,
    },
    buttonRow: {
        flexDirection: 'row',
        justifyContent: 'flex-end',
        marginTop: 20,
    },
})