# objectdetection_mcb_wires

The dataset was made from scratch - collecting , annotating and preprocessing the data.
**Version 1: YOLOv8 Object Detection Model**

In the first version of our object detection project, we utilized the state-of-the-art YOLOv8 (You Only Look Once version 8) model. This model was trained to detect miniature circuit breakers (MCBs) and wires within images and videos. It efficiently labels these objects and makes predictions on both image and video inputs.
We showcased this project on Google Colab, a cloud-based platform for running Python code, providing accessibility and ease of use for users. The YOLOv8 model's accuracy and real-time processing capabilities make it an effective tool for identifying MCBs and wires within visual media.
The results of this version is stored in file named predict, predict-img and predict-videos

**Version 2: Roboflow Object Detection with Real-time Webcam Integration**

In our second version, we leveraged a pre-trained object detection model obtained from the Roboflow platform. This model was designed to detect MCBs and wires in real-time using a webcam feed. To accomplish this, we utilized the OpenCV library, a powerful computer vision tool.
The system captures live video from a webcam and applies the Roboflow object detection model to identify MCBs and wires as they appear in the video stream. This real-time functionality is beneficial for applications such as monitoring electrical grid components in real-world scenarios.
Both versions of our project offer unique advantages, with the first focusing on pre-recorded images and videos, and the second providing real-time object detection through webcam integration. These solutions cater to different use cases and provide valuable insights into the application of object detection technology.
The result of this version is stored in the file named results 
