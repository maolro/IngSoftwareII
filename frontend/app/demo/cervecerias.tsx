import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { Card, ListItem, TouchableListItem, theme} from './components';
import { Cerveza, Cerveceria, Degustacion } from './objects';
import { ReviewForm } from './degustacion';

// Datos de prueba para cervecerías (luego se cogerán usando la API)
const MOCK_BREWERIES: Cerveceria[] = [
  { id: 'b1', name: 'La Fábrica Maravillas', address: 'Calle de Valverde, 29, Madrid' },
  { id: 'b2', name: 'Peninsula', address: 'Calle de La Ruda, 12, Madrid' },
  { id: 'b3', name: 'El Oso y el Madroño Taproom', address: 'Calle de la Victoria, 3, Madrid' },
];

// Datos de prueba para cervezas (luego se cogerán usando la API)
export const MOCK_BEERS: Cerveza[] = [
  { id: 'beer1', name: 'Malasaña Ale', style: 'Pale Ale', rating: 4.2, breweryId: 'b1' },
  { id: 'beer2', name: 'Maravillas Pilsner', style: 'Pilsner', rating: 4.0, breweryId: 'b1' },
  { id: 'beer3', name: 'Puro Tropico', style: 'IPA', rating: 4.5, breweryId: 'b2' },
  { id: 'beer4', name: 'Hop Revolution', style: 'NEIPA', rating: 4.7, breweryId: 'b2' },
  { id: 'beer5', 'name': 'Oso Famoso', style: 'Lager', rating: 3.8, breweryId: 'b3' },
];

// Datos de prueba para degustaciones (luego se cogerán usando la API)
const MOCK_REVIEWS: Degustacion[] = [
  { id: 'r1', beerId: 'beer1', author: 'Ana López', text: 'Muy sabrosa, un clásico de Malasaña.', rating: 4.0 },
  { id: 'r2', beerId: 'beer3', author: 'Bruno Reyes', text: '¡Tropicana pura! Me encanta.', rating: 5.0 },
  { id: 'r3', beerId: 'beer4', author: 'Usuario Demo', text: 'Increíblemente turbia y frutal.', rating: 4.8 },
  { id: 'r4', beerId: 'beer5', author: 'Ana López', text: 'Una lager sencilla, para pasar el rato.', rating: 3.0 },
  { id: 'r5', beerId: 'beer1', author: 'Carlos Diaz', text: 'Un poco cara, pero buena.', rating: 3.5 },
];

// Lista de todas las cervecerías
const BreweryList: React.FC<{
  onSelectBrewery: (brewery: Cerveceria) => void;
}> = ({ onSelectBrewery }) => (
  <View style={styles.page}>
    <Text style={styles.pageTitle}>Cervecerías</Text>
    <Card title="Cervecerías Cercanas">
      {MOCK_BREWERIES.map(brewery => (
        <TouchableListItem
          key={brewery.id}
          title={brewery.name}
          subtitle={brewery.address}
          iconName="storefront"
          onPress={() => onSelectBrewery(brewery)}
        />
      ))}
    </Card>
  </View>
);

