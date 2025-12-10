// Constantes de la aplicación
import React from 'react';
import { View, Text, Image, StyleSheet, TouchableOpacity } from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';

// El tema de la aplicaicón
export const theme = {
  primary: '#ca8a04',
  primaryLight: '#fefce8',
  textDark: '#1f2937',
  textLight: '#6b7280',
  border: '#e5e7eb',
  bgWhite: '#ffffff',
  bgLightGray: '#f9fafb',
  blue: '#3b82f6', 
  red: '#ef4444'
};

// Props del componente ListItem
interface ListItemProps {
  title: string;
  subtitle: string;
  avatarUrl?: string;
  iconName?: string;
  avatarText?: string;
}

// Props del componente Touchable list
interface TouchableListItemProps {
  title: string;
  subtitle: string;
  onPress: () => void;
  iconName?: string;
  avatarText?: string;
}

// Lista estática (no se puede clicar)
export function ListItem({
  title,
  subtitle,
  avatarUrl,
  iconName,
  avatarText,
}: ListItemProps) {
  return (
    <View style={styles.listItem}>
      {iconName && <Icon name={iconName} size={24} style={styles.listItemIcon} />}
      {avatarUrl && <Image source={{ uri: avatarUrl }} style={styles.listItemAvatar} />}
      {avatarText && !avatarUrl && (
        <View style={[styles.listItemAvatar, styles.avatarPlaceholder]}>
          <Text style={styles.avatarPlaceholderText}>{avatarText}</Text>
        </View>
      )}
      <View style={styles.listItemContent}>
        <Text style={styles.listItemTitle}>{title}</Text>
        <Text style={styles.listItemSubtitle}>{subtitle}</Text>
      </View>
    </View>
  );
}
type CardProps = {
  title: string;
  children: React.ReactNode;
};

// Componente Card
export function Card({ title, children }: CardProps) {
  return (
    <View style={styles.card}>
      <Text style={styles.cardTitle}>{title}</Text>
      {children}
    </View>
  );
}

// Lista dinámica (a la que se puede clicar)
export function TouchableListItem({
  title,
  subtitle,
  onPress,
  iconName,
  avatarText,
} : TouchableListItemProps){
  return (
    <TouchableOpacity style={styles.listItem} onPress={onPress}>
      {iconName && <Icon name={iconName} size={24} style={styles.listItemIcon} />}
      {avatarText && (
        <View style={[styles.listItemAvatar, styles.avatarPlaceholder]}>
          <Text style={styles.avatarPlaceholderText}>{avatarText}</Text>
        </View>
      )}
      <View style={styles.listItemContent}>
        <Text style={styles.listItemTitle}>{title}</Text>
        <Text style={styles.listItemSubtitle}>{subtitle}</Text>
      </View>
      <Icon name="chevron-right" size={24} color={theme.textLight} />
    </TouchableOpacity>
  );
}

// Estilos locales solo para Card
const styles = StyleSheet.create({
  card: {
    backgroundColor: theme.bgWhite,
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: theme.border,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.03,
    shadowRadius: 3,
    elevation: 2,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: '500',
    marginBottom: 12,
    color: theme.textDark,
  },
  listItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: theme.border,
  },
  listItemIcon: {
    marginRight: 12,
    color: theme.primary,
  },
  listItemAvatar: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: theme.border,
    marginRight: 12,
  },
  avatarPlaceholder: {
    backgroundColor: theme.border,
    justifyContent: 'center',
    alignItems: 'center',
  },
  avatarPlaceholderText: {
    color: theme.textLight,
    fontWeight: '700',
  },
  listItemContent: {
    flex: 1,
  },
  listItemTitle: {
    fontWeight: '500',
    color: theme.textDark,
    fontSize: 16,
  },
  listItemSubtitle: {
    fontSize: 14,
    color: theme.textLight,
    marginTop: 2,
  },
});
