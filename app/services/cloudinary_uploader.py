import cloudinary
import cloudinary.uploader
import os

# Set these in your environment variables
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

def upload_image_to_cloudinary(image_file):
    result = cloudinary.uploader.upload(image_file.file)
    return result['secure_url']
