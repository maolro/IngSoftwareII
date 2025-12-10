import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ActivityIndicator, TouchableOpacity, Alert } from 'react-native';
import { Card, ListItem, theme } from './components';
import api, { Beer, Tasting, User, Award, FriendRequest } from './api';

  // Variables que recibe de la cabecera
interface DashboardProps {
  userId: number; 
}

// Exportamos la pantalla de dashboard 
export const DashboardScreen: React.FC<DashboardProps> = ({
  userId,
}) => {
  const [recentTastings, setRecentTastings] = useState<Tasting[]>([]);
  const [favoriteBeers, setFavoriteBeers] = useState<Beer[]>([]);
  const [userAwards, setUserAwards] = useState<Award[]>([]);
  const [friendRequests, setFriendRequests] = useState<FriendRequest[]>([]);
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Cargar todos los datos en paralelo
      const [
        userData,
        tastingsData,
        favoritesData,
        awardsData,
        requestsData
      ] = await Promise.all([
      api.users.getById(userId).then(data => 
        { console.log('✅ User data loaded'); return data; }),
      api.degustaciones.getByUser(userId).then(data =>
        { console.log('✅ Tastings data loaded'); return data; }),
      api.beers.getFavorites(userId).then(data => 
        { console.log('✅ Favorites data loaded'); return data; }),
      api.awards.getByUser(userId).then(data => 
        { console.log('✅ Awards data loaded'); return data; }),
      api.users.getPendingRequests(userId).then(data => 
        { console.log('✅ Pending requests loaded'); return data; }),
    ]);

    console.log('All data loaded successfully');

      setCurrentUser(userData);
      setRecentTastings(tastingsData.slice(0, 5)); // Últimas 5 degustaciones
      setFavoriteBeers(favoritesData.slice(0, 3)); // Top 3 favoritas
      setUserAwards(awardsData); 
      setFriendRequests(requestsData);

    } 
    catch (err) {
      console.error('Error loading dashboard data:', err);
      setError('Error al cargar los datos del dashboard');
      Alert.alert("Error", "No se pudieron cargar los datos del dashboard");
    } 
    finally {
      setLoading(false);
    }
  };

  const handleAcceptFriend = async (senderId: number) => {
    try {
      // Usa la API de solicitudes de amistad
      await api.users.acceptFriendRequest(userId, senderId);
      
      // Actualiza estado local
      setFriendRequests(prev => prev.filter(req => req.sender_id !== senderId));
      Alert.alert("Éxito", "Ahora son amigos");
    } 
    catch (err) {
      console.error('Error accepting friend:', err);
      Alert.alert("Error", "No se pudo aceptar la solicitud");
    }
  };

  const handleDeclineFriend = async (senderId: number) => {
    try {
        // Usa el endpoint de rechazar
        await api.users.rejectFriendRequest(userId, senderId);

        // Actualiza estado local
        setFriendRequests(prev => prev.filter(req => req.sender_id !== senderId));
    } catch (err) {
        console.error('Error rejecting friend:', err);
        Alert.alert("Error", "No se pudo rechazar la solicitud");
    }
  };

  if (loading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color={theme.primary} />
        <Text style={styles.loadingText}>Cargando dashboard...</Text>
      </View>
    );
  }

  if (error) {
    return (
      <View style={styles.center}>
        <Text style={styles.errorText}>{error}</Text>
        <TouchableOpacity style={styles.retryButton} onPress={loadDashboardData}>
          <Text style={styles.retryButtonText}>Reintentar</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <View style={styles.page}>
      {/* Stats Grid */}
      <View style={styles.statsGrid}>
        <View style={styles.statsCard}>
          <Text style={styles.statNumber}>{recentTastings.length}</Text>
          <Text style={styles.statLabel}>Degustaciones</Text>
        </View>
        <View style={styles.statsCard}>
          <Text style={styles.statNumber}>{userAwards.length}</Text>
          <Text style={styles.statLabel}>Galardones</Text>
        </View>
      </View>

      {/* Solicitudes de amistad */}
      {friendRequests.length > 0 && (
        <Card title={`Solicitudes de amistad (${friendRequests.length})`}>
          {friendRequests.map(request => (
            <View key={request.id} style={styles.friendRequestItem}>
              <ListItem 
                title={request.sender_username}
                subtitle={request.sender_email}
                avatarText={request.sender_username.substring(0, 2).toUpperCase()}
              />
              <View style={styles.friendActions}>
                <TouchableOpacity 
                  style={[styles.friendButton, styles.acceptButton]}
                  onPress={() => handleAcceptFriend(request.sender_id)}
                >
                  <Text style={styles.friendButtonText}>✓</Text>
                </TouchableOpacity>
                <TouchableOpacity 
                  style={[styles.friendButton, styles.declineButton]}
                  onPress={() => handleDeclineFriend(request.sender_id)}
                >
                  <Text style={styles.friendButtonText}>✕</Text>
                </TouchableOpacity>
              </View>
            </View>
          ))}
        </Card>
      )}

      {/* Cervezas favoritas */}
      <Card title={`Cervezas favoritas (${favoriteBeers.length})`}>
        {favoriteBeers.length > 0 ? (
          favoriteBeers.map(beer => (
            <ListItem 
              key={beer.id}
              title={beer.nombre}
              subtitle={`${beer.estilo} · ${beer.valoracion_promedio ? `${beer.valoracion_promedio} ★` : 'Sin valorar'}`}
              iconName="sports-bar"
            />
          ))
        ) : (
          <Text style={styles.emptyText}>No tienes cervezas favoritas aún</Text>
        )}
      </Card>

      {/* Degustaciones recientes */}
      <Card title="Degustaciones recientes">
        {recentTastings.length > 0 ? (
          recentTastings.map(tasting => (
            <ListItem 
              key={tasting.id}
              title={tasting.nombre_cerveza || 'Cerveza'}
              subtitle={`${tasting.comentario || 'Sin comentario'} ${
                tasting.puntuacion ? `· ${tasting.puntuacion} ★` : ''
              }`}
              iconName="rate-review"
            />
          ))
        ) : (
          <Text style={styles.emptyText}>No hay degustaciones recientes</Text>
        )}
      </Card>

      {/* Galardones recientes */}
      <Card title="Últimos galardones">
        {userAwards.length > 0 ? (
          userAwards.map(award => (
            <ListItem 
              key={award.id}
              title={award.nombre}
              subtitle={`${award.nivel || 'Nivel 1'} · ${award.fecha_obtencion ? new Date(award.fecha_obtencion).toLocaleDateString() : 'Reciente'}`}
              iconName="emoji-events"
            />
          ))
        ) : (
          <Text style={styles.emptyText}>No tienes galardones aún</Text>
        )}
      </Card>
    </View>
  );
}