// Detalles de una cervecería
const BreweryDetail: React.FC<{
  brewery: Cerveceria;
  onSelectBeer: (beer: Cerveza) => void;
}> = ({ brewery, onSelectBeer }) => {
  const beers = MOCK_BEERS.filter(beer => beer.breweryId === brewery.id);

  return (
    <View style={styles.page}>
      <Text style={styles.detailTitle}>{brewery.name}</Text>
      <Text style={styles.detailSubtitle}>{brewery.address}</Text>

      <Card title="Cervezas">
        {beers.length > 0 ? (
          beers.map(beer => (
            <TouchableListItem
              key={beer.id}
              title={beer.name}
              subtitle={beer.style}
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

// Screen 2.3: Details for one beer
const BeerDetail: React.FC<{beer: Cerveza; onWriteReview: () => void; reviews: Degustacion[];}
> = ({ beer, onWriteReview, reviews }) => {
  return (
    <View style={styles.page}>
      <Text style={styles.detailTitle}>{beer.name}</Text>
      <Text style={styles.detailSubtitle}>{beer.style}</Text>
      <Text style={styles.detailRating}>Rating Promedio: {beer.rating} ★</Text>

      <TouchableOpacity style={styles.button} onPress={onWriteReview}>
        <Text style={styles.buttonText}>Añadir Reseña</Text>
      </TouchableOpacity>

      <Card title="Reseñas Recientes">
        {reviews.length > 0 ? (
          reviews.map(review => (
            <ListItem
              key={review.id}
              title={review.author}
              subtitle={`${review.text} (${review.rating} ★)`}
              avatarText={review.author.substring(0, 2).toUpperCase()}
            />
          ))
        ) : (
          <Text style={styles.emptyStateText}>
            No hay reseñas para esta cerveza. ¡Sé el primero!
          </Text>
        )}
      </Card>
    </View>
  );
};

// --- Main Navigator Component for this Feature ---

interface BreweryFeatureScreenProps {
  // This prop will be used to update the main App header
  setHeaderProps: (props: { title: string; onBack: (() => void) | null }) => void;
}

export const BreweriesScreen: React.FC<BreweryFeatureScreenProps> = ({
  setHeaderProps,
}) => {
  const [selectedBrewery, setSelectedBrewery] = useState<Cerveceria | null>(null);
  const [selectedBeer, setSelectedBeer] = useState<Cerveza | null>(null);
  const [isWritingReview, setIsWritingReview] = useState<boolean>(false);
  const [reviews, setReviews] = useState<Degustacion[]>(MOCK_REVIEWS);

  // --- Navigation Handlers ---
  const handleSelectBrewery = (brewery: Cerveceria) => {
    setSelectedBrewery(brewery);
    setHeaderProps({ title: brewery.name, onBack: handleBackToBreweries });
  };
  
  const handleSelectBeer = (beer: Cerveza) => {
    setSelectedBeer(beer);
    setHeaderProps({ title: beer.name, onBack: handleBackToBrewery });
  };
  
  const handleWriteReview = () => setIsWritingReview(true);

  // --- Back Handlers ---
  const handleBackToBreweries = () => {
    setSelectedBrewery(null);
    setHeaderProps({ title: 'BeerSP', onBack: null });
  };
  
  const handleBackToBrewery = () => {
    setSelectedBeer(null);
    if (selectedBrewery) {
      setHeaderProps({ title: selectedBrewery.name, onBack: handleBackToBreweries });
    }
  };

  const handleCancelReview = () => setIsWritingReview(false);

  // --- Submit Handler ---
  const handleSubmitReview = (review: string, rating: number) => {
    if (!selectedBeer) return; // Safety check

    const newReview: Degustacion = {
      id: `review_${Date.now()}`, 
      beerId: selectedBeer.id,
      author: 'Usuario Demo', 
      text: review,
      rating: rating,
    };
    // Añade la nueva degustación
    setReviews(prevReviews => [newReview, ...prevReviews]);
    console.log(`Review for ${selectedBeer?.name}: ${review}, Rating: ${rating}`);
    setIsWritingReview(false);
  };

  // --- Lógica de renderización ---
  const renderContent = () => {
    if (selectedBeer) {
      // Filtra las reseñas
      const beerReviews = reviews.filter(r => r.beerId === selectedBeer.id);
      
      return (
        <BeerDetail 
          beer={selectedBeer} 
          onWriteReview={handleWriteReview} 
          reviews={beerReviews} // Pasa reseñas filtradas
        />
      );
    }
    if (selectedBrewery) {
      return (
        <BreweryDetail
          brewery={selectedBrewery}
          onSelectBeer={handleSelectBeer}
        />
      );
    }
    return <BreweryList onSelectBrewery={handleSelectBrewery} />;
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
});