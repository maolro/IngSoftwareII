import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ActivityIndicator, Alert } from 'react-native';
import { Card, ListItem, TouchableListItem, theme} from './components';
import { ReviewForm } from './degustacion';
import api, { Beer, Brewery, Tasting } from './api'

// Lista de todas las cervecerías
const BreweryList: React.FC<{
  onSelectBrewery: (brewery: Brewery) => void;
  breweries: Brewery[];
  loading: boolean;
}> = ({ onSelectBrewery, breweries, loading }) => (
  <View style={styles.page}>
    <Text style={styles.pageTitle}>Cervecerías</Text>
    <Card title="Cervecerías Cercanas">
      { loading ? (
          <ActivityIndicator size="small" color={theme.primary} />
        ) : breweries.length > 0 ? (
              breweries.map(brewery => (
                <TouchableListItem
                  key={brewery.id}
                  title={brewery.nombre}
                  subtitle={"" + brewery.direccion + ", " + brewery.pais}
                  iconName="storefront"
                  onPress={() => onSelectBrewery(brewery)}
                />
              ))
            ) : (
              <Text style={styles.emptyStateText}>
                No hay cervecerías disponibles.
              </Text>
        )
      }
    </Card>
  </View>
);

// Detalles de una cervecería
// Detalles de una cervecería
const BreweryDetail: React.FC<{
  brewery: Brewery;
  onSelectBeer: (beer: Beer) => void;
  beers: Beer[];
  loading: boolean;
}> = ({ brewery, onSelectBeer, beers, loading }) => {
  // Filtro de las cervezas
  const breweryBeers = beers.filter(beer => 
    true
  );
  return (
    <View style={styles.page}>
      <Text style={styles.detailTitle}>{brewery.nombre}</Text>
      <Text style={styles.detailSubtitle}>{"" + brewery.direccion + ", "
       + brewery.ciudad + ", " + brewery.pais}</Text>

      <Card title="Cervezas Disponibles">
        {loading ? (
          <ActivityIndicator size="small" color={theme.primary} />
        ) : breweryBeers.length > 0 ? (
          breweryBeers.map(beer => (
            <TouchableListItem
              key={beer.id}
              title={beer.nombre}
              subtitle={`${beer.estilo} · ${beer.pais_procedencia}`}
              iconName="sports-bar"
              onPress={() => onSelectBeer(beer)}
            />
          ))
        ) : (
          <Text style={styles.emptyStateText}>
            No hay cervezas registradas para este local.
          </Text>
        )}
      </Card>
    </View>
  );
};

// Detalles sobre una cerveza
const BeerDetail: React.FC<{
  beer: Beer;
  onWriteReview: () => void;
  reviews: Tasting[];
  loading: boolean;
}> = ({ beer, onWriteReview, reviews, loading }) => {
  return (
    <View style={styles.page}>
      <Text style={styles.detailTitle}>{beer.nombre}</Text>
      <Text style={styles.detailSubtitle}>{beer.estilo}</Text>
      <Text style={styles.detailRating}>
        {beer.valoracion_promedio ? 
          `Rating Promedio: ${beer.valoracion_promedio} ★` : 
          'Sin valoraciones aún'
        }
      </Text>

      <TouchableOpacity style={styles.button} onPress={onWriteReview}>
        <Text style={styles.buttonText}>Añadir Degustación</Text>
      </TouchableOpacity>

      <Card title="Degustaciones Recientes">
        {loading ? (
          <ActivityIndicator size="small" color={theme.primary} />
        ) : reviews.length > 0 ? (
          reviews.map(review => (
            <ListItem
              key={review.id}
              title={`${review.nombre_usuario || 'Usuario'}`}
              subtitle={`${review.comentario || 'Sin comentario'} ${
                review.puntuacion ? `(${review.puntuacion} ★)` : ''
              }`}
              avatarText={review.nombre_usuario?.substring(0, 2).toUpperCase() || 'U'}
            />
          ))
        ) : (
          <Text style={styles.emptyStateText}>
            No hay degustaciones para esta cerveza. ¡Sé el primero!
          </Text>
        )}
      </Card>
    </View>
  );
};

// --- Componente principal ---

interface BreweryFeatureScreenProps {
  // Variables que recibe de la cabecera
  userId: number; 
  setHeaderProps: (props: { onBack: (() => void) | null }) => void;
}

