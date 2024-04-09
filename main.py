import pandas as pd
import re

archivo_excel = "Sindicato_encuestav2.xlsx"
datos = pd.read_excel(archivo_excel)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Pregunta 1. Priorizar categorias

# 1.1 Definir las categorías con sus respectivas columnas
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

# 1.2 Calcular el promedio de cada categoría
promedios_categorias = {}
for categoria, columna in categorias.items():
    promedios_categorias[categoria] = datos[columna].mean()

# 1.3 Ordenar las categorías por prioridad descendente
categorias_ordenadas = sorted(promedios_categorias.items(), key=lambda x: x[1], reverse=True)

# 1.4 Mostrar el resultado
print("Priorización de categorias (ordenadas por prioridad descendente):")
for categoria, promedio in categorias_ordenadas:
    print(f"---{categoria}: {promedio}")


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Pregunta 2: Cuanto considera para aumento movilizacion 

datos_movilizacion = datos.copy()

# 2.1 Función para limpiar los datos de aumento de movilización
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

# 2.2 Limpiar columna 
datos_movilizacion['2.1 Aumento Movilización'] = datos_movilizacion['2.1 Aumento Movilización'].apply(limpiar_aumento_movilizacion)
datos_movilizacion = datos_movilizacion[datos_movilizacion['2.1 Aumento Movilización'] > 1000]

# 2.3 Eliminar filas con valores nulos 
datos_movilizacion = datos_movilizacion.dropna(subset=['2.1 Aumento Movilización'])

# 2.4 Guardar los datos limpios en un nuevo archivo Excel
archivo_excel_limpios = "Aumento_movilizacion_limpios.xlsx"
datos_movilizacion.to_excel(archivo_excel_limpios, index=False)

# 2.5 Cargar el archivo Excel limpio
datos_movilizacion_limpios = pd.read_excel(archivo_excel_limpios)

# 2.6 Calcular el promedio de la columna '2.1 Aumento Movilización'
promedio_aumento_movilizacion = datos_movilizacion_limpios['2.1 Aumento Movilización'].mean()
print("\nEl monto de aumento de movilización a considerar es:", promedio_aumento_movilizacion)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Pregunta 3: Cuanto considera para el aumento sueldo base

datos_aumento_sueldo = datos.copy()

# 3.1 Funcion para limpiar columna "Aumento sueldo base" 
def limpiar_aumento_sueldo_base(valor):
    if isinstance(valor, str):
        # Eliminar caracteres no numéricos
        valor = re.sub(r'[^\d]', '', valor)
        if valor.isdigit():
            # Convertir a entero
            valor = int(valor)
            return valor
    elif isinstance(valor, (int, float)):
        # Si el valor ya es un número, dejarlo como está
        if 1 < valor <= 100:
            valor /= 100
            return valor
        return valor
    else:
        return None

# 3.2 Limpiar columna (como estamos trabajando con porcentajes, hay que filtrar los valores menores/iguales a 1 ej: 10% es 0,10 y 100% es 1)
datos_aumento_sueldo['1.3 Aumento Sueldo Base'] = datos_aumento_sueldo['1.3 Aumento Sueldo Base'].apply(limpiar_aumento_sueldo_base)
datos_aumento_sueldo = datos_aumento_sueldo[datos_aumento_sueldo['1.3 Aumento Sueldo Base'] <= 1]
datos_aumento_sueldo = datos_aumento_sueldo.dropna(subset=['1.3 Aumento Sueldo Base'])

# 3.3 Limpiar sueldos bases (para asi poder calcular el promedio de sueldo base)
datos_sueldos_limpios = datos_aumento_sueldo

# 3.4 Funcion para limpiar sueldos bases
def limpiar_sueldo_base(valor):
    if isinstance(valor, str):
        # Eliminar palabras y caracteres no numéricos excepto '.', '-' y '$'
        valor = re.sub(r'[^\d.\-$]', '', valor)
        # Eliminar los puntos, comas, $ y -
        valor = re.sub(r'[.,$\-$]', '', valor)
        # Verificar si el valor contiene solo dígitos después de la limpieza
        if valor.isdigit():
            return int(valor)
    elif isinstance(valor, (int, float)):
        # Si el valor ya es un número, dejarlo como está
        return int(valor)
    else:
        return None

# 3.5 Limpiar sueldos bases
datos_sueldos_limpios['1.2 Tu  sueldo base actualmente es...'] = datos_sueldos_limpios['1.2 Tu  sueldo base actualmente es...'].apply(limpiar_sueldo_base)

# 3.6 Eliminar filas con valores nulos, tambien se filtra por los menores a 50 millones ya que habian outliers que impedian sacar una media representativa de los sueldos
datos_sueldos_limpios = datos_sueldos_limpios.dropna(subset=['1.2 Tu  sueldo base actualmente es...'])
datos_sueldos_limpios = datos_sueldos_limpios[datos_sueldos_limpios['1.2 Tu  sueldo base actualmente es...'] < 50000000]

# 3.7 Guardar los sueldos bases y los aumentos limpios en un nuevo archivo Excel
archivo_sueldos_limpios = "Sueldos_Bases_Limpios.xlsx"
datos_sueldos_limpios.to_excel(archivo_sueldos_limpios, index=False)

# 3.8 Calcular promedios de sueldo base y aumento de sueldo base
promedio_sueldo_base = datos_sueldos_limpios['1.2 Tu  sueldo base actualmente es...'].mean()
promedio_aumento_sueldo_base = datos_sueldos_limpios['1.3 Aumento Sueldo Base'].mean()


# 3.9 Calcular promedio de aumento de sueldo base nuevo, multiplicando el sueldo base promedio por el aumento de sueldo base promedio
aumento_sueldo_total = promedio_aumento_sueldo_base * promedio_sueldo_base
print(f"\nEl monto de aumento sueldo base a considerar es: ", aumento_sueldo_total)


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Pregunta 4: Identifique montos para: • Aguinaldo • Colación • Bono Vacaciones


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Pregunta 5:En general, ¿existen diferencias en las respuestas en base a laregión en la que reside la persona?


