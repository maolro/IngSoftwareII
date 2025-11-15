import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Card, ListItem, theme} from './components';

// Exportamos la pantalla de dashboard (o home)
export default function Dashboard() {
  return (
    <View style={styles.page}>
      {/* Stats Grid */}
      <View style={styles.statsGrid}>
        <View style={styles.statsCard}>
          <Text style={styles.statNumber}>12</Text>
          <Text style={styles.statLabel}>Nº Degustaciones</Text>
        </View>
        <View style={styles.statsCard}>
          <Text style={styles.statNumber}>3</Text>
          <Text style={styles.statLabel}>Nº Locales</Text>
        </View>
      </View>

      {/* Solicitudes de amistad */}
      <Card title="Solicitudes de amistad (3)">
        <ListItem title="Glynn Lee" subtitle="correoelectronico@dominio.net" avatarText="GL" />
        <ListItem title="Oscar Dum" subtitle="oscar.dum@dominio.net" avatarText="OD" />
        <ListItem title="Carlo Emilion" subtitle="carlo.e@dominio.net" avatarText="CE" />
      </Card>

      {/* Cervezas favoritas */}
      <Card title="Cervezas favoritas (Top 3)">
        <ListItem title="IPA Galáctica" subtitle="Rating: 4.8 ★" iconName="sports-bar" />
        <ListItem title="Stout Oscura" subtitle="Rating: 4.7 ★" iconName="sports-bar" />
        <ListItem title="Trigo Ligera" subtitle="Rating: 4.5 ★" iconName="sports-bar" />
      </Card>

      {/* Galardones recientes */}
      <Card title="Últimos galardones">
        <ListItem title="Primeros Pasos" subtitle="Nivel 1 · 14 Nov 2025" iconName="emoji-events" />
        <ListItem title="Amante de IPA" subtitle="Nivel 2 · 12 Nov 2025" iconName="emoji-events" />
      </Card>
    </View>
  );
}

// Estilos locales solo para HomeScreen
const styles = StyleSheet.create({
  page: {
    padding: 20,
  },
  statsGrid: {
    flexDirection: 'row',
    gap: 16,
    marginBottom: 16,
  },
  statsCard: {
    flex: 1,
    backgroundColor: theme.primaryLight,
    borderWidth: 1,
    borderColor: '#fef08a',
    padding: 16,
    borderRadius: 12,
  },
  statNumber: {
    fontSize: 32,
    fontWeight: '700',
    color: theme.primary,
  },
  statLabel: {
    fontSize: 14,
    color: '#a16207',
  },
});