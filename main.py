import pandas as pd
import re

#Abrir excel 
archivo_excel = "Sindicato_encuestav2.xlsx"
datos = pd.read_excel(archivo_excel)


# Pregunta 1. Priorizar categorias

# Definir las categorías con sus respectivas columnas
categorias = {
    "Sueldo Base": "1. Sueldo Base",
    "Movilización": "2. Movilización",
    "Colación": "3. Colación",
    "Aumento Asignación Perdida de Caja (servicio al cliente)": "4. Aumento Asignación Perdida de Caja (servicio al cliente)",
    "Aguinaldo Septiembre": "5. Aguinaldo Septiembre",
    "Aguinaldo Navidad": "6. Aguinaldo Navidad",
    "Regalo Navidad Hijo Trabajadores": "7. Regalo Navidad Hijo Trabajadores",
    "Beneficio Permanencia por años de Servicio": "8. Beneficio Permanencia por años de Servicio",
    "Bono Vacaciones": "9. Bono Vacaciones",
    "Permiso Administrativo": "10. Permiso Administrativo",
    "Préstamo Vacaciones": "11. Préstamo Vacaciones",
    "Pago de los primeros 3 días en licencia médica": "12. Pago de los primeros 3 días en licencia médica (La primera anual)"
}

# Calcular el promedio de cada categoría
promedios_categorias = {}
for categoria, columna in categorias.items():
    promedios_categorias[categoria] = datos[columna].mean()

# Ordenar las categorías por prioridad descendente
categorias_ordenadas = sorted(promedios_categorias.items(), key=lambda x: x[1], reverse=True)

# Mostrar el resultado
print("Priorización de categorias (ordenadas por prioridad descendente):")
for categoria, promedio in categorias_ordenadas:
    print(f"---{categoria}: {promedio}")


#Punto 2: Calcular aumento movilizacion (limpiando datos y calculando promedio de los datos limpios)

# Definir una función para limpiar los datos de aumento de movilización
def limpiar_aumento_movilizacion(valor):
    if isinstance(valor, str):
        # Eliminar puntos, comas y guiones
        valor = re.sub(r'\$', '', valor)
        valor = re.sub(r',', '', valor)
        valor = re.sub(r'-', '', valor)
        valor = re.sub(r'\.', '', valor)
        valor = re.sub(r'[\.,-]', '', valor)
        # Verificar si el valor contiene solo dígitos después de la limpieza
        if valor.isdigit():
            valor = int(valor)
            if valor <= 1000:
                return None
            return valor
        else:
            return None
    return valor

# Aplicar la limpieza a la columna correspondiente
datos['2.1 Aumento Movilización'] = datos['2.1 Aumento Movilización'].apply(limpiar_aumento_movilizacion)
datos = datos[datos['2.1 Aumento Movilización'] > 1000]

# Eliminar filas con valores nulos (es decir, aquellos que no pudieron ser limpiados a un número entero)
datos = datos.dropna(subset=['2.1 Aumento Movilización'])

# Guardar los datos limpios en un nuevo archivo Excel
archivo_excel_limpios = "Aumento_movilizacion_limpios.xlsx"
datos.to_excel(archivo_excel_limpios, index=False)

# Cargar el archivo Excel limpio en un DataFrame
datos_limpios = pd.read_excel(archivo_excel_limpios)

# Calcular el promedio de la columna '2.1 Aumento Movilización'
promedio_aumento_movilizacion = datos_limpios['2.1 Aumento Movilización'].mean()

print("\nEl promedio de aumento de movilización es:", promedio_aumento_movilizacion)

