import pandas as pd
import re

archivo_excel = "Sindicato_encuestav2.xlsx"
datos = pd.read_excel(archivo_excel)

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
print("Priorización de aspectos relevantes (ordenadas por prioridad descendente):")
for categoria, promedio in categorias_ordenadas:
    print(f"---{categoria}: {promedio}")


"""
# Definir una función para limpiar la columna 'Aumento Movilización'
def limpiar_aumento_movilizacion(valor):

    # Eliminar texto no numérico
    valor_limpio = re.sub(r'[^\d.,]+', '', valor)
    # Eliminar punto si no es parte de un número decimal
    valor_limpio = re.sub(r'\.(?![\d]*\.)', '', valor_limpio)
    # Eliminar coma si no es parte de un número decimal
    valor_limpio = re.sub(r',(?![\d]*,)', '', valor_limpio)
    # Eliminar punto final si no es parte de un número decimal
    valor_limpio = re.sub(r'\.$', '', valor_limpio)
    # Eliminar el signo de dólar
    valor_limpio = re.sub(r'\$', '', valor_limpio)
    # Convertir a float si es un número válido
    try:
        return float(valor_limpio)
    except ValueError:
        return None

# Eliminar las filas que contienen porcentajes en la columna 'Aumento Movilización'
datos = datos[~datos['2.1 Aumento Movilización'].astype(str).str.contains('%')]

# Aplicar la función de limpieza a la columna 'Aumento Movilización' sin porcentajes
datos['Aumento Movilización Limpio'] = datos['2.1 Aumento Movilización'].apply(limpiar_aumento_movilizacion)

# Guardar los datos limpios en un nuevo archivo Excel
datos.to_excel("sindicato_limpios.xlsx", index=False)

# Mostrar los datos después de la limpieza
print(datos['Aumento Movilización Limpio'])
"""