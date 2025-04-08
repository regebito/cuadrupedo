import multiprocessing
import cv2
import mediapipe as mp
import pyautogui
import time
margeninferior=-70
margensuperior=70
sensibilidad = 1.5
numerodenoclicks=5
numerodeclicks=5

def detectar_mano(queue):
    """ Captura las coordenadas de todas las puntas de los dedos y las envía en tiempo real """
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    cap = cv2.VideoCapture(0)

    with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)  # Voltear horizontalmente
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb_frame)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Diccionario para almacenar las coordenadas de las puntas de los dedos
                    dedos = {
                        "pulgar": None,
                        "indice": None,
                        "medio": None,
                        "anular": None,
                        "meñique": None
                    }

                    # Obtener el tamaño de la pantalla
                    screen_w, screen_h = pyautogui.size()
                    
                    # Obtener coordenadas de cada dedo
                    dedos["pulgar"] = (int(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x * screen_w * sensibilidad),
                                       int(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y * screen_h * sensibilidad))
                    
                    dedos["indice"] = (int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * screen_w * sensibilidad),
                                       int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * screen_h * sensibilidad))
                    
                    dedos["medio"] = (int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x * screen_w * sensibilidad),
                                      int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * screen_h * sensibilidad))
                    
                    dedos["anular"] = (int(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x * screen_w* sensibilidad),
                                       int(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y * screen_h * sensibilidad))
                    
                    dedos["meñique"] = (int(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x * screen_w * sensibilidad),
                                        int(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y * screen_h * sensibilidad))
                    print(dedos["pulgar"])
                    # Enviar el diccionario con las coordenadas de los dedos
                    queue.put(dedos)

                    # Dibujar la mano en la imagen
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            cv2.imshow("Detección de Mano", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()
    
    queue.put(None)  # Señal de terminación

def mostrar_coordenadas(queue):
    contadorclicks=0
    contadornoclicks=0
    """ Recibe y muestra las coordenadas de todas las puntas de los dedos en tiempo real """
    while True:
        dedos = queue.get()
        if dedos is None:
            break  # Terminar proceso
        last_x, last_y = pyautogui.position()  # Obtener posición inicial del ratón

        xpulgar, ypulgar = dedos["pulgar"]  # Coordenadas del dedo pulgar
        xindice, yindice = dedos["indice"]  # Coordenadas del dedo índice
        xmedio, ymedio = dedos["medio"] # Coordenadas del dedo medio
        xanular, yanular = dedos["anular"]  # Coordenadas del dedo anular
        xmeñique, ymeñique = dedos["meñique"]   # Coordenadas del dedo meñique
        
        distanciacorazonpulgarx= xmedio-xpulgar
        distanciacorazonpulgary= ymedio-ypulgar

        smooth_x = (last_x * 0.7) + (xindice * 0.3)
        smooth_y = (last_y * 0.7) + (yindice * 0.3)

        pyautogui.moveTo(smooth_x, smooth_y, duration=0.01, _pause=False)  # Movimiento rápido sin pausa

        last_x, last_y = smooth_x, smooth_y  # Actualizar última posición

        #print(distanciacorazonpulgarx,distanciacorazonpulgary)
        #print(f"Pulgar: {dedos['pulgar']} | Índice: {dedos['indice']} | Medio: {dedos['medio']} | Anular: {dedos['anular']} | Meñique: {dedos['meñique']}")        
        if (distanciacorazonpulgarx<margensuperior and distanciacorazonpulgarx>margeninferior)and(distanciacorazonpulgary<margensuperior and distanciacorazonpulgary>margeninferior):
            contadorclicks+=1
            contadornoclicks=0
            if contadorclicks==numerodeclicks:
                pyautogui.mouseDown(button='left')  # Mantiene presionado el botón izquierdo
                print("he clicado")
                contadornoclicks=0
        else:
            contadorclicks=0
            contadornoclicks+=1
            if contadornoclicks==numerodenoclicks:
                pyautogui.mouseUp(button='left')
                print("he dejado de clicar")
                contadorclicks=0 
if __name__ == "__main__":
    queue = multiprocessing.Queue(maxsize=10)  # Buffer limitado para evitar acumulación

    # Crear procesos
    proceso_deteccion = multiprocessing.Process(target=detectar_mano, args=(queue,))
    proceso_mostrar = multiprocessing.Process(target=mostrar_coordenadas, args=(queue,))

    proceso_deteccion.start()
    proceso_mostrar.start()

    proceso_deteccion.join()
    proceso_mostrar.join()

    print("Procesos finalizados.")