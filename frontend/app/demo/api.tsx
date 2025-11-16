// api.tsx
const API_BASE_URL = 'http://localhost:8000/api';

// Interfaces para los tipos de datos
export interface User {
  user_id: number;
  username: string;
  email: string;
  birth_date?: string;
  created_at?: string;
  updated_at?: string;
  friends?: number[];
  avatar?: string;
}

export interface Beer {
  id: number;
  nombre: string;
  descripcion?: string;
  foto?: string;
  estilo: string;
  pais_procedencia: string;
  tamano?: string;
  formato?: string;
  porcentaje_alcohol?: number;
  ibu?: number;
  color?: string;
  valoracion_promedio?: number;
  total_valoraciones?: number;
}

export interface Tasting {
  id: number;
  usuario_id: number;
  cerveza_id: number;
  cerveceria_id?: number;
  puntuacion?: number;
  comentario?: string;
  fecha_creacion?: string;
  fecha_actualizacion?: string;
  nombre_usuario?: string;
  nombre_cerveza?: string;
}

export interface Brewery {
  id: number;
  nombre: string;
  direccion?: string;
  ciudad?: string;
  pais?: string;
  descripcion?: string;
  foto?: string;
}

export interface Comment {
  id: number;
  degustacion_id: number;
  usuario_id: number;
  comentario: string;
  fecha_creacion?: string;
  usuario?: User;
}

// Cliente API genérico
class ApiClient {
  private baseURL: string;

  constructor(baseURL: string) {
    this.baseURL = baseURL;
  }

  private async request(endpoint: string, options: RequestInit = {}) {
    const url = `${this.baseURL}${endpoint}`;
    
    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      console.log(`API Call: ${options.method || 'GET'} ${url}`);
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error(`API Error: ${response.status} - ${errorText}`);
        throw new Error(`HTTP ${response.status}: ${errorText}`);
      }

      // Para respuestas sin contenido (como DELETE)
      if (response.status === 204) {
        return null;
      }

      const responseForText = response.clone();
    
