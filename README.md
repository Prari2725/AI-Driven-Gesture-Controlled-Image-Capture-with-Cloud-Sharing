# Automatic Selfie

This project uses OpenCV, Google Drive API, and QR code generation to capture and upload images to Google Drive.

## Getting Started

### Prerequisites

- Python 3.x
- Virtualenv (optional)

### Installation

1. Clone the repository:

``` bash
git clone https://github.com/your-username/your-repo.git
```

2. Create and activate a virtual environment (optional):

``` bash
cd your-repo 

python -m  venv .venv

source .venv/bin/activate
```
3. Install the requirements:

``` bash
pip install -r requirements.txt
```

4. Set up the Google Drive API:
- Go to the [Google Cloud Console](https://console.cloud.google.com/) and create a new project.
- Enable the Google Drive API for your project.
- Create a service account and download the JSON key file.
- Place the JSON key file in the root directory of your project and rename it to `service_account.json`.

5. Run the main script:

```bash 
python main.py
```

## Usage

1. show your fingers to start capture Timer on the camera frame to capture and upload images.

2. The captured images will be uploaded to the specified Google Drive folder.

3. A QR code will be generated for each uploaded image.

4. The QR code images will be displayed in a side by side with caputure Window.

5. To exit the program, press 'q' on the keyboard.

## License

This project is licensed under the [MIT License](LICENSE).