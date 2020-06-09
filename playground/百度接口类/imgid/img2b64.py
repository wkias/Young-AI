import cv2
import base64


class img2b64:

    @staticmethod
    def cv():
        cap = cv2.VideoCapture(0)
        is_success, img = cv2.imencode(".png", cap.read()[1])
        if is_success:
            return img.tobytes()

    @staticmethod
    def file(path):
        with open(path, 'rb') as f:
            return f.read()

    @staticmethod
    def b64(bytes_img):
        return base64.b64encode(bytes_img).decode()

    @classmethod
    def cv2b64(cls):
        return base64.b64encode(cls.cv()).decode()

    @classmethod
    def file2b64(cls, path):
        return base64.b64encode(cls.file(path)).decode()

    @classmethod
    def __call__(cls):
        return cls.cv()


if __name__ == '__main__':
    print(img2b64.cv())
    print(img2b64.file('1.jpg'))
