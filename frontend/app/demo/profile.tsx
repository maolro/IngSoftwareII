import React, { useEffect, useState } from 'react';
import {
  View, Text, Image, TouchableOpacity, StyleSheet,
  TextInput, Alert, ActivityIndicator
} from 'react-native';
import { Card, ListItem, theme, TouchableListItem } from './components';
import Icon from 'react-native-vector-icons/MaterialIcons';
import api, { User, Tasting } from './api';

interface ProfileScreenProps {
  userId: number | null; 
  currentUserId: number; 
  friends: number[]; 
  friendRequests: { from: number, to: number, status: 'pending' | 'accepted' | 'rejected' }[];
  onSendFriendRequest: (userId: number) => void;
  onViewProfile: (userId: number) => void;
  setHeaderProps: (props: { onBack: (() => void) | null }) => void; 
}

export default function ProfileScreen({
  userId,
  currentUserId,
  friends,
  friendRequests,
  onSendFriendRequest,
  onViewProfile,
  setHeaderProps
}: ProfileScreenProps) {

  const [activeTab, setActiveTab] = useState('info');
  const [isEditing, setIsEditing] = useState(false);

  // --- ESTADOS DE DATOS (API) ---
  const [viewingProfile, setViewingProfile] = useState<User | null>(null);
  const [editData, setEditData] = useState<Partial<User>>({}); // Cambios temporales para edición

  // Datos de las pestañas (se cargan bajo demanda)
  const [profileFriends, setProfileFriends] = useState<User[]>([]);
  const [profileTastings, setProfileTastings] = useState<Tasting[]>([]);

  // Estados de carga
  const [isLoading, setIsLoading] = useState(true);
  const [isTabLoading, setIsTabLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Flags para saber si ya cargamos los datos de las pestañas
  const [hasFetchedFriends, setHasFetchedFriends] = useState(false);
  const [hasFetchedTastings, setHasFetchedTastings] = useState(false);

  // Constante para comprobar si estás en tu perfil
  const isMyProfile = userId === null || userId === currentUserId;

  // --- Carga de Datos del Perfil  ---
  useEffect(() => {
    // Determina qué ID cargar
    const idToLoad = isMyProfile ? currentUserId : userId;

    if (!idToLoad) {
      setError("No se pudo determinar el usuario a cargar.");
      return;
    }

    const fetchUsuario = async () => {
      setIsLoading(true);
      setError(null);
      // Reseteamos los datos de las pestañas al cambiar de perfil
      setHasFetchedFriends(false);
      setHasFetchedTastings(false);
      setProfileFriends([]);
      setProfileTastings([]);

      try {
        const userData = await api.users.getById(idToLoad);
        setViewingProfile(userData);
        setEditData(userData); 
      } catch (err) {
        console.error("Error al cargar el usuario:", err);
        setError("No se pudo cargar el perfil.");
      } finally {
        setIsLoading(false);
      }
    };

    fetchUsuario();
  }, [userId, currentUserId]); // Se ejecuta si cambia el ID del perfil o el usuario logueado

  // --- Carga de Datos de Pestañas (Bajo demanda) ---
  useEffect(() => {
    if (!viewingProfile) return;

    const loadTabData = async () => {
      setIsTabLoading(true);
      try {
        if (activeTab === 'friends' && !hasFetchedFriends) {
          const friendsData = await api.users.getFriends(viewingProfile.user_id);
          setProfileFriends(friendsData);
          setHasFetchedFriends(true);
        } else if (activeTab === 'reviews' && !hasFetchedTastings) {
          const tastingsData = await api.degustaciones.getByUser(viewingProfile.user_id);
          setProfileTastings(tastingsData);
          setHasFetchedTastings(true);
        }
      } catch (err) {
        console.error(`Error al cargar la pestaña ${activeTab}:`, err);
        Alert.alert("Error", `No se pudieron cargar los datos de la pestaña.`);
      } finally {
        setIsTabLoading(false);
      }
    };

    loadTabData();
  }, [activeTab, viewingProfile, hasFetchedFriends, hasFetchedTastings]);


  // --- Lógica de Amistad ---
  const friendStatus = () => {
    if (!viewingProfile) return 'none'; 

    if (friends.includes(viewingProfile.user_id)) {
      return 'friends';
    }
    if (friendRequests.some(req => req.to === viewingProfile.user_id && req.status === 'pending')) {
      return 'pending';
    }
    return 'none';
  };
  const currentFriendStatus = friendStatus();

  // --- Handlers ---
  const handleEdit = () => {
    if (!viewingProfile) return;
    setEditData(viewingProfile); 
    setIsEditing(true);
  };

  const handleCancel = () => {
    setIsEditing(false);
    setEditData(viewingProfile ?? {}); // Revierte los cambios
  };

  // Gestiona y actualiza los datos llamando a la API
  const handleSave = async () => {
    if (!viewingProfile) return;

    // Solo envía los campos que se pueden editar
    const dataToUpdate: Partial<User> = {
      username: editData.username,
      email: editData.email,
      birth_date: editData.birth_date,
      avatar: editData.avatar, 
    };

    try {
      const updatedUser = await api.users.update(viewingProfile.user_id, dataToUpdate);

      // Actualiza el estado local con la respuesta del servidor
      setViewingProfile(updatedUser);
      setEditData(updatedUser); // Actualiza la base de edición
      setIsEditing(false);
      Alert.alert("Éxito", "Perfil actualizado correctamente.");
    } catch (err) {
      console.error("Error al guardar:", err);
      Alert.alert("Error", "No se pudo actualizar el perfil.");
    }
  };

  // --- MODIFICADO ---
  // Selecciona para ver datos de un amigo (ahora usa User)
  const handleSelectFriend = (friend: User) => {
    onViewProfile(friend.user_id);
  };

  // Función para añadir amigo 
  const handleAddFriend = () => {
    if (!viewingProfile) return;
    onSendFriendRequest(viewingProfile.user_id);
    Alert.alert(
      'Solicitud de Amistad',
      `Solicitud enviada a ${viewingProfile.username}` // Usamos username
    );
  };

  // --- Funciones de renderización ---
  const renderEditControls = () => {
    if (!isMyProfile) return null;
    if (isEditing) {
      return (
        <View style={styles.buttonContainer}>
          <TouchableOpacity style={[styles.button, styles.buttonCancel]} onPress={handleCancel}>
            <Text style={styles.buttonText}>Cancelar</Text>
          </TouchableOpacity>
          <TouchableOpacity style={[styles.button, styles.buttonSave]} onPress={handleSave}>
            <Text style={styles.buttonText}>Guardar</Text>
          </TouchableOpacity>
        </View>
      );
    }
    return (
      <View style={styles.buttonContainer}>
        <TouchableOpacity style={[styles.button, styles.buttonEdit]} onPress={handleEdit}>
          <Text style={styles.buttonText}>Editar Perfil</Text>
        </TouchableOpacity>
      </View>
    );
  };

  const renderFriendshipButton = () => {
    if (isMyProfile) return null;
    switch (currentFriendStatus) {
      case 'friends':
        return (
          <View style={[styles.button, styles.buttonFriends]}>
            <Icon name="check" size={20} color={theme.bgWhite} />
            <Text style={[styles.buttonText, { marginLeft: 10 }]}>Amigos</Text>
          </View>
        );
      case 'pending':
        return (
          <View style={[styles.button, styles.buttonPending]}>
            <Icon name="hourglass-top" size={20} color={theme.bgWhite} />
            <Text style={[styles.buttonText, { marginLeft: 10 }]}>Solicitud Enviada</Text>
          </View>
        );
      case 'none':
        return (
          <TouchableOpacity style={[styles.button, styles.buttonAddFriend]} onPress={handleAddFriend}>
            <Icon name="person-add" size={20} color={theme.bgWhite} />
            <Text style={[styles.buttonText, { marginLeft: 10 }]}>Añadir Amigo</Text>
          </TouchableOpacity>
        );
      default: return null;
    }
  };

  // --- Renderizado principal ---

  // Estado de carga principal
  if (isLoading) {
    return <ActivityIndicator size="large" style={styles.loader} />;
  }

  // Estado de error principal
  if (error || !viewingProfile) {
    return <Text style={styles.emptyStateText}>{error || "No se encontró el perfil."}</Text>;
  }

  // Formatear fechas
  const formatDate = (dateString?: string) => {
    if (!dateString) return "No especificado";
    return new Date(dateString).toLocaleDateString();
  }
  return (
    <View style={styles.page}>
      {/* --- Cabecera --- */}
      <View style={styles.profileHeader}>
        <Image
          source={{ uri: viewingProfile.avatar 
            || 'https://placehold.co/100x100/e2e8f0/64748b?text=AL' }}
          style={styles.profileHeaderPic}
        />
        <Text style={styles.profileHeaderName}>{viewingProfile.username}</Text>
        <Text style={styles.profileHeaderUsername}>
          {viewingProfile.email}
        </Text>
        {renderFriendshipButton()}
      </View>

      {/* --- Pestañas del perfil --- */}
      <View style={styles.profileTabs}>
        <TouchableOpacity onPress={() => setActiveTab('info')}>
          <Text style={[styles.tab, activeTab === 'info' && styles.tabActive]}>Info</Text>
        </TouchableOpacity>
        <TouchableOpacity onPress={() => setActiveTab('friends')}>
          <Text style={[styles.tab, activeTab === 'friends' && styles.tabActive]}>Amigos</Text>
        </TouchableOpacity>
        <TouchableOpacity onPress={() => setActiveTab('reviews')}>
          <Text style={[styles.tab, activeTab === 'reviews' && styles.tabActive]}>Degustaciones</Text>
        </TouchableOpacity>
      </View>

      {/* --- Indicador de carga para pestañas --- */}
      {isTabLoading && <ActivityIndicator size="small" style={{ margin: 20 }} />}

      {/* --- Pestaña de información personal --- */}
      {activeTab === 'info' && (
        <Card title="Información Personal">
          {isEditing ? (
            <>
              <View style={styles.editItem}>
                <Text style={styles.editLabel}>Username</Text>
                <TextInput
                  style={styles.editInput}
                  value={editData.username}
                  onChangeText={text => setEditData({ ...editData, username: text })}
                />
              </View>
              <View style={styles.editItem}>
                <Text style={styles.editLabel}>Email</Text>
                <TextInput
                  style={styles.editInput}
                  value={editData.email}
                  onChangeText={text => setEditData({ ...editData, email: text })}
                  keyboardType="email-address"
                />
              </View>
              <View style={styles.editItem}>
                <Text style={styles.editLabel}>Fecha de Nacimiento (YYYY-MM-DD)</Text>
                <TextInput
                  style={styles.editInput}
                  value={editData.birth_date}
                  onChangeText={text => setEditData({ ...editData, birth_date: text })}
                  placeholder="YYYY-MM-DD"
                />
              </View>
              <ListItem
                title="Miembro desde"
                subtitle={formatDate(viewingProfile.created_at)}
              />
            </>
          ) : (
            <>
              <ListItem title="Email" subtitle={viewingProfile.email} />
              <ListItem title="Fecha de Nacimiento" subtitle={formatDate(viewingProfile.birth_date)} />
              <ListItem
                title="Miembro desde"
                subtitle={formatDate(viewingProfile.created_at)}
              />
            </>
          )}
          {renderEditControls()}
        </Card>
      )}

      {/* --- Pestaña de Amigos --- */}
      {activeTab === 'friends' && !isTabLoading && (
        <Card title={`Lista de Amigos (${profileFriends.length})`}>
          {profileFriends.length === 0 && (
            <Text style={styles.emptyStateText}>Este usuario no tiene amigos.</Text>
          )}
          {profileFriends.map(friend => (
            <TouchableListItem
              key={friend.user_id}
              title={friend.username}
              subtitle={friend.email}
              avatarText={friend.username.substring(0, 2).toUpperCase()}
              onPress={() => handleSelectFriend(friend)}
            />
          ))}
        </Card>
      )}

      {/* --- Pestaña de Degustaciones --- */}
      {activeTab === 'reviews' && !isTabLoading && (
        <Card title={`Degustaciones (${profileTastings.length})`}>
          {profileTastings.length === 0 && (
            <Text style={styles.emptyStateText}>No hay degustaciones todavía.</Text>
          )}
          {profileTastings.map(tasting => (
            <ListItem
              key={tasting.id}
              title={tasting.nombre_cerveza || "Sin nombre"}
              subtitle={`Puntuación: ${tasting.puntuacion || 'N/A'}`}
              iconName="sports-bar"
            />
          ))}
        </Card>
      )}
    </View>
  );
}

// --- Estilos ---
const styles = StyleSheet.create({
  loader: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  page: {
    padding: 20,
  },
  profileHeader: {
    alignItems: 'center',
    marginBottom: 24,
    padding: 16,
    backgroundColor: theme.bgWhite,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: theme.border,
  },
  profileHeaderPic: {
    width: 100,
    height: 100,
    borderRadius: 50,
    marginBottom: 12,
    borderWidth: 3,
    borderColor: theme.bgWhite,
  },
  profileHeaderName: {
    fontSize: 24,
    fontWeight: '700',
    color: theme.textDark,
  },
  profileHeaderUsername: {
    fontSize: 16,
    color: theme.textLight,
  },
  profileTabs: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    borderBottomWidth: 1,
    borderBottomColor: theme.border,
    backgroundColor: theme.bgWhite,
    borderTopLeftRadius: 12,
    borderTopRightRadius: 12,
    paddingTop: 8,
  },
  tab: {
    padding: 12,
    fontWeight: '500',
    color: theme.textLight,
    borderBottomWidth: 3,
    borderBottomColor: 'transparent',
  },
  tabActive: {
    color: theme.primary,
    borderBottomColor: theme.primary,
  },
  buttonContainer: {
    flexDirection: 'row',
    justifyContent: 'flex-end',
    marginTop: 16,
    borderTopWidth: 1,
    borderTopColor: theme.border,
    paddingTop: 16,
  },
  button: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 10,
    paddingHorizontal: 20,
    borderRadius: 8,
    marginLeft: 10,
    flexWrap: 'nowrap',
  },
  buttonEdit: {
    backgroundColor: theme.blue,
  },
  buttonSave: {
    backgroundColor: theme.primary,
  },
  buttonCancel: {
    backgroundColor: theme.textLight,
  },
  buttonText: {
    color: theme.bgWhite,
    fontWeight: '500',
  },
  editItem: {
    paddingVertical: 12,
  },
  editLabel: {
    fontSize: 14,
    color: theme.textLight,
    marginBottom: 4,
    fontWeight: '500',
  },
  editInput: {
    borderWidth: 1,
    borderColor: theme.border,
    borderRadius: 8,
    padding: 12,
    fontSize: 16,
    color: theme.textDark,
  },
  emptyStateText: {
    padding: 16,
    color: theme.textLight,
    textAlign: 'center',
  },
  buttonAddFriend: {
    marginTop: 10,
    marginBottom: 16,
    marginLeft: 0,
    backgroundColor: theme.blue,
  },
  buttonFriends: {
    marginTop: 10,
    marginBottom: 16,
    marginLeft: 0,
    backgroundColor: theme.textLight,
  },
  buttonPending: {
    marginTop: 10,
    backgroundColor: theme.primary,
    marginBottom: 16,
    marginLeft: 0,
  },
});