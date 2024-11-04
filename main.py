import os
import cv2

def load_dataset(dataset_path):
    images_path = os.path.join(dataset_path, 'images')
    labels_path = os.path.join(dataset_path, 'labels')

    dataset = []

    for image_file in os.listdir(images_path):
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
dataset = load_dataset(dataset_path)

# Пример обработки первого изображения и его аннотаций
if dataset:
    image, annotations = dataset[0]
    print("Количество аннотаций:", len(annotations))
    for annotation in annotations:
        print("Аннотация:", annotation)