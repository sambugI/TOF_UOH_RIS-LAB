import os
import cv2 as cv
import numpy as np
import json
import time
from arena_api.enums import PixelFormat
from arena_api.system import system
from arena_api.buffer import BufferFactory
from arena_api.__future__.save import Writer

def read_camera_parameters(filepath):
    """Lee los parámetros intrínsecos de la cámara desde un archivo JSON."""
    with open(filepath, "r") as file:
        data = json.load(file)

    cmtx = np.array(data["cameramatrix"]).reshape((3, 3))
    correction_factor = 52 / 50  # Ajuste de escala correcto
    cmtx /= correction_factor  
    dist = np.array(data["distcoeffs"]).reshape((-1, 1))

    return cmtx, dist

TAB1 = "  "
pixel_format = PixelFormat.BGR8

def create_device_with_tries():
    tries = 0
    tries_max = 6
    sleep_time_secs = 10

    while tries < tries_max:
        devices = system.create_device()
        if devices:
            return devices
        print(f'{TAB1}Try {tries+1} of {tries_max}: waiting {sleep_time_secs} secs')
        time.sleep(sleep_time_secs)
        tries += 1

    raise Exception(f'{TAB1}No device found! Please connect a device.')

def detect_aruco_dictionary(image):
    possible_dictionaries = [
        cv.aruco.DICT_4X4_50, cv.aruco.DICT_4X4_100, cv.aruco.DICT_4X4_250, cv.aruco.DICT_4X4_1000,
        cv.aruco.DICT_5X5_50, cv.aruco.DICT_5X5_100, cv.aruco.DICT_5X5_250, cv.aruco.DICT_5X5_1000,
        cv.aruco.DICT_6X6_50, cv.aruco.DICT_6X6_100, cv.aruco.DICT_6X6_250, cv.aruco.DICT_6X6_1000,
        cv.aruco.DICT_7X7_50, cv.aruco.DICT_7X7_100, cv.aruco.DICT_7X7_250, cv.aruco.DICT_7X7_1000,
        cv.aruco.DICT_ARUCO_ORIGINAL
    ]
    
    for dictionary_id in possible_dictionaries:
        aruco_dict = cv.aruco.getPredefinedDictionary(dictionary_id)
        parameters = cv.aruco.DetectorParameters()
        detector = cv.aruco.ArucoDetector(aruco_dict, parameters)
        if len(image.shape) == 3 and image.shape[2] == 3:
            gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        else:
            gray = image
        corners, ids, _ = detector.detectMarkers(image)

        if ids is not None:
            print(f"Diccionario detectado: {dictionary_id}")
            return aruco_dict  

    print("No se detectó un diccionario válido.")
    return None


def estimate_pose_markers(corners, marker_size, cmtx, dist):
    """
    Calcula la rotación (rvecs) y la traslación (tvecs) de cada marcador detectado.

    corners: Esquinas detectadas de cada marcador.
    marker_size: Tamaño real del marcador (en mm o la unidad que coincida con cmtx).
    cmtx: Matriz intrínseca de la cámara.
    dist: Coeficientes de distorsión de la cámara.

    Retorna:
    - Lista de rvecs (vectores de rotación)
    - Lista de tvecs (vectores de traslación)
    """
    marker_points = np.array([
        [-marker_size / 2, marker_size / 2, 0],  # Esquina superior izquierda
        [marker_size / 2, marker_size / 2, 0],   # Esquina superior derecha
        [marker_size / 2, -marker_size / 2, 0],  # Esquina inferior derecha
        [-marker_size / 2, -marker_size / 2, 0]  # Esquina inferior izquierda
    ], dtype=np.float32)

    rvecs = []
    tvecs = []

    for c in corners:
        success, rvec, tvec = cv.solvePnP(marker_points, c, cmtx, dist, flags=cv.SOLVEPNP_IPPE_SQUARE)
        if success:
            rvecs.append(rvec)
            tvecs.append(tvec)

    return rvecs, tvecs

