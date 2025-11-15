export interface Cerveza {
  id: string;
  name: string;
  style: string;
  rating: number;
  breweryId: string;
}

export interface Cerveceria {
  id: string;
  name: string;
  address: string;
}

export interface Degustacion {
  id: string;
  beerId: string;
  author: string;
  text: string;
  rating: number;
}

export interface Usuario {
  id: string;
  name: string;
  username: string;
  avatar: string;
  email: string;
  origin: string;
  memberSince: string;
}

export interface ReviewInfo {
  id: string;
  title: string;
  subtitle: string;
}

export interface UserData {
    id: string;
    name: string;
    username: string;
    avatar?: string;
}