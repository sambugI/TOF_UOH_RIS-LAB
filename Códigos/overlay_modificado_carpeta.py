import os
import json
import numpy as np
import cv2
import open3d as o3d

def load_calibration_data(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    camera_matrix = np.array(data["cameramatrix"]).reshape(3, 3)
    dist_coeffs = np.array(data["distcoeffs"])
    rotation_vector = np.array([float(x) for x in data["rotation"]]).reshape(3, 1)
    translation_vector = np.array([float(x) for x in data["translation"]]).reshape(3, 1)
    
    return camera_matrix, dist_coeffs, rotation_vector, translation_vector

def project_rgb_on_tof(rgb_path, tof_path, json_path):
    output_dir = os.path.dirname(rgb_path)
    
    # Verificar si la imagen existe
    if not os.path.exists(rgb_path):
        print(f"Error: La imagen {rgb_path} no se encontró.")
        return
    
    # Cargar imagen RGB y verificar que se haya leído correctamente
    image_rgb = cv2.imread(rgb_path, cv2.IMREAD_UNCHANGED)
    if image_rgb is None:
        print(f"Error: No se pudo cargar la imagen {rgb_path}. Verifique la ruta y el formato del archivo.")
        return
    
    # Convertir de BGR a RGB8
    image_rgb = cv2.cvtColor(image_rgb, cv2.COLOR_BGR2RGB)
    
    # Asegurar formato RGB8
    if image_rgb.dtype != np.uint8:
        image_rgb = image_rgb.astype(np.uint8)
    
    # Cargar nube de puntos ToF
    if not os.path.exists(tof_path):
        print(f"Error: El archivo PLY {tof_path} no se encontró.")
        return
    
    pcd = o3d.io.read_point_cloud(tof_path)
    points = np.asarray(pcd.points)
    
    # Cargar parámetros de calibración
    if not os.path.exists(json_path):
        print(f"Error: El archivo JSON {json_path} no se encontró.")
        return
    
    camera_matrix, dist_coeffs, rotation_vector, translation_vector = load_calibration_data(json_path)
    
    # Proyectar puntos 3D a 2D en la imagen RGB
    points_2d, _ = cv2.projectPoints(points, rotation_vector, translation_vector, camera_matrix, dist_coeffs)
    
    colors = np.zeros((len(points), 3))
    height, width, _ = image_rgb.shape
    
    for i, (x, y) in enumerate(points_2d.reshape(-1, 2)):
        x, y = int(round(x)), int(round(y))
        if 0 <= x < width and 0 <= y < height:
            colors[i] = image_rgb[y, x] / 255.0
    
    # Asignar colores a la nube de puntos
    pcd.colors = o3d.utility.Vector3dVector(colors)
    
    # Guardar resultado
    output_ply = os.path.join(output_dir, "output_projected.ply")
    o3d.io.write_point_cloud(output_ply, pcd)
    print(f"Archivo guardado en: {output_ply}")

if __name__ == "__main__":
    rgb_path = input("Ingrese la ruta del archivo JPG: ").strip('"')
    tof_path = input("Ingrese la ruta del archivo PLY: ").strip('"')
    json_path = r"C:\\ProgramData\\Lucid Vision Labs\\ArenaView\\243900238.json"
    
    project_rgb_on_tof(rgb_path, tof_path, json_path)
