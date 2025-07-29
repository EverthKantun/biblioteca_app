# Sistema de Gestión de Biblioteca 

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13%2B-blue)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green)

Sistema para administrar bibliotecas con control de usuarios, libros, préstamos y reportes estadísticos.

## Características Principales 

- **Gestión de Libros**:
  - Registro de nuevos libros (título, autor, año)
  - Búsqueda y actualización de información
  - Control de disponibilidad (prestado/disponible)

- **Gestión de Usuarios**:
  - Registro de clientes (nombre, dirección, teléfono)
  - Historial de préstamos
  - Modificación de datos

- **Transacciones**:
  - Sistema completo de préstamos y devoluciones
  - Validación de disponibilidad
  - Registro de fechas automático

- **Reportes Avanzados**:
  - Gráficos de libros más prestados (Top 5)
  - Estadísticas de usuarios más activos
  - Tasa de disponibilidad general
  - Estado actual de todos los libros

## Tecnologías Utilizadas 

- **Backend**:
  - Python 3.8+
  - PostgreSQL (Manejado con psycopg2)
  - Variables de entorno (.env)

- **Frontend**:
  - Tkinter (Interfaz gráfica)
  - Matplotlib (Gráficos estadísticos)