      try {
        // Intenta parsear como JSON
        const data = await response.json();
        // Imprime el JSON de forma legible
        console.log(`Respuesta JSON ${url}:`, JSON.stringify(data, null, 2));
        return data;
        
      } catch (jsonError) {
        // Si falla el .json() muestra el texto plano
        console.error(`JSON no parseable. Este es el texto:`, await responseForText.text());
        throw jsonError;
      }
      } catch (error) {
        console.error(`💥 Network error for ${url}:`, error);
        throw error;
      }
  }

  async get(endpoint: string) {
    return this.request(endpoint, { method: 'GET' });
  }

  async post(endpoint: string, data: any) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async put(endpoint: string, data: any) {
    return this.request(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async delete(endpoint: string) {
    return this.request(endpoint, { method: 'DELETE' });
  }
}

// Instancia del cliente API
const apiClient = new ApiClient(API_BASE_URL);

// Servicios específicos por entidad
export const api = {
  // --- USUARIOS ---
  users: {
    // Obtener todos los usuarios
    getAll: (): Promise<User[]> => apiClient.get('/usuarios/'),
    
    // Obtener usuario por ID
    getById: (id: number): Promise<User> => apiClient.get(`/usuarios/${id}/`),
    
    // Crear usuario
    create: (userData: {
      username: string;
      email: string;
      password: string;
      birth_date: string;
    }): Promise<User> => apiClient.post('/usuarios/', userData),
    
    // Actualizar usuario
    update: (id: number, userData: Partial<User>): Promise<User> => 
      apiClient.put(`/usuarios/${id}/`, userData),
    
    // Eliminar usuario
    delete: (id: number): Promise<void> => apiClient.delete(`/usuarios/${id}/`),
    
    // Amigos
    getFriends: (userId: number): Promise<User[]> => 
      apiClient.get(`/usuarios/${userId}/amigos/`),
    
    addFriend: (userId: number, friendId: number): Promise<any> =>
      apiClient.post(`/usuarios/${userId}/amigos/`, { friend_id: friendId }),
    
    removeFriend: (userId: number, friendId: number): Promise<void> =>
      apiClient.delete(`/usuarios/${userId}/amigos/${friendId}/`),
  },

  // --- CERVEZAS ---
  beers: {
    // Obtener todas las cervezas (con filtros opcionales)
    getAll: (params?: { q?: string; estilo?: string; pais?: string }): Promise<Beer[]> => {
      const queryParams = params ? new URLSearchParams(params).toString() : '';
      const endpoint = queryParams ? `/cervezas/?${queryParams}` : '/cervezas/';
      return apiClient.get(endpoint);
    },
    
    // Obtener cerveza por ID
    getById: (id: number): Promise<Beer> => apiClient.get(`/cervezas/${id}/`),
    
    // Crear cerveza
    create: (beerData: {
      nombre: string;
      estilo: string;
      pais_procedencia: string;
      descripcion?: string;
      porcentaje_alcohol?: number;
      ibu?: number;
    }): Promise<Beer> => apiClient.post('/cervezas/', beerData),
    
    // Eliminar cerveza
    delete: (id: number): Promise<void> => apiClient.delete(`/cervezas/${id}/`),
    
    // Obtener estilos únicos
    getStyles: (): Promise<string[]> => apiClient.get('/cervezas/estilos/'),
    
    // Obtener países únicos
    getCountries: (): Promise<string[]> => apiClient.get('/cervezas/paises/'),
    
    // Obtener valoración promedio
    getRating: (beerId: number): Promise<{ valoracion_promedio: number }> =>
      apiClient.get(`/cervezas/${beerId}/valoracion/`),
    
    // Obtener cervezas favoritas de un usuario
    getFavorites: (userId: number): Promise<Beer[]> =>
      apiClient.get(`/usuarios/${userId}/cervezas/favoritas/`),
  },

  // --- DEGUSTACIONES ---
  degustaciones: {
    // Obtener todas las degustaciones
    getAll: (): Promise<Tasting[]> => apiClient.get('/degustaciones/'),
    
    // Obtener degustación por ID
    getById: (id: number): Promise<Tasting> => apiClient.get(`/degustaciones/${id}/`),
    
    // Crear degustación
    create: (tastingData: {
      usuario_id: number;
      cerveza_id: number;
      cerveceria_id?: number;
      puntuacion?: number;
      comentario?: string;
    }): Promise<Tasting> => apiClient.post('/degustaciones/', tastingData),
    
    // Actualizar degustación
    update: (id: number, tastingData: Partial<Tasting>): Promise<Tasting> =>
      apiClient.put(`/degustaciones/${id}/`, tastingData),
    
    // Eliminar degustación
    delete: (id: number): Promise<void> => apiClient.delete(`/degustaciones/${id}/`),
    
    // Obtener degustaciones por usuario
    getByUser: (userId: number): Promise<Tasting[]> =>
      apiClient.get(`/degustaciones/?usuario_id=${userId}`),
    
    // Obtener degustaciones por cerveza
    getByBeer: (beerId: number): Promise<Tasting[]> =>
      apiClient.get(`/degustaciones/?cerveza_id=${beerId}`),
  },

  // --- COMENTARIOS ---
  comments: {
    // Obtener comentarios de una degustación
    getByTasting: (tastingId: number): Promise<Comment[]> =>
      apiClient.get(`/degustaciones/${tastingId}/comentarios/`),
    
    // Crear comentario
    create: (commentData: {
      degustacion_id: number;
      usuario_id: number;
      comentario: string;
    }): Promise<Comment> => apiClient.post('/comentarios/', commentData),
    
    // Eliminar comentario
    delete: (id: number): Promise<void> => apiClient.delete(`/comentarios/${id}/`),
  },

  // --- CERVECERÍAS ---
  breweries: {
    // Obtener todas las cervecerías
    getAll: (): Promise<Brewery[]> => apiClient.get('/cervecerias/'),
    
    // Obtener cervecería por ID
    getById: (id: number): Promise<Brewery> => apiClient.get(`/cervecerias/${id}/`),
    
    // Crear cervecería
    create: (breweryData: {
      nombre: string;
      direccion?: string;
      ciudad?: string;
      pais?: string;
    }): Promise<Brewery> => apiClient.post('/cervecerias/', breweryData),
    
    // Eliminar cervecería
    delete: (id: number): Promise<void> => apiClient.delete(`/cervecerias/${id}/`),
  },

  // --- GALARDONES (si los necesitas) ---
  awards: {
    getAll: (): Promise<any[]> => apiClient.get('/galardones/'),
    getByUser: (userId: number): Promise<any[]> => 
      apiClient.get(`/usuarios/${userId}/galardones/`),
  },
};

// Hook personalizado para usar la API en componentes React
export const useApi = () => {
  return api;
};

export default api;