# Proceso para arrancar la app

https://docs.expo.dev/tutorial/create-your-first-app/

1. Instalar node 20 y npm 10
2. Instalar expo ("npm install expo")
3. Iniciar la imagen docker de backend ("docker-compose up")
4. Entrar en la carpeta frontend ("cd frontend")
5. Instalar todos los paquetes ("npm ci"). 
6. Ejecutar la app ("npx expo start")

# Arrancar la app en el móvil (continuar pasos anteriores)

1. Instalarse ngrok y ejecutar el comando "ngrok http 8000" (expondrá el puerto 8000 y generará un url)
2. Cambiar la constante base_url del fichero "index.tsx" al url generado con ngrok
3. Ejecutar la app con opción de tunnel ("npx expo start --tunnel")
4. Escanear el QR con la cámara (si iPhone) o la app Expo Go (si Android)
