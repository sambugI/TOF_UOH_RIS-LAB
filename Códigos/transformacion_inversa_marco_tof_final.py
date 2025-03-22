# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 19:12:51 2025

@author: samue
"""

""" Este código permite tomar los archivos .json para transformar la información del ArUco Marker respecto a la cámara para ponerla respecto a la cámara ToF en lugar de la cámara RGB y 
luego tomar la inversa. Estas nuevas matrices de traslación y rotación permiten poner las nubes de puntos tomando como sistema de referencia al ArUco marker para tener una mejor alineación
entre las nubes de puntos al introducir estas matrices en Apply transform de CloudCompare. 
Una vez se corre este archivo en la terminal, se debe especificar las direcciones de los archivos .json donde se tiene la información de la cámara respecto al ArUco Marker hasta que se introduzca
en la terminal una dirección no válido de un archivo .json. Luego, se debe ingresar la carpeta donde se quiere guardar el archivo .txt en donde se encuentran las matrices calculadas.
"""

import numpy as np
import cv2
import json
import os

# Vector de rotación y traslación de la segunda cámara respecto a la primera
rotation_vector = np.array([0.037393, 0.029319, -0.005906])
translation_vector = np.array([4.358053, 85.270463, 22.640340])

# Convertir el vector de rotación a matriz de rotación
rotation_matrix, _ = cv2.Rodrigues(rotation_vector)

# Lista vacía de dinosaurios
dinosaurs = []

# Pedir archivos JSON hasta que el usuario ingrese 'y'
while True:
    file_path = input("Ingrese la ruta del archivo JSON o 'y' para continuar: ").strip()
    if file_path.lower() == 'y':
        break
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            if "rotation_matrix" in data and "translation_vector" in data:
                dinosaurs.append({
                    "rotation_matrix": np.array(data["rotation_matrix"]),
                    "translation_vector": np.array(data["translation_vector"])
                })
            else:
                print("Error: El archivo no contiene las claves necesarias.")
    except Exception as e:
        print(f"Error al leer el archivo: {e}")

# Transformar cada dinosaurio a la nueva cámara
transformed_dinosaurs = []
for dino in dinosaurs:
    new_rotation_matrix = rotation_matrix @ dino["rotation_matrix"]
    new_translation_vector = rotation_matrix @ dino["translation_vector"] + translation_vector.reshape(3, 1)
    transformed_dinosaurs.append({
        "rotation_matrix": new_rotation_matrix,
        "translation_vector": new_translation_vector
    })

# Lista para guardar las matrices inversas en formato homogéneo
inverse_transformations = []

for dino in transformed_dinosaurs:
    R = dino["rotation_matrix"]
    t = dino["translation_vector"]

    R_inv = R.T  # Traspuesta de la matriz de rotación
    t_inv = -R_inv @ t  # Traslación invertida

    # Construcción de la matriz homogénea inversa
    inverse_matrix = np.eye(4)  # Matriz identidad 4x4
    inverse_matrix[:3, :3] = R_inv  # Insertar la matriz de rotación inversa
    inverse_matrix[:3, 3] = t_inv.flatten()  # Insertar la traslación inversa

    inverse_transformations.append(inverse_matrix)

# Seleccionar la carpeta de destino
output_folder = input("Ingrese la carpeta donde desea guardar las matrices: ").strip()
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Archivo de salida único
output_file = os.path.join(output_folder, "matrices.txt")
with open(output_file, 'w') as f:
    for i, inv_matrix in enumerate(inverse_transformations):
        f.write(f"Matriz {i+1}:\n")
        for row in inv_matrix:
            f.write(" ".join(f"{val:.8f}" for val in row) + "\n")
        f.write("\n")
print(f"Todas las matrices han sido guardadas en: {output_file}")
