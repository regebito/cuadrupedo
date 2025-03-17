import multiprocessing
import cv2
import mediapipe as mp
import pyautogui
import time

def detectar_mano(queue):
    """ Captura los puntos de los dedos y los envía sin delay """
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    cap = cv2.VideoCapture(0)

    with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Voltear la imagen horizontalmente y convertirla a RGB
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb_frame)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

                    # Normalizar coordenadas a valores de pantalla
                    screen_w, screen_h = pyautogui.size()
                    x_index, y_index = int(index_tip.x * screen_w), int(index_tip.y * screen_h)

                    # Enviar inmediatamente la coordenada
                    queue.put((x_index, y_index))
                    print(queue)
                    # Dibujar puntos en la mano
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            cv2.imshow("Detección de Mano", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()
    
    queue.put(None)  # Señal de terminación

def mover_raton(queue):
    """ Recibe las coordenadas del dedo índice y mueve el ratón en tiempo real """
    last_x, last_y = pyautogui.position()  # Obtener posición inicial del ratón

    while True:
        coords = queue.get()
        if coords is None:
            break  # Terminar proceso

        x, y = coords

        # Suavizar el movimiento con un filtro básico (media entre última y nueva posición)
        smooth_x = (last_x * 0.7) + (x * 0.3)
        smooth_y = (last_y * 0.7) + (y * 0.3)

        pyautogui.moveTo(smooth_x, smooth_y, duration=0.01, _pause=False)  # Movimiento rápido sin pausa

        last_x, last_y = smooth_x, smooth_y  # Actualizar última posición

if __name__ == "__main__":
    queue = multiprocessing.Queue(maxsize=10)  # Limitar el buffer para reducir lag

    # Crear los procesos
    proceso_deteccion = multiprocessing.Process(target=detectar_mano, args=(queue,))
    proceso_movimiento = multiprocessing.Process(target=mover_raton, args=(queue,))

    proceso_deteccion.start()
    proceso_movimiento.start()

    proceso_deteccion.join()
    proceso_movimiento.join()

    print("Procesos finalizados.")
