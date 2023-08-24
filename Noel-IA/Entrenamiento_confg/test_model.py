import tensorflow as tf
import cv2
import numpy as np
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils

# Rutas a los archivos necesarios
PATH_TO_SAVED_MODEL = "exported_model/saved_model"
PATH_TO_LABEL_MAP = "label_map.pbtxt"
IMAGE_PATH = "image.jpeg"

# Cargar el modelo entrenado
model = tf.saved_model.load(PATH_TO_SAVED_MODEL)

# Cargar el mapa de etiquetas
category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABEL_MAP, use_display_name=True)

# Cargar y preprocesar la imagen
image_np = cv2.imread(IMAGE_PATH)
image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)

# Redimensionar la imagen
input_size = (1024, 768)  # Cambie esto a la resolución esperada por su modelo
image_np_resized = cv2.resize(image_np, input_size)

input_tensor = tf.convert_to_tensor(image_np)
input_tensor = input_tensor[tf.newaxis, ...]

# Realizar inferencia
detections = model(input_tensor)

# Visualizar los resultados
num_detections = int(detections.pop('num_detections'))
detections = {key: value[0, :num_detections].numpy() for key, value in detections.items()}
detections['num_detections'] = num_detections
detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

label_id_offset = 0
image_np_with_detections = image_np.copy()
viz_utils.visualize_boxes_and_labels_on_image_array(
    image_np_with_detections,
    detections['detection_boxes'],
    detections['detection_classes'] + label_id_offset,
    detections['detection_scores'],
    category_index,
    use_normalized_coordinates=True,
    max_boxes_to_draw=200,
    min_score_thresh=.80,
    agnostic_mode=False
)

# Guardar la imagen con cuadros delimitadores
output_image_path = "output_image.jpg"
cv2.imwrite(output_image_path, cv2.cvtColor(image_np_with_detections, cv2.COLOR_RGB2BGR))
