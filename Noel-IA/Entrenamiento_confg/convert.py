import os
import json
import cv2
import tensorflow as tf
from object_detection.utils import dataset_util


def create_tf_example(json_file, image_dir):
    with open(json_file, 'r') as f:
        data = json.load(f)

    image_path = os.path.join(image_dir, data['imagePath'])
    img = cv2.imread(image_path)
    height, width, _ = img.shape

    with open(image_path, 'rb') as f:
        encoded_image_data = f.read()

    filename = data['imagePath'].encode('utf8')
    image_format = b'jpeg'

    xmins, xmaxs, ymins, ymaxs = [], [], [], []
    classes_text, classes = [], []

    for shape in data['shapes']:
        if shape['shape_type'] == 'circle':
            x1, y1 = shape['points'][0]
            x2, y2 = shape['points'][1]
            x_center, y_center = (x1 + x2) / 2, (y1 + y2) / 2
            radius = abs(x2 - x1) / 2
            x_min, x_max = x_center - radius, x_center + radius
            y_min, y_max = y_center - radius, y_center + radius
        elif shape['shape_type'] == 'polygon':
            x_coords, y_coords = zip(*shape['points'])
            x_min, x_max = min(x_coords), max(x_coords)
            y_min, y_max = min(y_coords), max(y_coords)

        label = shape['label']
        if label == 'Cell':
            class_id = 1
        elif label == 'Cell inside':
            class_id = 2
        elif label == 'Aspirated Cell':
            class_id = 3

        xmins.append(x_min / width)
        xmaxs.append(x_max / width)
        ymins.append(y_min / height)
        ymaxs.append(y_max / height)
        classes_text.append(label.encode('utf8'))
        classes.append(class_id)

    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/filename': dataset_util.bytes_feature(filename),
        'image/source_id': dataset_util.bytes_feature(filename),
        'image/encoded': dataset_util.bytes_feature(encoded_image_data),
        'image/format': dataset_util.bytes_feature(image_format),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
        'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
        'image/object/class/label': dataset_util.int64_list_feature(classes),
    }))
    return tf_example


def main():
    json_dir = 'entrenamiento'
    image_dir = 'entrenamiento'
    output_file = 'entrenamiento.record'

    writer = tf.io.TFRecordWriter(output_file)
    for root, _, files in os.walk(json_dir):
        for file in files:
            if file.endswith('.json'):
                json_file = os.path.join(root, file)
                tf_example = create_tf_example(json_file, image_dir)
                writer.write(tf_example.SerializeToString())
    writer.close()


if __name__ == '__main__':
    main()

