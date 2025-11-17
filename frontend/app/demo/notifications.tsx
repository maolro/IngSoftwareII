import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Card, ListItem, theme} from './components';

export default function NotificationsScreen() {
  return (
    <View style={styles.page}>
      <Text style={styles.pageTitle}>Notificaciones</Text>
      <Card title="Actividad de Amigos">
        <ListItem title="maria_catadora" subtitle="ha valorado una nueva cerveza." avatarText="MA" />
        <ListItem title="carlos_brewmaster" subtitle='ha conseguido el galardón "Nivel 5".' avatarText="CA" />
        <ListItem title="maria_catadora" subtitle="ha añadido un comentario." avatarText="MA" />
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