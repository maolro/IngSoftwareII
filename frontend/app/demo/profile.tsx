import React, { useEffect, useState } from 'react';
import { View, Text, Image, TouchableOpacity, StyleSheet, TextInput, Alert } from 'react-native';
import { Card, ListItem, theme, TouchableListItem } from './components';
import { Usuario, ReviewInfo } from './objects';
import Icon from 'react-native-vector-icons/MaterialIcons';

// Datos de usuario (normalmente se obtendría mediante la API)
const CURRENT_USER: Usuario = {
  id: 'user1',
  name: 'Usuario Demo',
  username: '@usuariodemo',
  avatar: 'https://placehold.co/100x100/e2e8f0/64748b?text=UD',
  email: 'usuario.demo@email.com',
  origin: 'Madrid, España',
  memberSince: '10 Oct 2025',
};

// Datos de amigos (normalmente se obtendría mediante la API)
const MOCK_FRIENDS: Usuario[] = [
  {
    id: 'user2',
    name: 'Ana López',
    username: '@analopez',
    avatar: 'https://placehold.co/100x100/6ee7b7/064e3b?text=AL',
    email: 'ana.lopez@email.com',
    origin: 'Valencia, España',
    memberSince: '15 Nov 2025',
  },
  {
    id: 'user3',
    name: 'Bruno Reyes',
    username: '@bruno',
    avatar: 'https://placehold.co/100x100/c4b5fd/4338ca?text=BR',
    email: 'bruno.reyes@email.com',
    origin: 'Lisboa, Portugal',
    memberSince: '28 Oct 2025',
  },
];

// Datos de todos los usuarios (normalmente se obtendría mediante API)
const MOCK_ALL_USERS: Usuario[] = [
  CURRENT_USER,
  ...MOCK_FRIENDS,
  {
    id: 'user4',
    name: 'Carlo Emilion',
    username: '@carlo.e',
    avatar: 'https://placehold.co/100x100/fca5a5/991b1b?text=CE',
    email: 'carlo.emilion@email.com',
    origin: 'Roma, Italia',
    memberSince: '5 Nov 2025',
  },
  {
    id: 'user5',
    name: 'Daniela Silva',
    username: '@daniela.s',
    avatar: 'https://placehold.co/100x100/fcd34d/92400e?text=DS',
    email: 'daniela.silva@email.com',
    origin: 'São Paulo, Brasil',
    memberSince: '20 Oct 2025',
  },
];

// Datos de degustaciones (normalmente se obtendría mediante API)
const MOCK_REVIEWS: { [key: string]: ReviewInfo[] } = {
  user1: [
    { id: 'r1', title: 'IPA Galáctica', subtitle: 'Rating: 4.8 ★ · 14 Nov 2025' },
    { id: 'r2', title: 'Stout Oscura', subtitle: 'Rating: 4.7 ★ · 12 Nov 2025' },
  ],
  user2: [
    { id: 'r3', title: 'Maravillas Pilsner', subtitle: 'Rating: 4.0 ★ · 15 Nov 2025' },
  ],
  user3: [
    { id: 'r4', title: 'Puro Tropico', subtitle: 'Rating: 5.0 ★ · 13 Nov 2025' },
  ],
};

interface ProfileScreenProps {
  userId: string | null;
  friends: string[];
  friendRequests: { from: string, to: string, status: 'pending' | 'accepted' | 'rejected' }[];
  onSendFriendRequest: (userId: string) => void;
  onViewProfile: (userId: string) => void;
  setHeaderProps: (props: { onBack: (() => void) | null }) => void;
}

