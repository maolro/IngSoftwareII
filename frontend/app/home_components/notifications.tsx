import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ActivityIndicator, ScrollView, RefreshControl } from 'react-native';
import { Card, ListItem, theme } from './components';
import api, { Tasting } from './api'; // Ensure this points to your api file

interface NotificationsScreenProps {
  userId: number;
}

export default function NotificationsScreen({ userId }: NotificationsScreenProps) {
  const [activities, setActivities] = useState<Tasting[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadActivity = async () => {
    try {
      setError(null);
      const data = await api.users.getActivity(userId);
      setActivities(data);
    } 
    catch (err) {
      console.error("Error loading activity:", err);
      setError("No se pudo cargar la actividad reciente.");
    } 
    finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    loadActivity();
  }, [userId]);

  const onRefresh = () => {
    setRefreshing(true);
    loadActivity();
  };

  // Helper to format the notification text
  const getSubtitle = (tasting: Tasting) => {
    const beerName = tasting.nombre_cerveza || "una cerveza";
    const score = tasting.puntuacion ? ` con ${tasting.puntuacion} ★` : "";
    if (tasting.comentario) {
      return `Comentó sobre ${beerName}: "${tasting.comentario}"${score}`;
    }
    return `Ha valorado ${beerName}${score}.`;
  };

  if (loading && !refreshing) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color={theme.primary} />
      </View>
    );
  }

  return (
    <ScrollView 
      style={styles.page}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
      }
    >
      <Text style={styles.pageTitle}>Notificaciones</Text>
      
      {error && (
        <Text style={styles.errorText}>{error}</Text>
      )}

      <Card title="Actividad de Amigos">
        {activities.length === 0 && !error ? (
          <Text style={styles.emptyText}>No hay actividad reciente de tus amigos.</Text>
        ) : (
          activities.map((item) => (
            <ListItem 
              key={item.id}
              title={item.nombre_usuario || "Usuario"} 
              subtitle={getSubtitle(item)}
              // Genera iniciales
              avatarText={(item.nombre_usuario || "?").substring(0, 2).toUpperCase()}
            />
          ))
        )}
      </Card>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  page: {
    padding: 20,
  },
  center: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 50,
  },
  pageTitle: {
    fontSize: 28,
    fontWeight: '700',
    marginBottom: 20,
    color: theme.textDark,
  },
  errorText: {
    color: 'red',
    marginBottom: 10,
    textAlign: 'center',
  },
  emptyText: {
    color: theme.textLight,
    fontStyle: 'italic',
    padding: 10,
    textAlign: 'center',
  }
});