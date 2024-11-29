import qrcode
import cv2

class QRCodeGenerator:
    def __init__(self, version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4):
        """
        Initializes a new instance of the QRCodeGenerator class.

        Parameters:
            version (int): The version of the QR code to generate. Default is 1.
            error_correction (int): The error correction level of the QR code. Default is qrcode.constants.ERROR_CORRECT_L.
            box_size (int): The size of each box in the QR code. Default is 10.
            border (int): The size of the border around the QR code. Default is 4.

        Returns:
            None
        """
        self.version = version
        self.error_correction = error_correction
        self.box_size = box_size
        self.border = border

    def generate_qr_code(self, content):
        """
        Generates a QR code image based on the provided content.

        Parameters:
            content (str): The content to be encoded in the QR code.

        Returns:
            PIL.Image.Image: The generated QR code image.
        """

        qr = qrcode.QRCode(
            version=self.version,
            error_correction=self.error_correction,
            box_size=self.box_size,
            border=self.border,
        )
        qr.add_data(content)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        return img
    
    
if __name__ == "__main__":
    import numpy as np
    from PIL import Image
    import cv2
    qrcode_generator = QRCodeGenerator()
    qr_img = qrcode_generator.generate_qr_code("https://www.google.com/")
    qr_img = qr_img.convert('RGB')  # Convert to RGB format
    qr_img = cv2.cvtColor(np.array(qr_img), cv2.COLOR_RGB2BGR)  # Convert to BGR format
    cv2.setWindowProperty("QR Code", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.mamesWindow("QR Code", cv2.WINDOW_FULLSCREEN)
    cv2.imshow("QR Code", qr_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

