import React, { useEffect, useState } from 'react';
import {
  StyleSheet,
  Text,
  View,
  SafeAreaView,
  ScrollView,
  Image,
  TouchableOpacity,
  StatusBar,
  FlatList,
  Modal,
} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';
import { theme } from './components';
import Dashboard from './dashboard';
import { BreweriesScreen } from './cervecerias';
import ProfileScreen from './profile';
import NotificationsScreen from './notifications';
import { SearchModal } from './search';

// Datos de prueba
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

// --- Definición de tipos ---
type PageName = 'home' | 'breweries' | 'profile' | 'notifications';

interface HeaderProps {
  onBack: (() => void) | null;
}

// --- Componentes de Layout (Header y Footer) ---

const AppHeader: React.FC<{ 
  headerProps: HeaderProps;
  onNavigate: (page: PageName) => void;
  onOpenSearch: () => void;
}> = ({ headerProps, onNavigate, onOpenSearch }) => (
  <View style={styles.appHeader}>
    {headerProps.onBack ? (
      <TouchableOpacity onPress={headerProps.onBack} style={styles.headerButton}>
        <Icon name="arrow-back" size={26} color={theme.textDark} />
      </TouchableOpacity>
    ) : (
      <TouchableOpacity onPress={onOpenSearch} style={styles.headerButton}>
        <Icon name="search" size={26} color={theme.textDark} />
      </TouchableOpacity>
    )}
    
    <Image source={require('../../assets/logo.png')} style={styles.logo} />
    
    <TouchableOpacity onPress={() => onNavigate('notifications')}>
      <Icon name="notifications" size={26} color={theme.textDark} />
    </TouchableOpacity>
  </View>
);

const AppFooter: React.FC<{
  activePage: PageName;
  onNavigate: (page: PageName) => void;
}> = ({ activePage, onNavigate }) => (
  <View style={styles.appFooter}>
    {/* Ítem de Cervecerías */}
    <TouchableOpacity style={styles.navItem} onPress={() => onNavigate('breweries')}>
      <Icon name="map" size={28} color={activePage === 'breweries' ? theme.primary : theme.textLight} />
      <Text style={[styles.navLabel, activePage === 'breweries' && styles.navLabelActive]}>
        Cervecerías
      </Text>
    </TouchableOpacity>
    {/* Ítem de Inicio */}
    <TouchableOpacity style={styles.navItem} onPress={() => onNavigate('home')}>
      <Icon name="home" size={28} color={activePage === 'home' ? theme.primary : theme.textLight} />
      <Text style={[styles.navLabel, activePage === 'home' && styles.navLabelActive]}>
        Inicio
      </Text>
    </TouchableOpacity>
    {/* Ítem de Perfil */}
    <TouchableOpacity style={styles.navItem} onPress={() => onNavigate('profile')}>
      <Icon name="person" size={28} color={activePage === 'profile' ? theme.primary : theme.textLight} />
      <Text style={[styles.navLabel, activePage === 'profile' && styles.navLabelActive]}>
        Perfil
      </Text>
    </TouchableOpacity>
  </View>
);

