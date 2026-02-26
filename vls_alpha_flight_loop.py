import time
from vls_alpha_pid import VLS_PID_Controller
from vls_alpha_sensors import MPU6050_Aura

def main_flight_loop():
    """Loop principal de controle da Aura para o VLS-Alpha."""
    print("--- [AURA MISSION CONTROL: VLS-ALPHA FLIGHT LOOP] ---")
    
    # Inicializar Componentes
    sensor = MPU6050_Aura()
    pid_x = VLS_PID_Controller(kp=1.5, ki=0.1, kd=0.5)
    pid_y = VLS_PID_Controller(kp=1.5, ki=0.1, kd=0.5)
    
    print("⚡ SISTEMA ARMADO. Iniciando estabilização ativa...")
    
    last_time = time.time()
    
    try:
        while True:
            current_time = time.time()
            dt = current_time - last_time
            if dt == 0: dt = 0.001
            
            # 1. Ler os 'Olhos' (Sensores)
            angles = sensor.get_angles()
            
            # 2. Calcular 'Reação' (PID)
            comando_x = pid_x.compute(angles['tilt_x'], dt)
            comando_y = pid_y.compute(angles['tilt_y'], dt)
            
            # 3. Executar 'Ação' (Servos)
            # Aqui entraria a biblioteca RPi.GPIO ou pigpio para mover os servos
            print(f"[NAV] X: {angles['tilt_x']:5.2f} | Y: {angles['tilt_y']:5.2f} | CMD: {comando_x:6.2f}/{comando_y:6.2f} ", end="\r")
            
            last_time = current_time
            time.sleep(0.01) # Ciclo de 100Hz
            
    except KeyboardInterrupt:
        print("\n\nSISTEMA DESARMADO. VLS em segurança.")

if __name__ == "__main__":
    main_flight_loop()
