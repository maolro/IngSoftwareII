import React, { useState, useEffect } from 'react'; // --- MODIFICADO ---
import {
  StyleSheet,
  Text,
  View,
  Image,
  TouchableOpacity,
  TextInput,
  Modal,
  FlatList,
  ActivityIndicator, 
} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';
import { theme } from './components';
import api, { User } from './api';

interface SearchModalProps {
  visible: boolean;
  onClose: () => void;
  onViewProfile: (userId: number) => void;
}

export const SearchModal: React.FC<SearchModalProps> = ({
  visible,
  onClose,
  onViewProfile
}) => {
  const [searchQuery, setSearchQuery] = useState('');

  // Estados para manejar los datos de la API
  const [allUsers, setAllUsers] = useState<User[]>([]);
  const [searchResults, setSearchResults] = useState<User[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Carga todos los usuarios CUANDO el modal se hace visible
  useEffect(() => {
    // Solo cargar si el modal está visible y los usuarios no se han cargado
    if (visible && allUsers.length === 0) {
      const fetchAllUsers = async () => {
        setIsLoading(true);
        setError(null);
        try {
          const users = await api.users.getAll();
          setAllUsers(users);
        } catch (err) {
          setError((err as Error).message);
          console.error("Error al cargar usuarios:", err);
        } finally {
          setIsLoading(false);
        }
      };
      fetchAllUsers();
    }
  }, [visible]); // Se ejecuta cada vez que 'visible' cambia

  // Gestina la búsqueda
  const handleSearch = (query: string) => {
    setSearchQuery(query);
    if (query.trim() === '') {
      setSearchResults([]);
      return;
    }

    // Filtra los usuarios localmente
    const filteredUsers = allUsers.filter(user =>
      (user.username.toLowerCase().includes(query.toLowerCase()) ||
        (user.email && user.email.toLowerCase().includes(query.toLowerCase())))
    );
    setSearchResults(filteredUsers);
  };

  // Renderiza el item de usuario 
  const renderUserItem = ({ item }: { item: User }) => (
    <View style={styles.userItem}>
      <TouchableOpacity
        style={styles.userInfo}
        onPress={() => {
          console.log('Selected user:', item.id, item.username);
          onViewProfile(item.id);
          setSearchQuery('');
          setSearchResults([]);
        }}
      >
        <Image
          source={{ uri: item.avatar || 'https://placehold.co/100x100/e2e8f0/64748b?text=U' }}
          style={styles.userAvatar}
        />
        <View style={styles.userDetails}>
          <Text style={styles.userName}>{item.username}</Text>
          <Text style={styles.userUsername}>{item.email}</Text>
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

        {/* Barra de Búsqueda  */}
        <View style={styles.searchContainer}>
          <Icon name="search" size={20} color={theme.textLight} style={styles.searchIcon} />
          <TextInput
            style={styles.searchInput}
            placeholder="Buscar por nombre de usuario o email..." 
            value={searchQuery}
            onChangeText={handleSearch}
            autoFocus={true}
          />
        </View>

        {/* Resultados */}
        <FlatList
          data={searchResults}
          renderItem={renderUserItem}
          keyExtractor={(item) => item.username.toString()}
          style={styles.resultsList}
          ListEmptyComponent={
            <View style={styles.emptyState}>
              {isLoading ? (
                <ActivityIndicator size="large" color={theme.primary} />
              ) : error ? (
                <>
                  <Icon name="error-outline" size={48} color={theme.red} />
                  <Text style={styles.emptyStateText}>Error al cargar: {error}</Text>
                </>
              ) : (
                <>
                  <Icon name="search-off" size={48} color={theme.border} />
                  <Text style={styles.emptyStateText}>
                    {searchQuery ? 'No se encontraron usuarios' : 'Busca usuarios para agregar'}
                  </Text>
                </>
              )}
            </View>
          }
        />
      </View>
    </Modal>
  );
};

// --- Estilos ---
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