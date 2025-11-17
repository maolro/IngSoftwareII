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
  Modal, 
} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';
import { theme } from './components';
import { DashboardScreen } from './dashboard';
import { BreweriesScreen } from './cervecerias';
import ProfileScreen from './profile';
import NotificationsScreen from './notifications';
import { SearchModal } from './search';
import api from './api'; 

const CURRENT_USER_ID = 1;

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
    <TouchableOpacity style={styles.navItem} onPress={() => onNavigate('breweries')}>
      <Icon name="map" size={28} color={activePage === 'breweries' ? theme.primary : theme.textLight} />
      <Text style={[styles.navLabel, activePage === 'breweries' && styles.navLabelActive]}>
        Cervecerías
      </Text>
    </TouchableOpacity>
    <TouchableOpacity style={styles.navItem} onPress={() => onNavigate('home')}>
      <Icon name="home" size={28} color={activePage === 'home' ? theme.primary : theme.textLight} />
      <Text style={[styles.navLabel, activePage === 'home' && styles.navLabelActive]}>
        Inicio
      </Text>
    </TouchableOpacity>
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
  const [searchModalVisible, setSearchModalVisible] = useState(false);
  const [viewingProfileId, setViewingProfileId] = useState<number | null>(null);
  // Estado para solicitudes de amistad 
  const [friendRequests, setFriendRequests] = useState<{ from: number, to: number, 
    status: 'pending' | 'accepted' | 'rejected' }[]>([]);
  // Estado para amigos que se cargará desde la API
  const [friends, setFriends] = useState<number[]>([]);
  // Historial de perfiles
  const [profileHistory, setProfileHistory] = useState<number[]>([CURRENT_USER_ID]);

  // Cargar los amigos del usuario actual al iniciar la app
  useEffect(() => {
    const loadFriends = async () => {
      try {
        const friendsData = await api.users.getFriends(CURRENT_USER_ID);
        const friendIds = friendsData.map(user => user.id);
        console.log("Amigos: "+friendIds.toString())
        setFriends(friendIds);
      } catch (error) {
        console.error("Error al cargar amigos:", error);
      }
    };

    loadFriends();
  }, []); 

  // Efecto para actualizar el botón de atrás
  useEffect(() => {
    if (activePage === 'profile' && profileHistory.length > 1) {
      setHeaderProps({ onBack: handleBack });
    } else {
      setHeaderProps({ onBack: null });
    }
  }, [activePage, profileHistory]);

  // Cambio de pantalla y visualización de un perfil
  const handleViewProfile = (userId: number) => {
    setProfileHistory(prev => [...prev, userId]);
    setViewingProfileId(userId);
    setActivePage('profile');
    setSearchModalVisible(false);
  };

  // Navega a un perfil y gestiona el historial de navegación
  const handleNavigateToProfile = (page: PageName) => {
    if (page === 'profile') {
      if (profileHistory[profileHistory.length - 1] !== CURRENT_USER_ID) {
        setProfileHistory(prev => [...prev, CURRENT_USER_ID]);
      }
      setViewingProfileId(CURRENT_USER_ID);
    }
    setActivePage(page);
  };

  // Función para enviar solicitudes de amistad
  const handleSendFriendRequest = async (userId: number) => {
    try {
      // Llama a la API
      await api.users.addFriend(CURRENT_USER_ID, userId);

      // Actualiza la UI
      setFriendRequests(prev => [...prev, {
        from: CURRENT_USER_ID,
        to: userId,
        status: 'pending'
      }]);
      console.log(`Solicitud de amistad enviada a ${userId} via API`);
    } catch (error) {
      console.error("Error al enviar solicitud de amistad:", error);
    }
  };

  // Lógica sin cambios, funciona con números
  const handleBack = () => {
    if (profileHistory.length > 1) {
      const newHistory = profileHistory.slice(0, -1);
      setProfileHistory(newHistory);

      const previousProfileId = newHistory[newHistory.length - 1];

      if (previousProfileId === CURRENT_USER_ID) {
        setViewingProfileId(null);
      } else {
        setViewingProfileId(previousProfileId);
      }

      setActivePage('profile');
    } else {
      setActivePage('home');
      setViewingProfileId(null);
    }
  };

  const getCurrentProfileId = () => {
    if (viewingProfileId) {
      return viewingProfileId;
    }
    return profileHistory[profileHistory.length - 1] === CURRENT_USER_ID ? null : profileHistory[profileHistory.length - 1];
  };

  // Función que decide qué pantalla renderizar
  const renderPage = () => {
    switch (activePage) {
      case 'home':
        return <DashboardScreen userId={CURRENT_USER_ID} />;
      case 'breweries':
        return <BreweriesScreen userId={CURRENT_USER_ID} setHeaderProps={setHeaderProps} />;
      case 'profile':
        return (
          <ProfileScreen
            userId={getCurrentProfileId()} 
            currentUserId={CURRENT_USER_ID}
            friends={friends} 
            friendRequests={friendRequests}
            onSendFriendRequest={handleSendFriendRequest} 
            onViewProfile={handleViewProfile} 
            setHeaderProps={setHeaderProps}
          />
        );
      case 'notifications':
        return <NotificationsScreen />;
      default:
        return <DashboardScreen userId={CURRENT_USER_ID} />;
    }
  };

  return (
    <SafeAreaView style={styles.phoneMockup}>
      <StatusBar barStyle="dark-content" backgroundColor={theme.bgWhite} />

      <AppHeader
        headerProps={headerProps}
        onNavigate={handleNavigateToProfile}
        onOpenSearch={() => setSearchModalVisible(true)}
      />

      <ScrollView style={styles.appMain}>
        {renderPage()}
      </ScrollView>

      <AppFooter activePage={activePage} onNavigate={handleNavigateToProfile} />

      <SearchModal
        onViewProfile={handleViewProfile}
        visible={searchModalVisible}
        onClose={() => setSearchModalVisible(false)}
      />
    </SafeAreaView>
  );
}

// --- Estilos de App.tsx ---
// (Sin cambios)
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
    backgroundColor: '#cfd60bff',
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