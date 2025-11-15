import React, { useState } from 'react';
import {
  StyleSheet,
  Text,
  View,
  Image,
  TouchableOpacity,
  TextInput,
  Modal,
  FlatList,
} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';
import { theme } from './components';

// Define UserData interface here since it's not imported from './objects'
interface UserData {
  id: string;
  name: string;
  username: string;
  avatar?: string;
}

const MOCK_ALL_USERS: UserData[] = [
  { id: 'user1', name: 'Usuario Demo', username: '@usuariodemo', avatar: 'https://placehold.co/100x100/e2e8f0/64748b?text=UD' },
  { id: 'user2', name: 'Ana López', username: '@analopez', avatar: 'https://placehold.co/100x100/6ee7b7/064e3b?text=AL' },
  { id: 'user3', name: 'Bruno Reyes', username: '@bruno', avatar: 'https://placehold.co/100x100/c4b5fd/4338ca?text=BR' },
  { id: 'user4', name: 'Carlo Emilion', username: '@carlo.e', avatar: 'https://placehold.co/100x100/fca5a5/991b1b?text=CE' },
  { id: 'user5', name: 'Daniela Silva', username: '@daniela.s', avatar: 'https://placehold.co/100x100/fcd34d/92400e?text=DS' },
];

const CURRENT_USER_ID = 'user1';

interface SearchModalProps {
  visible: boolean;
  onClose: () => void;
  onSendFriendRequest: (userId: string) => void;
  onViewProfile: (userId: string) => void;
  friendRequests: {from: string, to: string, status: 'pending' | 'accepted' | 'rejected'}[];
  friends: string[];
}

export const SearchModal: React.FC<SearchModalProps> = ({ visible, onClose,  onViewProfile }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<UserData[]>([]);

  // Gestina la búsqueda
  const handleSearch = (query: string) => {
    setSearchQuery(query);
    if (query.trim() === '') {
      setSearchResults([]);
      return;
    }

    // Filtra los usuarios
    const filteredUsers = MOCK_ALL_USERS.filter(user => 
      user.id !== CURRENT_USER_ID && // Excluir al usuario actual
      (user.name.toLowerCase().includes(query.toLowerCase()) || 
       user.username.toLowerCase().includes(query.toLowerCase()))
    );
    setSearchResults(filteredUsers);
  };

  // Renderiza la barra de búsqueda
  const renderUserItem = ({ item }: { item: UserData }) => (
    <View style={styles.userItem}>
      <TouchableOpacity 
        style={styles.userInfo}
        onPress={() => {
          onViewProfile(item.id);
        }}
      >
        <Image 
          source={{ uri: item.avatar || 'https://placehold.co/100x100/e2e8f0/64748b?text=U' }} 
          style={styles.userAvatar}
        />
        <View style={styles.userDetails}>
          <Text style={styles.userName}>{item.name}</Text>
          <Text style={styles.userUsername}>{item.username}</Text>
        </View>
      </TouchableOpacity>
    </View>
  );

  return (
    <Modal
      visible={visible}
      animationType="slide"
      onRequestClose={onClose}
    >
      <View style={styles.modalContainer}>
        {/* Header del Modal */}
        <View style={styles.modalHeader}>
          <Text style={styles.modalTitle}>Buscar Usuarios</Text>
          <TouchableOpacity onPress={onClose} style={styles.closeButton}>
            <Icon name="close" size={24} color={theme.textDark} />
          </TouchableOpacity>
        </View>

        {/* Barra de Búsqueda */}
        <View style={styles.searchContainer}>
          <Icon name="search" size={20} color={theme.textLight} style={styles.searchIcon} />
          <TextInput
            style={styles.searchInput}
            placeholder="Buscar por nombre o username..."
            value={searchQuery}
            onChangeText={handleSearch}
            autoFocus={true}
          />
        </View>

        {/* Resultados */}
        <FlatList
          data={searchResults}
          renderItem={renderUserItem}
          keyExtractor={(item) => item.id}
          style={styles.resultsList}
          ListEmptyComponent={
            <View style={styles.emptyState}>
              <Icon name="search-off" size={48} color={theme.border} />
              <Text style={styles.emptyStateText}>
                {searchQuery ? 'No se encontraron usuarios' : 'Busca usuarios para agregar como amigos'}
              </Text>
            </View>
          }
        />
      </View>
    </Modal>
  );
};

const styles = StyleSheet.create({
  modalContainer: {
    flex: 1,
    backgroundColor: theme.bgWhite,
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 16,
    borderBottomWidth: 1,
    borderBottomColor: theme.border,
  },
  modalTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: theme.textDark,
  },
  closeButton: {
    padding: 4,
  },
  searchContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    margin: 16,
    paddingHorizontal: 20,
    backgroundColor: theme.bgLightGray,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: theme.border,
  },
  searchIcon: {
    marginRight: 8,
  },
  searchInput: {
    flex: 1,
    paddingHorizontal: 20,
    paddingVertical: 12,
    fontSize: 16,
    color: theme.textDark,
  },
  resultsList: {
    flex: 1,
  },
  userItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: theme.border,
  },
  userInfo: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
  },
  userAvatar: {
    width: 50,
    height: 50,
    borderRadius: 25,
    marginRight: 12,
  },
  userDetails: {
    flex: 1,
  },
  userName: {
    fontSize: 16,
    fontWeight: '500',
    color: theme.textDark,
    marginBottom: 2,
  },
  userUsername: {
    fontSize: 14,
    color: theme.textLight,
  },
  addButton: {
    backgroundColor: theme.primary,
    padding: 8,
    borderRadius: 20,
  },
  pendingButton: {
    backgroundColor: theme.textLight,
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 16,
  },
  pendingText: {
    color: theme.bgWhite,
    fontSize: 12,
    fontWeight: '500',
  },
  friendButton: {
    backgroundColor: theme.blue,
    padding: 8,
    borderRadius: 20,
  },
  emptyState: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 60,
  },
  emptyStateText: {
    marginTop: 12,
    fontSize: 16,
    color: theme.textLight,
    textAlign: 'center',
  },
});