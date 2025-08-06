# Prueba Técnica – Data Engineer para Business Intelligence

En este repositorio se encuentran los ejercicios propuestos para la prueba técnica.
Cada carpeta tiene su respectivo README con los entregables para ese ejercicio.
Render fue seleccionada como base de datos PostgreSQL en la nube para esta prueba.
Las automatizaciones se hicieron con GitHub Actions para ejecutar `main.py` diariamente/semanalmente. Las credenciales sensibles se almacenan como [GitHub Secrets].

### Variables de entorno

- `ORIGIN_DB_URL`: conexión a la base local PostgreSQL.  
- `DEST_DB_URL`: conexión a la base en Render.  

### Automatización

Se usa GitHub Actions para ejecutar `main.py` diariamente. Las credenciales sensibles se almacenan como [GitHub Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets).  