def detect_aruco_pose(image, cmtx, dist, marker_size=50):  # En mm si cmtx está en mm
    aruco_dict = detect_aruco_dictionary(image)

    if aruco_dict is None:
        print("No se pudo detectar el diccionario, saliendo.")
        return None, None

    parameters = cv.aruco.DetectorParameters()
    detector = cv.aruco.ArucoDetector(aruco_dict, parameters)
    corners, ids, _ = detector.detectMarkers(image)

    if ids is not None:
        # ⚠️ CAMBIO AQUÍ: Usamos el detector para calcular la pose
        rvecs, tvecs = estimate_pose_markers(corners, marker_size, cmtx, dist)

        cv.aruco.drawDetectedMarkers(image, corners)
        cv.drawFrameAxes(image, cmtx, dist, rvecs[0], tvecs[0], marker_size / 2)  

        rmat, _ = cv.Rodrigues(rvecs[0])

        print(f"ID: {ids[0][0]}")
        print(f"Posición (tvec): {tvecs[0].flatten()}")
        print(f"Rotación (rmat): \n{rmat}\n")

        return rmat, tvecs[0]

    print("No se detectaron ArUcos.")
    return None, None

def save_camera_pose(rmat, tvec, output_dir):
    pose_data = {
        "rotation_matrix": rmat.tolist(),
        "translation_vector": tvec.tolist(),
    }
    output_path = os.path.join(output_dir, "qr_pose.json")

    with open(output_path, "w") as file:
        json.dump(pose_data, file, indent=4)

    print(f"Posición de la cámara guardada en: {output_path}")

def save(buffer, save_dir):
    converted = BufferFactory.convert(buffer, pixel_format)
    writer = Writer.from_buffer(converted)
    writer.pattern = os.path.join(save_dir, "image_<count>.png")
    writer.save(converted)
    BufferFactory.destroy(converted)
    return writer.saved_images[-1]

def example_entry_point(filepath):
    devices = create_device_with_tries()
    device = system.select_device(devices)
    
    device.start_stream()
    buffer = device.get_buffer()
    save_image_path = save(buffer, filepath)
    device.requeue_buffer(buffer)
    device.stop_stream()
    system.destroy_device()

    return save_image_path

if __name__ == "__main__":
    try:
        save_dir = input("Introduce el directorio donde guardar los resultados: ")
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        save_image_path = example_entry_point(save_dir)
        params_path = "C:\\ProgramData\\Lucid Vision Labs\\ArenaView\\243800650.json"
        cmtx, dist = read_camera_parameters(params_path)
        image = cv.imread(save_image_path)
        corrected_image = cv.undistort (image, cmtx, dist)
        if image is None:
            print("Error: No se pudo cargar la imagen.")
            exit()
        size = float(input("El tamaño (largo o ancho) del aruco marker es: "))
        rmat, tvec = detect_aruco_pose(image, cmtx, dist, size)

        if rmat is not None and tvec is not None:
            # Redimensionar la imagen antes de mostrarla (ejemplo: reducir al 50% del tamaño original)
            scale_percent = 50  # Cambia este valor para ajustar el tamaño
            width = int(image.shape[1] * scale_percent / 100)
            height = int(image.shape[0] * scale_percent / 100)
            resized_image = cv.resize(image, (width, height), interpolation=cv.INTER_AREA)
            cv.imshow("ArUco Pose", resized_image)
            cv.waitKey(0)
            cv.destroyAllWindows()
            if input("¿Está bien la imagen? (y/n): ").lower() == "y":
                save_camera_pose(rmat, tvec, save_dir)
                print("Posición del QR calculada y guardada.")
            else:
                print("Imagen incorrecta.")
        else:
            print("No se pudo obtener la pose del ArUco.")

    except Exception as e:
        print(f"Error: {e}")