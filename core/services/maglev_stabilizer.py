import time

class MagLevStabilizer:
    """Controlador de Levitação Magnética para o protótipo de 1 metro."""
    
    def __init__(self, target_height=10.0):
        # PID agressivo para magnetismo (sistema inerentemente instável)
        self.kp = 12.5 
        self.ki = 1.2
        self.kd = 4.5
        
        self.target_height = target_height # Altura em mm
        self.last_error = 0
        self.integral = 0
        
    def calculate_pwm(self, current_height, dt):
        """Calcula a potência magnética necessária (0-100%)."""
        error = self.target_height - current_height
        
        # P
        p_out = self.kp * error
        # I
        self.integral += error * dt
        i_out = self.ki * self.integral
        # D
        d_out = self.kd * (error - self.last_error) / dt
        
        output = p_out + i_out + d_out
        self.last_error = error
        
        # Limitador PWM
        return max(0, min(100, output))

if __name__ == "__main__":
    mag = MagLevStabilizer()
    print("🧲 [AURA MAGLEV] Iniciando estabilização magnética...")
    
    # Simulação de queda por gravidade sendo corrigida por eletroímã
    h = 0.0 # Começa no chão
    dt = 0.005 # 200Hz loop (levitação exige alta velocidade)
    
    for _ in range(20):
        pwm = mag.calculate_pwm(h, dt)
        print(f"Altura: {h:5.2f}mm | Potência Magnética: {pwm:5.1f}%")
        
        # Simula física simples
        if pwm > 50: h += 1.0 # Sobe
        else: h -= 0.5 # Cai
        
        time.sleep(dt)