// Estilos locales solo para HomeScreen
const styles = StyleSheet.create({
  page: {
    padding: 20,
  },
  center: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
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
    alignItems: 'center',
  },
  statNumber: {
    fontSize: 32,
    fontWeight: '700',
    color: theme.primary,
  },
  statLabel: {
    fontSize: 14,
    color: '#a16207',
    textAlign: 'center',
  },
  friendRequestItem: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  friendActions: {
    flexDirection: 'row',
    gap: 8,
  },
  friendButton: {
    width: 32,
    height: 32,
    borderRadius: 16,
    justifyContent: 'center',
    alignItems: 'center',
  },
  acceptButton: {
    backgroundColor: theme.primary,
  },
  declineButton: {
    backgroundColor: theme.red,
  },
  friendButtonText: {
    color: theme.bgWhite,
    fontWeight: 'bold',
    fontSize: 14,
  },
  emptyText: {
    padding: 16,
    color: theme.textLight,
    textAlign: 'center',
    fontStyle: 'italic',
  },
  loadingText: {
    marginTop: 12,
    color: theme.textLight,
    textAlign: 'center',
  },
  errorText: {
    color: theme.red,
    textAlign: 'center',
    marginBottom: 16,
  },
  retryButton: {
    backgroundColor: theme.primary,
    padding: 12,
    borderRadius: 8,
    alignItems: 'center',
  },
  retryButtonText: {
    color: theme.bgWhite,
    fontSize: 16,
    fontWeight: '600',
  },
});