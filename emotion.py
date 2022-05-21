import time

from fer import FER
import matplotlib.pyplot as plt


# import time
#
# start = time.time()
# # %matplotlib inline
#
# test_image_one = plt.imread("photo.jpg")
# emo_detector = FER(mtcnn=True)
# # Capture all the emotions on the image
# captured_emotions = emo_detector.detect_emotions(test_image_one)
# # Print all captured emotions with the image
# print(captured_emotions)
# plt.imshow(test_image_one)
#
# # Use the top Emotion() function to call for the dominant emotion in the image
# dominant_emotion, emotion_score = emo_detector.top_emotion(test_image_one)
# print(dominant_emotion, emotion_score)
#
# end = time.time()
# print("--- %s seconds ---" % (time.time() - start))


class EmotionAnalyze:
    def __init__(self):
        self.emotion_now = None
        self.is_busy = False

    def analyze_image(self, image):
        if self.is_busy:
            return
        self.is_busy = True
        start = time.time()
        # try:
        #     test_image_one = plt.imread("photo.jpg")
        # except Exception as e:
        #     print(e)
        #     return
        emo_detector = FER(mtcnn=True)
        # Capture all the emotions on the image
        # captured_emotions = emo_detector.detect_emotions(image)
        # Print all captured emotions with the image
        # print(captured_emotions)
        # plt.imshow(test_image_one)

        # Use the top Emotion() function to call for the dominant emotion in the image
        dominant_emotion, emotion_score = emo_detector.top_emotion(image)
        self.emotion_now = dominant_emotion
        print("--- %s seconds ---" % (time.time() - start))
        self.is_busy = False

    def get_emotion(self) -> str:
        return self.emotion_now or 'Analyzing...'


if __name__ == '__main__':
    analyzer = EmotionAnalyze()
    analyzer.analyze_image()
