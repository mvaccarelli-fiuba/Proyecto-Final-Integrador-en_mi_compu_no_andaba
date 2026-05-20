import glob
import os

from werkzeug.utils import secure_filename

from config import PLATOS_IMAGES_DIR, PLATOS_IMAGES_URL_PREFIX
from src.platos import repository

ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}


def get_platos():
    return repository.get_all_platos()


def get_plato(id):
    return repository.get_plato(id)


def get_platos_con_restriccion(restriccion):
    return repository.get_platos_con_restriccion(restriccion)


def create_plato(plato_data):
    return repository.create_plato(plato_data)


def update_plato(id, plato_data):
    return repository.update_plato(id, plato_data)


def delete_plato(id):
    return repository.delete_plato(id)


def _allowed_image(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS
    )


def upload_plato_imagen(plato_id, file):
    repository.get_plato(plato_id)

    if file is None or not file.filename:
        raise ValueError("No se envió ninguna imagen")

    filename = secure_filename(file.filename)
    if not _allowed_image(filename):
        raise ValueError(
            "Formato de imagen no permitido. Use png, jpg, jpeg, gif o webp"
        )

    ext = filename.rsplit(".", 1)[1].lower()
    if ext == "jpeg":
        ext = "jpg"

    os.makedirs(PLATOS_IMAGES_DIR, exist_ok=True)

    for old_file in glob.glob(os.path.join(PLATOS_IMAGES_DIR, f"{plato_id}.*")):
        os.remove(old_file)

    stored_name = f"{plato_id}.{ext}"
    file.save(os.path.join(PLATOS_IMAGES_DIR, stored_name))

    imagen_url = f"{PLATOS_IMAGES_URL_PREFIX}/{stored_name}"
    return repository.update_plato_imagen(plato_id, imagen_url)