// Pantalla que se exporta
export const BreweriesScreen: React.FC<BreweryFeatureScreenProps> = ({
  userId, setHeaderProps,
}) => {
  const [selectedBrewery, setSelectedBrewery] = useState<Brewery | null>(null);
  const [selectedBeer, setSelectedBeer] = useState<Beer | null>(null);
  const [isWritingReview, setIsWritingReview] = useState<boolean>(false);
  
  // Estados de datos desde API
  const [breweries, setBreweries] = useState<Brewery[]>([]);
  const [beers, setBeers] = useState<Beer[]>([]);
  const [reviews, setReviews] = useState<Tasting[]>([]);
  
  // Estados de carga
  const [isLoading, setIsLoading] = useState(true);
  const [isBreweriesLoading, setIsBreweriesLoading] = useState(false);
  const [isBeersLoading, setIsBeersLoading] = useState(false);
  const [isReviewsLoading, setIsReviewsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Cargar datos iniciales
  useEffect(() => {
    loadInitialData();
  }, []);

  const loadInitialData = async () => {
    try {
      setIsLoading(true);
      setError(null);

      // Cargar cervecerías y cervezas en paralelo
      const [breweriesData, beersData] = await Promise.all([
        api.breweries.getAll(),
        api.beers.getAll()
      ]);

      setBreweries(breweriesData);
      setBeers(beersData);
      
    } catch (err) {
      console.error('Error cargando datos iniciales:', err);
      setError('Error al cargar los datos');
      Alert.alert("Error", "No se pudieron cargar las cervecerías y cervezas");
    } finally {
      setIsLoading(false);
    }
  };

  // Cargar degustaciones cuando se selecciona una cerveza
  useEffect(() => {
    if (selectedBeer) {
      loadBeerReviews(selectedBeer.id);
    }
  }, [selectedBeer]);

  const loadBeerReviews = async (beerId: number) => {
    try {
      setIsReviewsLoading(true);
      const reviewsData = await api.degustaciones.getByBeer(beerId);
      setReviews(reviewsData);
    } catch (err) {
      console.error('Error cargando degustaciones:', err);
      Alert.alert("Error", "No se pudieron cargar las degustaciones");
    } finally {
      setIsReviewsLoading(false);
    }
  };

  // --- Gestores de Navegación ---
  const handleSelectBrewery = (brewery: Brewery) => {
    setSelectedBrewery(brewery);
    setHeaderProps({ onBack: handleBackToBreweries });
  };
  
  const handleSelectBeer = (beer: Beer) => {
    setSelectedBeer(beer);
    setHeaderProps({ onBack: handleBackToBrewery });
  };
  
  const handleWriteReview = () => setIsWritingReview(true);

  // --- Gestión de la cabecera para volver atrás ---
  const handleBackToBreweries = () => {
    setSelectedBrewery(null);
    setSelectedBeer(null);
    setReviews([]);
    setHeaderProps({ onBack: null });
  };
  
  const handleBackToBrewery = () => {
    setSelectedBeer(null);
    setReviews([]);
    if (selectedBrewery) {
      setHeaderProps({ onBack: handleBackToBreweries });
    }
  };

  const handleCancelReview = () => setIsWritingReview(false);

  // --- Submit para nueva degustación ---
  const handleSubmitReview = async (review: string, rating: number) => {
    if (!selectedBeer) return;

    try {
      // Crear la nueva degustación
      const newTasting = await api.degustaciones.create({
        usuario_id: userId, // ID del usuario actual
        cerveza_id: selectedBeer.id,
        cerveceria_id: selectedBrewery?.id,
        puntuacion: rating,
        comentario: review,
      });

      // Actualizar la lista de degustaciones
      setReviews(prev => [newTasting, ...prev]);
      await loadBeerReviews(selectedBeer.id);
      
      // Actualizar la cerveza para reflejar posible cambio en valoración
      const updatedBeer = await api.beers.getById(selectedBeer.id);
      setBeers(prev => prev.map(beer => 
        beer.id === selectedBeer.id ? updatedBeer : beer
      ));

      console.log(`Degustación creada para ${selectedBeer.nombre}: ${review}, Rating: ${rating}`);
      setIsWritingReview(false);
      
      Alert.alert("Éxito", "Degustación añadida correctamente");
      
    } catch (err) {
      console.error('Error creating tasting:', err);
      Alert.alert("Error", "No se pudo crear la degustación");
    }
  };

  // --- Renderizado de estados de carga/error ---
  if (isLoading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color={theme.primary} />
        <Text style={styles.loadingText}>Cargando cervecerías y cervezas...</Text>
      </View>
    );
  }

  if (error) {
    return (
      <View style={styles.center}>
        <Text style={styles.errorText}>{error}</Text>
        <TouchableOpacity style={styles.retryButton} onPress={loadInitialData}>
          <Text style={styles.retryButtonText}>Reintentar</Text>
        </TouchableOpacity>
      </View>
    );
  }

  // --- Lógica de renderización ---
  const renderContent = () => {
    if (selectedBeer) {
      return (
        <BeerDetail 
          beer={selectedBeer} 
          onWriteReview={handleWriteReview} 
          reviews={reviews}
          loading={isReviewsLoading}
        />
      );
    }
    
    if (selectedBrewery) {
      return (
        <BreweryDetail
          brewery={selectedBrewery}
          onSelectBeer={handleSelectBeer}
          beers={beers}
          loading={isBeersLoading}
        />
      );
    }
    
    return (
      <BreweryList 
        onSelectBrewery={handleSelectBrewery} 
        breweries={breweries}
        loading={isBreweriesLoading}
      />
    );
  };

  return (
    <>
      {renderContent()}
      
      {isWritingReview && selectedBeer && (
        <ReviewForm
          beer={selectedBeer}
          onSubmit={handleSubmitReview}
          onCancel={handleCancelReview}
        />
      )}
    </>
  );
};

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
  detailTitle: {
    fontSize: 24,
    fontWeight: '700',
    color: theme.textDark,
    marginBottom: 4,
  },
  detailSubtitle: {
    fontSize: 16,
    color: theme.textLight,
    marginBottom: 16,
  },
  detailRating: {
    fontSize: 18,
    color: theme.textDark,
    marginBottom: 24,
  },
  emptyStateText: {
    padding: 16,
    color: theme.textLight,
    textAlign: 'center',
  },
  button: {
    backgroundColor: theme.blue,
    padding: 16,
    borderRadius: 8,
    alignItems: 'center',
    marginBottom: 20,
  },
  buttonText: {
    color: theme.bgWhite,
    fontSize: 16,
    fontWeight: '700',
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
  center: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
});