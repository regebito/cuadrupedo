from multiprocessing import Process, Queue
import cv2
import mediapipe as mp
import time
import pyautogui

# Configuración de la cámara y sensibilidad
ejexcamarasuperior = 0.25
ejexcamarainferior = 0.75
ejeycamarasuperior = 0.75   
ejeycamarainferior = 0.25
sensibilidad = 1
ejexcamarasensibilidadsuperior = ejexcamarasuperior * sensibilidad
ejeycamarasensibilidadsuperior = ejeycamarasuperior * sensibilidad
ejexcamarasensibilidadinferior = ejexcamarainferior * sensibilidad
ejeycamarasensibilidadinferior = ejeycamarainferior * sensibilidad

margeninferior=-0.03
margensuperior=0.03
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
def captura_puntos(q):
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    cap = cv2.VideoCapture(0)
    finger_tips = [4, 8, 12, 16, 20]

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        data = {}
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                first_hand = results.multi_hand_landmarks[0]  # Acceder a la primera mano detectada
                indice = first_hand.landmark[8]  # Acceder al punto específico (por ejemplo, índice 8)
                pulgar = first_hand.landmark[4]
                corazon = first_hand.landmark[12]
                anular = first_hand.landmark[16]
                menique = first_hand.landmark[20]
                #print("nuevamano")
                #print(f"indice {indice.x},  {indice.y}")
                #print(f"pulgar {pulgar.x}{pulgar.y}")
                #print(f"anular {anular.x}{anular.y}")
                #print(f"corazon {corazon.x}{corazon.y}")
                #print(f"menique {menique.x}{menique.y}")
                #print(corazon.x)
                #print(pulgar.x)
                distanciacorazonpulgarx= -corazon.x+pulgar.x
                distanciacorazonpulgary= -corazon.y+pulgar.y
                print(f"distancia x {distanciacorazonpulgarx} distancia y {distanciacorazonpulgary}")
                ratonx = 1920*(indice.x-ejexcamarasensibilidadinferior)/(ejexcamarasensibilidadsuperior-ejexcamarasensibilidadinferior)
                ratony = 1080*(indice.y-ejeycamarasensibilidadinferior)/(ejeycamarasensibilidadsuperior-ejeycamarasensibilidadinferior)
                
            #print(f"Punto y = {y} puntocalculado = {ratony}")
            if (distanciacorazonpulgarx<margensuperior and distanciacorazonpulgarx>margeninferior):
                pyautogui.click(button='left', clicks=1, interval=0.0, duration=0.0)
                print("he clicado")
                #pyautogui.hotkey('alt', 'tab','alt')
                #pyautogui.press('alt')



            pyautogui.moveTo(ratonx,ratony)  # Mueve el cursor a (X=500, Y=500)

        
        if data:  
            q.put(data)  # Solo enviar datos si hay algo detectado
        
        cv2.imshow('Hand Tracking', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def procesar_datos(q):
    while True:
        if not q.empty():  # Solo intentar leer si hay datos disponibles
            data = q.get()
            if 8 in data:  # Verifica si el dedo índice está en los datos
                indicex = data[8]["x"]
                indicey = data[8]["y"]
                #print(indicex,indicey)
                #print(f"Punta del índice: X={indicex:.3f}, Y={indicey:.3f}")

                # Cálculo de posición del ratón basado en coordenadas de la cámara
                ratonx = 1920*(indicex-ejexcamarasensibilidadsuperior)/(ejexcamarasensibilidadinferior-ejexcamarasensibilidadsuperior)
                ratony = 1080*(indicey-ejeycamarasensibilidadinferior)/(ejeycamarasensibilidadsuperior-ejeycamarasensibilidadinferior)
                pyautogui.moveTo(ratonx, ratony)

        time.sleep(0.05)  # Evitar consumo excesivo de CPU

if __name__ == "__main__":
    q = Queue()
    p1 = Process(target=captura_puntos, args=(q,))
    p2 = Process(target=procesar_datos, args=(q,))

    p1.daemon = True  # Permite que el proceso termine cuando el programa principal finaliza
    p2.daemon = True

    p1.start()
    p2.start()

    # Bucle principal para mantener el programa vivo
    try:
        while True:
            time.sleep(1)  # Mantener el programa corriendo sin consumir CPU
    except KeyboardInterrupt:
        print("Terminando procesos...")
