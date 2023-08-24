from matplotlib import parse_version
import tensorflow as tf
from skimage.measure import regionprops
import matplotlib.pyplot as plt
import cv2
import numpy as np
import os
import glob
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from PIL import Image
import imageio
from tqdm import tqdm
import pandas as pd
from scipy.optimize import curve_fit
from scipy.signal import medfilt
from scipy.interpolate import interp1d
from pykalman import KalmanFilter
import gc

# Rutas a los archivos necesarios
PATH_TO_SAVED_MODEL = "workspace_4/exported_model/saved_model"
PATH_TO_LABEL_MAP = "workspace_4/label_map.pbtxt"

# Cargar el modelo entrenado
model = tf.saved_model.load(PATH_TO_SAVED_MODEL)

# Cargar el mapa de etiquetas
category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABEL_MAP, use_display_name=True)

# Funciones para ajustar

def theret(x,e):
    return (3*2.1)/(2*np.pi)*(1/e)*x

def plaza(x,dia,Rp,e):
    b1 = np.single(2.0142)
    b3 = np.single(2.1187)
    R0 = dia/2
    return (1/(b1*(1-(Rp/R0)**b3)))*(3/e)*x


# Función para convertir pixeles a micras
def pixel_to_micron(value):
    # 1 micra es igual a 6 pixeles
    return value / 6.0

# Función para calcular el diámetro medio de la célula aspirada
def measure_aspirated_cell_diameter(box, image_shape):
    # Conversión de las coordenadas del cuadro delimitador a pixeles
    ymin, xmin, ymax, xmax = [int(coord) for coord in (box[0]*image_shape[0], box[1]*image_shape[1], box[2]*image_shape[0], box[3]*image_shape[1])]
    
    # Calcular el ancho y la altura en pixeles
    width_pixels = xmax - xmin
    height_pixels = ymax - ymin
    
    # Convertir a micras
    width_microns = pixel_to_micron(width_pixels)
    height_microns = pixel_to_micron(height_pixels)
    
    # Calcular y devolver el diámetro medio en micras
    return (width_microns + height_microns) / 2.0

# Función para crear el directorio de resultados si no existe
def create_results_directory(input_folder):
    results_dir = os.path.join(os.path.dirname(input_folder), 'Resultados')
    #if not os.path.exists(results_dir):
    #    os.mkdir(results_dir)
    return results_dir

def read_data_file(start_path):
    # Definir el nombre del archivo a buscar
    filename = 'Data.txt'
    
    # Inicializar la ruta del archivo de datos
    data_file_path = None
    
    # Buscar el archivo de datos hasta 5 niveles hacia arriba
    for _ in range(5):
        start_path = os.path.abspath(os.path.join(start_path, '..'))  # Subir un nivel
        potential_path = os.path.join(start_path, filename)
        
        # Comprobar si el archivo de datos existe en este nivel
        if os.path.exists(potential_path):
            data_file_path = potential_path
            break
    
    # Si el archivo de datos no se encuentra, lanzar un error
    if data_file_path is None:
        raise FileNotFoundError(f"No se encontró el archivo '{filename}' en los 5 niveles superiores.")
    
    # Lee el archivo 'Data.txt' encontrado con numpy
    data_array = np.genfromtxt(data_file_path, delimiter='\t', skip_header=2, dtype=str)
    
    # Crea un DataFrame a partir de los datos importados
    data_df = pd.DataFrame(data_array)
    
    # Asigna nombres a las columnas del DataFrame
    data_df.columns = ['Control', 'Time [s]', 'Position [mm]', 'Pressure [Pa]', 'Image Ref.']
    
    # Realiza las transformaciones necesarias
    data_df['Image Ref.'] = data_df['Image Ref.'].str[1:]  # Elimina el primer carácter "\"
    data_df['Position [mm]'] = pd.to_numeric(data_df['Position [mm]'])  # Convierte los datos de posición a número
    data_df['Pressure [Pa]'] = data_df['Position [mm]'] * 9.81 # Convierte los datos de posición a presión
    #print(data_df['Pressure [Pa]'])
    return data_df


