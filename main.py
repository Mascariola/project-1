import cv2
import kivy
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.config import Config

kivy.require('1.11.1')

# Prevent Kivy window from being resized
Config.set('graphics', 'resizable', False)

class MyApp(App):
    def build(self):
        self.state = 'front_page'
        self.main_layout = BoxLayout(orientation='vertical')

        # Front Page Layout
        self.front_page_layout = BoxLayout(orientation='vertical')
        self.front_page_layout.add_widget(Label(text='Object Detector', font_size='40sp'))
        self.front_page_layout.add_widget(Label(text='Final Project', font_size='30sp'))
        self.front_page_layout.add_widget(Label(text='Created by: Perly Mascariola And Christopher Gerongco', font_size='20sp'))
        self.start_button = Button(text='Start', font_size='20sp')
        self.start_button.bind(on_press=self.start_camera)
        self.front_page_layout.add_widget(self.start_button)

        # Add the front page layout to the main layout
        self.main_layout.add_widget(self.front_page_layout)

        # Camera Layout (initially empty)
        self.camera_layout = None

        return self.main_layout

    def start_camera(self, instance):
        self.main_layout.remove_widget(self.front_page_layout)

        self.img = Image()
        self.capture = cv2.VideoCapture(0)
        self.capture.set(3, 1280)
        self.capture.set(4, 720)
        self.capture.set(10, 70)

        self.camera_layout = BoxLayout(orientation='vertical')
        self.camera_layout.add_widget(self.img)

        self.main_layout.add_widget(self.camera_layout)

        Clock.schedule_interval(self.update, 1.0 / 30.0)

    def update(self, dt):
        thres = 0.45
        classNames = []
        classFile = 'coco.names'
        with open(classFile, 'rt') as f:
            classNames = f.read().rstrip('\n').split('\n')

        configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
        weightsPath = 'frozen_inference_graph.pb'

        net = cv2.dnn_DetectionModel(weightsPath, configPath)
        net.setInputSize(320, 320)
        net.setInputScale(1.0 / 127.5)
        net.setInputMean((127.5, 127.5, 127.5))
        net.setInputSwapRB(True)

        ret, frame = self.capture.read()
        if not ret:
            return

        classIds, confs, bbox = net.detect(frame, confThreshold=thres)

        if len(classIds) != 0:
            for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
                cv2.rectangle(frame, box, color=(0, 255, 0), thickness=2)
                cv2.putText(frame, classNames[classId - 1].upper(), (box[0] + 10, box[1] + 30),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, str(round(confidence * 100, 2)), (box[0] + 200, box[1] + 30),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

        buf1 = cv2.flip(frame, 0)
        buf = buf1.tostring()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.img.texture = texture

    def on_stop(self):
        # Release the camera when the app is closed
        if self.capture is not None:
            self.capture.release()

if __name__ == '__main__':
    MyApp().run()
