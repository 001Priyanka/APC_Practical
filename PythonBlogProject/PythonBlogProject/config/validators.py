import os
from django.core.exceptions import ValidationError
from PIL import Image

def validate_avatar_image(image_field):
    """
    Validate author avatar images:
    - Maximum size: 2 MB
    - Allowed extensions: .jpg, .jpeg, .png, .webp
    """
    max_size_mb = 2
    if image_field.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"Profile image size must not exceed {max_size_mb} MB.")

    valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
    ext = os.path.splitext(image_field.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError(f"Unsupported file format '{ext}'. Allowed formats: {', '.join(valid_extensions)}.")

    try:
        image = Image.open(image_field)
        image.verify()
    except Exception:
        raise ValidationError("Uploaded file is not a valid image.")


def validate_cover_image(image_field):
    """
    Validate blog cover images:
    - Maximum size: 5 MB
    - Allowed extensions: .jpg, .jpeg, .png, .webp
    """
    max_size_mb = 5
    if image_field.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"Cover image size must not exceed {max_size_mb} MB.")

    valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
    ext = os.path.splitext(image_field.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError(f"Unsupported file format '{ext}'. Allowed formats: {', '.join(valid_extensions)}.")

    try:
        image = Image.open(image_field)
        image.verify()
    except Exception:
        raise ValidationError("Uploaded file is not a valid image.")
