import time

class VLS_PID_Controller:
    """Controlador de Estabilização para o VLS-Alpha (Cano de PVC)."""
    
    def __init__(self, kp, ki, kd):
        self.kp = kp # Ganho Proporcional (Reação imediata)
        self.ki = ki # Ganho Integral (Correção de erros acumulados)
        self.kd = kd # Ganho Derivativo (Amortecimento de oscilação)
        
        self.last_error = 0
        self.integral = 0
        self.target_angle = 0 # Vertical perfeita
        
    def compute(self, current_angle, dt):
        """Calcula a correção necessária para os servos."""
        error = self.target_angle - current_angle
        
        # P: Proporcional
        proportional = self.kp * error
        
        # I: Integral
        self.integral += error * dt
        integral = self.ki * self.integral
        
        # D: Derivativo
        derivative = self.kd * (error - self.last_error) / dt
        
        # Saída Total
        output = proportional + integral + derivative
        
        self.last_error = error
        return output

# --- EXEMPLO DE USO ---
if __name__ == "__main__":
    # Constantes calibradas para o peso do PVC
    controlador = VLS_PID_Controller(kp=1.5, ki=0.1, kd=0.5)
    
    print("🚀 [AURA VLS] Iniciando Loop de Estabilização...")
    
    # Simulação de inclinação (Erro de 5 graus causado pelo vento)
    tilt_current = 5.0 
    dt = 0.01 # Ciclo de 10ms
    
    for _ in range(10):
        correcao = controlador.compute(tilt_current, dt)
        print(f"Inclinação: {tilt_current:.2f}° | Comando Servo: {correcao:.4f}")
        
        # Simula a resposta física (o foguete endireitando)
        tilt_current += correcao * 0.2
        time.sleep(dt)

    print("\n✅ VLS Estabilizado pela Aura.")
