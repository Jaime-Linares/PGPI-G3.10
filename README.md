## CityScape Rentals

* In the folder *docs*, you have all the documents related to the project: project plan, requirements record...
* In the folder *product*, you have the application code, that is, the code of the web platform for renting tourist apartments.

# Cómo cargar y usar la imagen Docker

Estos son los pasos necesarios para cargar y usar una imagen Docker exportada en otro dispositivo.  
Es necesario tener Docker instalado en el equipo.

## **1. Exportar la imagen desde el dispositivo original (Solo chico cuando esté terminado todo)**

Guarda la imagen Docker en un archivo `.tar` en el dispositivo de origen:

```docker save -o city-scape-rentals.tar city-scape-rentals ```  

  ---

## 2. Transferir la imagen al nuevo dispositivo

Descargar el archivo `city-scape-rentals.tar` de la carpeta docker.  

---

## 3. Cargar la imagen en el nuevo dispositivo

En el dispositivo, asegúrate de que Docker esté instalado y funcionando. Luego, usa el siguiente comando para cargar la imagen desde el archivo `.tar`:

```docker load -i city-scape-rentals.tar```  

Este comando importará la imagen a Docker. Puedes verificar que la imagen se cargó correctamente con:  

```docker images```

Deberías ver algo como:

```REPOSITORY          TAG       IMAGE ID       CREATED        SIZE```  
```city-scape-rentals  latest    1a2b3c4d5e6f   2 days ago     544MB```  

---

## **4. Ejecutar la imagen**
Ahora que la imagen está disponible, puedes usarla para crear y ejecutar un contenedor:  

```docker run -p 8000:8000 --name city-scape-rentals city-scape-rentals```

Esto iniciará un contenedor basado en la imagen city-scape-rentals y mapeará el puerto 8000 del contenedor al puerto 8000 del host.  

Accede a la aplicación en el navegador en:  
```http://localhost:8000```