export default function ProfileScreen({ userId, friends, friendRequests
  , onSendFriendRequest, onViewProfile, setHeaderProps }: ProfileScreenProps) {

  const [activeTab, setActiveTab] = useState('info'); // Pestaña activa
  const [currentUser, setCurrentUser] = useState(CURRENT_USER); // Estado del usuario actual
  const [viewingProfile, setViewingProfile] = useState(currentUser); // Usuario que se está viendo
  const [isEditing, setIsEditing] = useState(false); // Si está editando
  const [editData, setEditData] = useState(currentUser); // Cambios temporales para edición

  // Carga datos de usuario
  useEffect(() => {
    if (userId) {
      const userToView = MOCK_ALL_USERS.find(user => user.id === userId) || CURRENT_USER;
      setViewingProfile(userToView);
      
      // Cambia el header
      if (userId !== CURRENT_USER.id) {
        setHeaderProps({ onBack: () => {} });
      }
    } else {
      setViewingProfile(currentUser);
    }
  }, [userId, currentUser, setHeaderProps]);

  // Constante para comprobar si estás en tu perfil
  const isMyProfile = viewingProfile.id === currentUser.id;

  // Constante para comprobar el estado de amistad
  const friendStatus = () => {
    if (friends.includes(viewingProfile.id)) {
      return 'friends';
    }
    if (friendRequests.some(req => req.to === viewingProfile.id && req.status === 'pending')) {
      return 'pending';
    }
    return 'none';
  };
  const currentFriendStatus = friendStatus();

  // --- Handlers ---
  const handleEdit = () => {
    setEditData(viewingProfile);
    setIsEditing(true);
  };

  const handleCancel = () => {
    setIsEditing(false);
  };

  // Gestiona y actualiza los datos (normalmente usaría API)
  const handleSave = () => {
    setViewingProfile(editData);
    setCurrentUser(editData);
    setIsEditing(false);
  };

  // Selecciona para ver datos de un amigo
  const handleSelectFriend = (friend: Usuario) => {
    onViewProfile(friend.id);
    // setViewingProfile(friend);
    // setActiveTab('info');
    // setIsEditing(false);
  };

  // Función para añadir amigo
  const handleAddFriend = () => {
    // Aquí iría la lógica de la API para enviar la solicitud (RF-2.2)
    onSendFriendRequest(viewingProfile.id);
    Alert.alert(
      'Solicitud de Amistad',
      `Solicitud enviada a ${viewingProfile.name}`
    );
  };

  // --- Funciones de renderización ---

  const renderEditControls = () => {
    if (!isMyProfile) return null; // No hay botones de edit en perfiles de usuario

    if (isEditing) {
      return (
        <View style={styles.buttonContainer}>
          <TouchableOpacity
            style={[styles.button, styles.buttonCancel]}
            onPress={handleCancel}>
            <Text style={styles.buttonText}>Cancelar</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={[styles.button, styles.buttonSave]}
            onPress={handleSave}>
            <Text style={styles.buttonText}>Guardar</Text>
          </TouchableOpacity>
        </View>
      );
    }

    return (
      <View style={styles.buttonContainer}>
        <TouchableOpacity
          style={[styles.button, styles.buttonEdit]}
          onPress={handleEdit}>
          <Text style={styles.buttonText}>Editar Perfil</Text>
        </TouchableOpacity>
      </View>
    );
  };

  const renderFriendshipButton = () => {
    if (isMyProfile) return null; // No mostrar nada en tu propio perfil

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
          <TouchableOpacity
            style={[styles.button, styles.buttonAddFriend]}
            onPress={handleAddFriend}>
            <Icon name="person-add" size={20} color={theme.bgWhite} />
            <Text style={[styles.buttonText, { marginLeft: 10 }]}>Añadir Amigo</Text>
          </TouchableOpacity>
        );
      default:
        return null;
    }
  };

  return (
    <View style={styles.page}>
      {/* --- Cabecera --- */}
      <View style={styles.profileHeader}>
        <Image
          source={{ uri: viewingProfile.avatar }}
          style={styles.profileHeaderPic}
        />
        <Text style={styles.profileHeaderName}>{viewingProfile.name}</Text>
        <Text style={styles.profileHeaderUsername}>
          {viewingProfile.username}
        </Text>

        {/* Botón para añadir amigo */}
        {renderFriendshipButton()}
      </View>

      {/* --- estañas del perfil --- */}
      <View style={styles.profileTabs}>
        <TouchableOpacity onPress={() => setActiveTab('info')}>
          <Text style={[styles.tab, activeTab === 'info' && styles.tabActive]}>
            Info
          </Text>
        </TouchableOpacity>
        <TouchableOpacity onPress={() => setActiveTab('friends')}>
          <Text style={[styles.tab, activeTab === 'friends' && styles.tabActive]}>
            Amigos
          </Text>
        </TouchableOpacity>
        <TouchableOpacity onPress={() => setActiveTab('reviews')}>
          <Text style={[styles.tab, activeTab === 'reviews' && styles.tabActive]}>
            Degustaciones
          </Text>
        </TouchableOpacity>
      </View>

      {/* --- Pestañas --- */}

      {/* ---  Pestaña de información personal --- */}
      {activeTab === 'info' && (
        <Card title="Información Personal">
          {isEditing ? (
            <>
              <View style={styles.editItem}>
                <Text style={styles.editLabel}>Email</Text>
                <TextInput
                  style={styles.editInput}
                  value={editData.email}
                  onChangeText={text =>
                    setEditData({ ...editData, email: text })
                  }
                  keyboardType="email-address"
                />
              </View>
              <View style={styles.editItem}>
                <Text style={styles.editLabel}>Origen</Text>
                <TextInput
                  style={styles.editInput}
                  value={editData.origin}
                  onChangeText={text =>
                    setEditData({ ...editData, origin: text })
                  }
                />
              </View>
              <ListItem
                title="Miembro desde"
                subtitle={viewingProfile.memberSince}
              />
            </>
          ) : (
            <>
              <ListItem title="Email" subtitle={viewingProfile.email} />
              <ListItem title="Origen" subtitle={viewingProfile.origin} />
              <ListItem
                title="Miembro desde"
                subtitle={viewingProfile.memberSince}
              />
            </>
          )}
          {renderEditControls()}
        </Card>
      )}

      {/* --- FRIENDS TAB --- */}
      {/* This tab always shows *your* friends, even when viewing a friend's profile */}
      {activeTab === 'friends' && (
        <Card title={`Lista de Amigos (${MOCK_FRIENDS.length})`}>
          {MOCK_FRIENDS.map(friend => (
            <TouchableListItem
              key={friend.id}
              title={friend.name}
              subtitle={friend.username}
              avatarText={friend.name.substring(0, 2).toUpperCase()}
              onPress={() => handleSelectFriend(friend)}
            />
          ))}
        </Card>
      )}

      {/* --- REVIEWS TAB --- */}
      {activeTab === 'reviews' && (
        <Card title={`Reseñas (${MOCK_REVIEWS[viewingProfile.id]?.length || 0})`}>
          {(MOCK_REVIEWS[viewingProfile.id] || []).map(review => (
            <ListItem
              key={review.id}
              title={review.title}
              subtitle={review.subtitle}
              iconName="sports-bar"
            />
          ))}
          {!MOCK_REVIEWS[viewingProfile.id] && (
            <Text style={styles.emptyStateText}>No hay reseñas todavía.</Text>
          )}
        </Card>
      )}
    </View>
  );
}

// Estilos locales solo para ProfileScreen
const styles = StyleSheet.create({
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