def load_and_infer(image):
    # Comprueba si la entrada es una cadena, en ese caso, se considera que es una ruta de archivo
    if isinstance(image, str):
        image_np = cv2.imread(image)
        image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
    else:
        image_np = image

    input_tensor = tf.convert_to_tensor(image_np)
    input_tensor = input_tensor[tf.newaxis, ...]
    detections = model(input_tensor)
    num_detections = int(detections.pop('num_detections'))
    detections = {key: value[0, :num_detections].numpy() for key, value in detections.items()}
    detections['num_detections'] = num_detections
    detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

    return image_np, detections


def process_images(input_folder, output_folder):

    print("Procesando experimento "+input_folder)

    try:
      # Crea el directorio de resultados
      results_dir = create_results_directory(input_folder)
      #output_folder = os.path.join(results_dir, input_folder)

      image_files = glob.glob(os.path.join(input_folder, "*.jpeg"))
      image_files = sorted(image_files)
      writer = imageio.get_writer(os.path.join(output_folder, 'video.mp4'), fps=5)
      writer_c = imageio.get_writer(os.path.join(output_folder, 'cropped', 'video.mp4'), fps=5)
      
      # Lista para almacenar imágenes recortadas para calcular el ángulo promedio
      cropped_images = []
      first_crop_dims = None

      SCALE_BAR_TEXT = "50 um" 
      SCALE_BAR_PIXELS = 300
      
      for image_file in tqdm(image_files, desc="Processing images"):
          image_np, detections = load_and_infer(image_file)
          image_np_with_detections = image_np.copy()

          viz_utils.visualize_boxes_and_labels_on_image_array(
              image_np_with_detections,
              detections['detection_boxes'],
              detections['detection_classes'],
              detections['detection_scores'],
              category_index,
              use_normalized_coordinates=True,
              max_boxes_to_draw=200,
              min_score_thresh=.80,
              agnostic_mode=False
          )

          # Dibuja la barra de escala y su etiqueta
          SCALE_BAR_TEXT = "50 um" 
          SCALE_BAR_PIXELS = 300
          image_height, image_width = image_np_with_detections.shape[:2]
          cv2.line(image_np_with_detections, (50, image_height - 50), (50 + SCALE_BAR_PIXELS, image_height - 50), (255, 255, 255), 2)
          cv2.putText(image_np_with_detections, SCALE_BAR_TEXT, (50, image_height - 70), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)

          cv2.imwrite(os.path.join(output_folder, os.path.basename(image_file)), cv2.cvtColor(image_np_with_detections, cv2.COLOR_RGB2BGR))
          writer.append_data(cv2.cvtColor(image_np_with_detections, cv2.COLOR_RGB2BGR))

          last_valid_box = None

          if 3 in detections['detection_classes']:  # Class ID for "Aspirated Cell"
              box = detections['detection_boxes'][np.argmax(detections['detection_classes'] == 3)]
              ymin, xmin, ymax, xmax = box
              if first_crop_dims is None:
                  # Recortar la imagen por primera vez y guardar las dimensiones de recorte
                  first_crop_dims = (xmin, xmax, ymin, ymax)
              (left, right, top, bottom) = (first_crop_dims[0] * image_np.shape[1]*0.8, 
                                            first_crop_dims[1] * image_np.shape[1]*1.2,
                                            first_crop_dims[2] * image_np.shape[0]*0.80, 
                                            first_crop_dims[3] * image_np.shape[0]*1.2)
              cropped_img = image_np[int(top):int(bottom), int(left):int(right)]
              cropped_images.append(cropped_img)

      average_angle = find_average_angle(cropped_images)
      stabilized_images = stabilize_images(cropped_images, average_angle)
      left_positions = []  # Lista para guardar las posiciones del borde izquierdo


      previous_boxes = []
      ymin, xmin, ymax, xmax = box
      max_xmin_seen = None

      for i, stabilized_image in tqdm(enumerate(stabilized_images),desc="Processing cropped images"):
                  
          # Hacer una segunda inferencia de la detección de objetos
          image_np, detections = load_and_infer(stabilized_image)
          image_np_with_detections = image_np.copy()
          viz_utils.visualize_boxes_and_labels_on_image_array(
              image_np_with_detections,
              detections['detection_boxes'],
              detections['detection_classes'],
              detections['detection_scores'],
              category_index,
              use_normalized_coordinates=True,
              max_boxes_to_draw=1,
              min_score_thresh=.92,
              agnostic_mode=False
          )

          # Dibuja la barra de escala y su etiqueta
          SCALE_BAR_TEXT = "10 um" 
          SCALE_BAR_PIXELS = 60
          image_height, image_width = image_np_with_detections.shape[:2]
          cv2.line(image_np_with_detections, (50, image_height - 50), (50 + SCALE_BAR_PIXELS, image_height - 50), (255, 255, 255), 2)
          cv2.putText(image_np_with_detections, SCALE_BAR_TEXT, (50, image_height - 70), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
          
          cv2.imwrite(os.path.join(output_folder, 'cropped', os.path.basename(image_files[i])), cv2.cvtColor(image_np_with_detections, cv2.COLOR_RGB2BGR))
          writer_c.append_data(cv2.cvtColor(image_np_with_detections, cv2.COLOR_RGB2BGR))

          # Si la clase "Aspirated Cell" está en las detecciones, guarda la posición del borde izquierdo
          if 3 in detections['detection_classes']:  
              box = detections['detection_boxes'][np.argmax(detections['detection_classes'] == 3)]
              previous_boxes.append(box)

              if max_xmin_seen is None or box[1] < max_xmin_seen:
                  max_xmin_seen = box[1]
                  previous_boxes.append(box)

              if len(previous_boxes) > 3:  # Adjust this value according to your needs
                  previous_boxes.pop(0)  # Remove the oldest box
                  box = np.mean(previous_boxes, axis=0)  # Compute the moving average box

              _, xmin, _, xmax = box
              box_width = xmax - xmin
              box_width_in_pixels = box_width * image_np.shape[1]
              
              if len(stabilized_images) > 250:
                  left_positions.append(pixel_to_micron(box_width_in_pixels))  # Guarda la longitud del lado horizontal de la caja
              else:
                  left_positions.append(pixel_to_micron(xmin * image_np.shape[1]))  # Guarda la posición del borde izquierdo


      writer.close()
      writer_c.close()

      left_positions = np.abs((left_positions-left_positions[0]))

      # Después de que se han procesado las imágenes, lee el archivo de datos
      data_df = read_data_file(input_folder)

      # Aquí se cambió 'Image Ref.' por data_df.columns[4]
      data_df = data_df.set_index(data_df.columns[4])
      data_df = data_df.reindex([os.path.basename(f) for f in image_files])
      data_df.reset_index(inplace=True)

      # Aquí se cambió 'Press' por data_df.columns[3]
      press_values = data_df[data_df.columns[3]]
      press_values = press_values.values*(-10)
      press_values = press_values - press_values[0]
      #print(press_values)


      # Al final de la función 'process_images', calcula y muestra el diámetro de la celda aspirada
      if 3 in detections['detection_classes']:  # Class ID for "Aspirated Cell"
          box = detections['detection_boxes'][np.argmax(detections['detection_classes'] == 3)]
          diameter = measure_aspirated_cell_diameter(box, image_np.shape)
          print(f"El diámetro medio de la célula aspirada es de {diameter} micras.")
      
      # Calcular el número de datos que tienes actualmente
      n_points_current = len(left_positions)

      # Calcular los nuevos índices
      new_indices = np.linspace(0, n_points_current - 1, 300)

      # Crear la función de interpolación para left_positions
      f_left_positions = interp1d(range(n_points_current), left_positions)

      # Interpolar left_positions a los nuevos índices
      left_positions = f_left_positions(new_indices)

      # Haz lo mismo para press_values
      f_press_values = interp1d(range(n_points_current), press_values)
      press_values = f_press_values(new_indices)

      RP = 2.5
      LPRP = left_positions/RP

      # Aplicar el filtro de mediana
      window_size = 3  # Ajusta este valor según tus necesidades
      LPRP_median = medfilt(LPRP, window_size)
      # Inicializar el filtro de Kalman
      kf = KalmanFilter(initial_state_mean=0, n_dim_obs=1)
      # Usar el filtro de Kalman para suavizar los datos
      LPRP_kalman = kf.em(LPRP_median).smooth(LPRP_median)[0]
      press_values_smooth = kf.em(press_values).smooth(press_values)[0]

      # Si el valor de presión es igual a 0 o a 1 entonces LPRP = 0
      press_values_smooth[press_values_smooth <= 1] = 0
      LPRP_kalman[press_values_smooth <= 1] = 0

      # Ahora vamos a eliminar datos atípicos
      # Puedes ajustar estos límites a tus necesidades
      lower_bound = np.percentile(LPRP_kalman, 1)
      upper_bound = np.percentile(LPRP_kalman, 99)
      mask = (LPRP_kalman >= lower_bound) & (LPRP_kalman <= upper_bound)
      LPRP_kalman = LPRP_kalman[mask]
      press_values_smooth = press_values_smooth[mask]

      try:
        # Encuentra el índice en el que LPRP_kalman cae por debajo de 0.1 por primera vez
        indices_below_02 = np.where(LPRP_kalman[:-20] < 0.1)[-1]
        #print(indices_below_02)

        if indices_below_02.size > 0:  # Si existen índices que cumplen la condición
          first_index_below_02 = indices_below_02[-1]  # El último índice donde LPRP_kalman cae por debajo de 0.1

          # Elimina todos los datos desde este índice en adelante
          press_values_smooth_f = press_values_smooth[:first_index_below_02]
          LPRP_kalman_f = LPRP_kalman[:first_index_below_02]

          # Ahora, selecciona los datos en el rango de 0.2 a 0.3 de LPRP
          range_mask = (LPRP_kalman_f >= 0.1) & (LPRP_kalman_f <= 0.3)
          press_values_range = press_values_smooth_f[range_mask]
          LPRP_range = LPRP_kalman_f[range_mask]
        else:
          range_mask = (LPRP_kalman >= 0.1) & (LPRP_kalman <= 0.3)
          press_values_range = press_values_smooth[range_mask]
          LPRP_range = LPRP_kalman[range_mask]

      except:
        pass

      try:
        # Encuentra el índice en el que LPRP_kalman cae por debajo de 0.2 por primera vez
        indices_below_03 = np.where(LPRP_range > 0.3)[0]
        #print(indices_below_02)

        if indices_below_03.size > 0:  # Si existen índices que cumplen la condición
          first_index_below_03 = indices_below_03[0]  # El último índice donde LPRP_kalman cae por debajo de 0.2

          # Elimina todos los datos desde este índice en adelante
          press_values_smooth_f = press_values_smooth_f[first_index_below_03:]
          LPRP_kalman_f = LPRP_kalman_f[first_index_below_03:]

          # Ahora, selecciona los datos en el rango de 0.2 a 0.3 de LPRP
          range_mask = (LPRP_range >= 0.1) & (LPRP_range <= 0.3)
          press_values_range = press_values_range[range_mask]
          LPRP_range = LPRP_range[range_mask]
        else:
          range_mask = (LPRP_kalman >= 0.1) & (LPRP_kalman <= 0.3)
          press_values_range = press_values_smooth[range_mask]
          LPRP_range = LPRP_kalman[range_mask]

      except:
        pass

      # Dibujar el nuevo gráfico
      plt.figure()
      plt.plot(LPRP_kalman, press_values_smooth)
      plt.xlabel('$L_p/R_p$')
      plt.ylabel('$\Delta P$ [Pa]')
      plt.grid(color = 'green', linestyle = '--', linewidth = 0.5)
      plt.savefig(os.path.join(os.path.join(os.path.dirname(input_folder), 'Resultados'), input_folder+'_pressure_vs_LPRP.pdf'))

      print(LPRP_range)
      print(press_values_range)
      # Guardar las posiciones del borde izquierdo y los valores de presión en un archivo txt
      np.savetxt(os.path.join(os.path.join(os.path.dirname(input_folder), 'Resultados'), input_folder+'_output_LPRP_and_pressure.txt'), 
              np.column_stack((LPRP_kalman, press_values_smooth)), 
              fmt='%.4f', header='LP/RP\tPressure[Pa]', comments='')

      # Guardar las posiciones del borde izquierdo y los valores de presión en un archivo txt
      np.savetxt(os.path.join(os.path.join(os.path.dirname(input_folder), 'Resultados'), input_folder+'_output_LPRP_and_pressure_range.txt'), 
              np.column_stack((LPRP_range, press_values_range)), 
              fmt='%.4f', header='LP/RP\tPressure[Pa]', comments='')

      # Ajuste de parámetros mecánicos para los datos en el rango especificado
      popt, pcov = curve_fit(theret, press_values_range, LPRP_range)
      the_e = popt
      plt.plot(theret(press_values_range, *popt), press_values_range, 'r-', label='Theret et al.: $E_{ap}$ = %5.3f' % tuple(popt))

      popt, pcov = curve_fit(lambda x, e: plaza(x,diameter,RP,e), press_values_range, LPRP_range)
      plz_e = popt
      plt.plot(plaza(press_values_range, diameter, RP, popt),press_values_range, 'g--', label='Plaza et al.: $E_{ap}$ = %5.3f' % popt)

      # Guardar el módulo elástico y el diámetro en el archivo txt
      mec_res_path = os.path.join(os.path.dirname(input_folder), 'Mec_res.txt')
      # Verifica si el archivo ya existe
      if not os.path.isfile(mec_res_path):
          # Si el archivo no existe, escribe la cabecera
          with open(mec_res_path, 'w') as f:
              f.write('Test\ttheret\tplaza\tdiameter\n')

      # Abre el archivo en modo append ('a') para agregar nuevas líneas sin borrar las existentes
      with open(mec_res_path, 'a') as f:
          for theret_value, plaza_value in zip(the_e, plz_e):
              f.write(f'{input_folder}\t{theret_value}\t{plaza_value}\t{diameter}\n')

      plt.xlabel('$L_p/R_p$')
      plt.ylabel('$\Delta P$ [Pa]')
      plt.grid(color = 'green', linestyle = '--', linewidth = 0.5)
      plt.legend()
      plt.savefig(os.path.join((os.path.join(os.path.dirname(input_folder), 'Resultados')), input_folder+'_pressure_vs_LPRP_mec.pdf'))

    except:
      pass

    try:
      # Al final de la función, después de haber procesado las imágenes
      del image_files, writer, writer_c, cropped_images, detections
      del image_np, image_np_with_detections, box
      del previous_boxes, left_positions, data_df, press_values
      del LPRP, LPRP_median, LPRP_kalman, press_values_smooth
      del LPRP_range, press_values_range, popt, pcov
      gc.collect()  # Forzar la liberación de memoria
    except:
      pass

def stabilize_images(images, average_angle):
    # Tamaño final deseado de la imagen
    final_width, final_height = 2048, 1536

    # Rotar las imágenes para alinearlas con el eje horizontal
    M_rotate = cv2.getRotationMatrix2D((images[0].shape[1] / 2, images[0].shape[0] / 2), average_angle, 1)
    images = [cv2.warpAffine(image, M_rotate, (image.shape[1], image.shape[0])) for image in images]

    # Convertir las imágenes a escala de grises
    gray_images = [cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) for image in images]

    # Aplicar el filtro de Canny para detectar bordes
    gray_images = [cv2.Canny(gray, 130, 150, apertureSize = 3) for gray in gray_images]

    # Detectar características en la primera imagen
    features = cv2.goodFeaturesToTrack(gray_images[0], maxCorners=300, qualityLevel=0.01, minDistance=5, blockSize=10)

    stabilized_images = [images[0]]
    motion = np.zeros((2,), dtype=np.float32)  # El movimiento acumulado

    top = (final_height - stabilized_images[0].shape[0]) // 2
    bottom = final_height - stabilized_images[0].shape[0] - top
    left = (final_width - stabilized_images[0].shape[1]) // 2
    right = final_width - stabilized_images[0].shape[1] - left
    stabilized_images[0] = cv2.copyMakeBorder(stabilized_images[0], top, bottom, left, right, cv2.BORDER_CONSTANT, value=[0, 0, 0])

    for i in range(1, len(images)):

        # Comprobar que las características son válidas
        if features is not None and len(features) > 0:
            next_features, status, _ = cv2.calcOpticalFlowPyrLK(
                gray_images[i-1], gray_images[i], features, None, winSize=(30,30),
                maxLevel=2, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 20, 0.02))
        
            # Verificar que next_features y status no son None
            if next_features is not None and status is not None:
                # Calcular el movimiento promedio de las características
                valid_points = (status == 1).reshape(-1, 1)
                if valid_points.sum() > 0:
                    motion += np.mean(next_features[valid_points] - features[valid_points], axis=0)

                    # Aplicar la corrección de movimiento a la imagen actual
                    stabilized_image = cv2.warpAffine(images[i], np.array([[1, 0, -motion[0]], [0, 1, -motion[1]]], dtype=np.float32),
                                                    (images[i].shape[1], images[i].shape[0]), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
                    stabilized_image = cv2.copyMakeBorder(stabilized_image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[0, 0, 0])
                    stabilized_images.append(stabilized_image)

                # Actualizar las características
                features = next_features[valid_points.reshape(-1)]

        else:
            # No se pueden seguir las características, usar la imagen tal como está
            stabilized_image = cv2.copyMakeBorder(images[i], top, bottom, left, right, cv2.BORDER_CONSTANT, value=[0, 0, 0])
            stabilized_images.append(stabilized_image)

    return stabilized_images

def find_average_angle(images):
    angles = []
    lengths = []

    for image in images:
        # Convertir la imagen a escala de grises
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        # Aplicar el filtro de Canny para detectar bordes
        edges = cv2.Canny(gray, 100, 150, apertureSize = 3)

        # Dilatación y erosión para cerrar huecos
        dilated_edges = cv2.dilate(edges, None)
        edges = cv2.erode(dilated_edges, None)

        # Aplicar la Transformada de Hough para encontrar líneas segmentadas en la imagen
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=10, maxLineGap=10)
        if lines is None:
            continue

        # Para cada línea detectada, calcular la longitud y el ángulo
        for line in lines:
            for x1, y1, x2, y2 in line:
                length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                angle = np.arctan2(y2 - y1, x2 - x1) * 180.0 / np.pi

                # Agregar la longitud y el ángulo a las listas correspondientes
                lengths.append(length)
                angles.append(angle)

    # Si no se han detectado líneas, devolver 0 grados
    if len(lengths) == 0 or sum(lengths) == 0:
        return 0

    # Calcular el ángulo promedio, ponderado por las longitudes de las líneas
    average_angle = np.average(angles, weights=lengths)

    return average_angle



def main():
    dirs = []

    while True:
        print("Por favor, introduce la ruta del directorio que deseas procesar.")
        print("Si ya has terminado de introducir directorios, escribe 'done'.")
        input_folder = input()

        if input_folder.lower() == 'done':
            break
        elif os.path.isdir(input_folder):
            dirs.append(input_folder)
        else:
            print(f"El directorio {input_folder} no existe. Por favor, introduce un directorio válido.")

    if not dirs:
        print("No se seleccionaron directorios para el procesamiento.")
        return

    for input_folder in dirs:
        output_folder = os.path.join(input_folder, "output")
        os.makedirs(output_folder, exist_ok=True)
        os.makedirs(os.path.join(output_folder, 'cropped'), exist_ok=True)
        process_images(input_folder, output_folder)

if __name__ == "__main__":
    main()