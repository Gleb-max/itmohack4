import cv2
from threading import Thread

from emotion import EmotionAnalyze

vid = cv2.VideoCapture(0)

analyzer = EmotionAnalyze()

# is_running = True


# def analyze_while_true():
#     while is_running:
#         analyzer.analyze_image()
#
#
# analyzer_thread = Thread(target=analyze_while_true)
# analyzer_thread.start()

while True:
    ret, frame = vid.read()
    cv2.putText(frame,
                analyzer.get_emotion(),
                (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0, 255, 255),
                2,
                cv2.LINE_4)
    cv2.imshow('Yarik Cuck Old', frame)
    # analyzer.analyze_image(frame)
    Thread(target=lambda: analyzer.analyze_image(frame)).start()
    # cv2.imwrite('photo.jpg', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
vid.release()
cv2.destroyAllWindows()
# is_running = False
# analyzer_thread.join()