// --- Componente Principal ---
export default function App() {
  const [activePage, setActivePage] = useState<PageName>('home');
  const [headerProps, setHeaderProps] = useState<HeaderProps>({ onBack: null });
  const [viewingProfileId, setViewingProfileId] = useState<string | null>(null);
  const [searchModalVisible, setSearchModalVisible] = useState(false);
  const [friendRequests, setFriendRequests] = useState<{from: string, to: string, status: 'pending' | 'accepted' | 'rejected'}[]>([]);
  const [friends, setFriends] = useState<string[]>(['user2', 'user3']); //simula amigos
  // Para visitar perfiles anteriores
  const [profileHistory, setProfileHistory] = useState<(string | null)[]>([null]);

  useEffect(() => {
    // Si estamos en "profile" Y el historial es > 1 (o sea, no en nuestro perfil base)
    if (activePage === 'profile' && profileHistory.length > 1) {
      setHeaderProps({ onBack: handleBack });
    } else if (activePage === 'breweries' && headerProps.onBack) {
      // Dejar que BreweriesScreen gestione su propio header
    } else {
      // En cualquier otra página principal, quitar el botón "back"
      setHeaderProps({ onBack: null });
    }
  }, [activePage, profileHistory, headerProps.onBack]); // Depender del historial

  const handleViewProfile = (userId: string) => {
    setProfileHistory(prev => [...prev, userId]);
    setViewingProfileId(userId);
    setActivePage('profile');
    setSearchModalVisible(false);
  };

  // Reset viewing profile when navigating to own profile
  const handleNavigateToProfile = (page: PageName) => {
    if (page === 'profile') {
      setViewingProfileId(null); // Reset to show current user's profile
    }
    setActivePage(page);
  };

  // Gestiona el envío de solicitudes de amistad
  const handleSendFriendRequest = (userId: string) => {
    // Normalmente usaría API
    setFriendRequests(prev => [...prev, {
      from: CURRENT_USER_ID,
      to: userId,
      status: 'pending'
    }]);
    console.log(`Friend request sent to ${userId}`);
  };

  // Gestiona volver atrás al buscar perfiles 
  const handleBack = () => {
    // Quitar el último perfil del historial para "volver"
    setProfileHistory(prev => prev.slice(0, -1));
  };

  // Función que decide qué pantalla renderizar
  const renderPage = () => {
    switch (activePage) {
      case 'home':
        return <Dashboard />;
      case 'breweries':
        return <BreweriesScreen setHeaderProps={setHeaderProps} />;
      case 'profile':
        return <ProfileScreen userId={viewingProfileId} friends={friends}
        friendRequests={friendRequests} onSendFriendRequest={handleSendFriendRequest}
        onViewProfile={handleViewProfile} setHeaderProps={setHeaderProps} />;
      case 'notifications':
        return <NotificationsScreen />;
      default:
        return <Dashboard />;
    }
  };


  return (
    <SafeAreaView style={styles.phoneMockup}>
      <StatusBar barStyle="dark-content" backgroundColor={theme.bgWhite} />
      
      {/* Cabecera de la app */}
      <AppHeader 
        headerProps={headerProps} 
        onNavigate={handleNavigateToProfile} 
        onOpenSearch={() => setSearchModalVisible(true)}
      />

      {/* Main Content (Scrollable) */}
      <ScrollView style={styles.appMain}>
        {renderPage()}
      </ScrollView>

      {/* Bottom Navigation */}
      <AppFooter activePage={activePage} onNavigate={handleNavigateToProfile} />

      {/* Search Modal */}
      <SearchModal
        onViewProfile={handleViewProfile}
        visible={searchModalVisible}
        onClose={() => setSearchModalVisible(false)}
      />
    </SafeAreaView>
  );
}


// --- Estilos de App.tsx (solo los necesarios para el layout) ---
const styles = StyleSheet.create({
  phoneMockup: {
    flex: 1,
    backgroundColor: theme.bgWhite,
  },
  appHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: theme.border,
    backgroundColor: '#cfd60bff', // Tu color de header original
  },
  logo: {
    width: 100,
    height: 45,
    marginBottom: 5,
    resizeMode: 'contain',
  },
  appMain: {
    flex: 1,
    backgroundColor: theme.bgLightGray,
  },
  appFooter: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    alignItems: 'center',
    paddingVertical: 12,
    borderTopWidth: 1,
    borderTopColor: theme.border,
    backgroundColor: theme.bgWhite,
  },
  navItem: {
    alignItems: 'center',
  },
  navLabel: {
    fontSize: 12,
    marginTop: 2,
    color: theme.textLight,
  },
  navLabelActive: {
    color: theme.primary,
  },
  headerButton: {
    width: 40,
    alignItems: 'center',
  },
});
