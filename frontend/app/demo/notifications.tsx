import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Card, ListItem, theme} from './components';

export default function NotificationsScreen() {
  return (
    <View style={styles.page}>
      <Text style={styles.pageTitle}>Notificaciones</Text>
      <Card title="Actividad de Amigos">
        <ListItem title="Ana López" subtitle="ha valorado una nueva cerveza." avatarText="AL" />
        <ListItem title="Bruno Reyes" subtitle='ha conseguido el galardón "Nivel 5".' avatarText="BR" />
        <ListItem title="Ana López" subtitle="ha añadido un comentario." avatarText="AL" />
      </Card>
    </View>
  );
}

const styles = StyleSheet.create({
  page: {
    padding: 20,
  },
  pageTitle: {
    fontSize: 28,
    fontWeight: '700',
    marginBottom: 20,
    color: theme.textDark,
  },
});