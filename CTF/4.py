#Вращение изображения по координатам из ppc1
import os
from PIL import Image


def transform_image(image_path, output_path, step_size=10, angle_step=90):
    # Создать выходную директорию, если её нет
    os.makedirs(output_path, exist_ok=True)

    # Открываем изображение
    img = Image.open(image_path)
    width, height = img.size

    # Центральная точка изображения
    center_x, center_y = width // 2, height // 2

    # Начальная точка обрезки
    left, top = 0, 0
    right, bottom = width, height

    i = 0
    while right - left > step_size * 2 and bottom - top > step_size * 2:
        # Обрезка изображения
        left += step_size
        top += step_size
        right -= step_size
        bottom -= step_size

        cropped_img = img.crop((left, top, right, bottom))

        # Поворот изображения
        angle = i * angle_step
        rotated_img = cropped_img.rotate(angle, expand=True)

        # Масштабирование обратно к исходному размеру
        # scaled_img = rotated_img.resize((width, height))

        # Сохранение результата промежуточного шага
        rotated_img.save(f"{output_path}/step_{i}.png")

        i += 1


# Пример использования
transform_image("ppc1.png", "output_directory")
