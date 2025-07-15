import cloudinary
import cloudinary.uploader
import os

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_URL").split("@")[1],
    api_key=os.getenv("CLOUDINARY_URL").split("//")[1].split(":")[0],
    api_secret=os.getenv("CLOUDINARY_URL").split(":")[2].split("@")[0],
)

def upload_image(file_path, folder="products"):
    response = cloudinary.uploader.upload(file_path, folder=folder)
    return response["secure_url"]
