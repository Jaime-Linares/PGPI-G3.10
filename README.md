## CityScape Rentals

* In the folder *docs*, you have all the documents related to the project: project plan, requirements record...
* In the folder *product*, you have the application code, that is, the code of the web platform for renting tourist apartments.

# Enlace despliegue:
```https://pgpig310.pythonanywhere.com/```

# Análisis de Sonarqube
```https://sonarcloud.io/summary/overall?id=Jaime-Linares_PGPI-G3.10```


# Cómo cargar y usar la imagen Docker

Estos son los pasos necesarios para cargar y usar una imagen Docker exportada en otro dispositivo.  
Es necesario tener Docker instalado en el equipo.

## **1. Exportar la imagen desde el dispositivo original (Solo chico cuando esté terminado todo)**

Guarda la imagen Docker en un archivo `.tar` en el dispositivo de origen:

```docker save -o city-scape-rentals.tar city-scape-rentals ```  

  ---

## 2. Transferir la imagen al nuevo dispositivo

### Opción 1:   
Descargar el archivo `alvarochico2408/city-scape-rentals.tar` adjunto.  

### Opción2:  
Iniciar sesión en docker:  
```docker login```

Descargar la imagen subida en dockerHub:  
```docker pull alvarochico2408/city-scape-rentals:latest```

---

## 3. Cargar la imagen en el nuevo dispositivo

### Si antes has optado por la opción 1:
En el dispositivo, asegúrate de que Docker esté instalado y funcionando. Luego, usa el siguiente comando para cargar la imagen desde el archivo `.tar`:

```docker load -i alvarochico2408/city-scape-rentals.tar```  

Este comando importará la imagen a Docker. Puedes verificar que la imagen se cargó correctamente con:  

```docker images```

Deberías ver algo como:

```REPOSITORY                           TAG       IMAGE ID       CREATED        SIZE```  
```alvarochico2408/city-scape-rentals  latest    1a2b3c4d5e6f   2 days ago     544MB```  


### Si has optado por la opción 2, este paso no es necesario.
---

## **4. Ejecutar la imagen**
Ahora que la imagen está disponible, puedes usarla para crear y ejecutar un contenedor:  

```docker run -p 8000:8000 --name alvarochico2408/city-scape-rentals city-scape-rentals```

Esto iniciará un contenedor basado en la imagen city-scape-rentals y mapeará el puerto 8000 del contenedor al puerto 8000 del host.  

Accede a la aplicación en el navegador en:  
```http://localhost:8000```

## Ejecutar pruebas:

### Instalación de SonarScanner

#### macOS/Linux:
```brew install sonar-scanner```

## Windows/Linux (manual):
####    - Descarga SonarScanner CLI.
```https://docs.sonarsource.com/sonarqube/10.4/analyzing-source-code/scanners/sonarscanner/```
####    - Extrae los archivos y agrega la carpeta bin a la variable de entorno PATH.

### Verifica la instalación:
```sonar-scanner --version```
### Una vez descargado todo lo necesario:

## **1. Ejecutar los tests y generar la cobertura.**
```cd product/ProyectoWeb```
```coverage run --source=product/ProyectoWeb -m test```
```coverage xml```

## **2. Ejecutar SonarScanner (En una nueva terminal) **
```sonar-scanner```

## **3. Limpiar archivos temporales.**
```find . -type d -name ".scannerwork" -exec rm -rf {} +```





