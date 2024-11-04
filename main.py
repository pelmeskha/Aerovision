import os
import cv2
from tqdm import tqdm
import matplotlib.pyplot as plt

def draw_bounding_boxes(image, annotations):
    # Получаем размеры изображения
    height, width, _ = image.shape

    for annotation in annotations:
        class_id, x_center, y_center, box_width, box_height = annotation
        
        # Преобразуем координаты из относительных в абсолютные
        x_center_abs = int(x_center * width)
        y_center_abs = int(y_center * height)
        box_width_abs = int(box_width * width)
        box_height_abs = int(box_height * height)

        # Определяем координаты верхнего левого и нижнего правого углов
        x1 = int(x_center_abs - box_width_abs / 2)
        y1 = int(y_center_abs - box_height_abs / 2)
        x2 = int(x_center_abs + box_width_abs / 2)
        y2 = int(y_center_abs + box_height_abs / 2)

        # Рисуем прямоугольник на изображении
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Добавляем текст с идентификатором класса (опционально)
        cv2.putText(image, str(class_id), (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Используем Matplotlib для отображения изображения в цветах RGB
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.axis('off')  # Отключаем оси
    plt.show()

def load_dataset(dataset_path, max_images=None):
    images_path = os.path.join(dataset_path, 'images/01')
    labels_path = os.path.join(dataset_path, 'labels/01')

    dataset = []

    # Используем tqdm для создания прогресс-бара
    image_files = os.listdir(images_path)
    
    # Если max_images задан, ограничиваем количество файлов
    if max_images is not None:
        image_files = image_files[:max_images]

    for image_file in tqdm(image_files, desc="Loading dataset", unit="file"):
        # Предполагаем, что имена файлов изображений и меток совпадают, за исключением расширения
        image_id = os.path.splitext(image_file)[0]
        image_path = os.path.join(images_path, image_file)
        label_file = f"{image_id}.txt"
        label_path = os.path.join(labels_path, label_file)

        # Считываем изображение
        image = cv2.imread(image_path)
        if image is None:
            print(f"Не удалось загрузить изображение: {image_path}")
            continue

        # Считываем аннотации
        annotations = []
        if os.path.exists(label_path):
            with open(label_path, 'r') as file:
                for line in file.readlines():
                    parts = line.strip().split()
                    if len(parts) == 5:
                        class_id = int(parts[0])
                        x_center = float(parts[1])
                        y_center = float(parts[2])
                        width = float(parts[3])
                        height = float(parts[4])
                        annotations.append((class_id, x_center, y_center, width, height))
        
        dataset.append((image, annotations))

    return dataset

# Использование функции
dataset_path = 'dataset'
max_images_to_load = 100  # Задайте желаемое количество изображений
dataset = load_dataset(dataset_path, max_images=max_images_to_load)

# Пример обработки первого изображения и его аннотаций
if dataset:
    image, annotations = dataset[0]
    print("Количество аннотаций:", len(annotations))
    for annotation in annotations:
        print("Аннотация:", annotation)

    # Пример использования функции для первого изображения из датасета
    image, annotations = dataset[0]
    draw_bounding_boxes(image, annotations)
