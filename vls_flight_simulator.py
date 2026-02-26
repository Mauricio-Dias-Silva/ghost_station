import time
import random
import math

class VLS_Alpha_Sim:
    """Simulador de voo para o protótipo VLS-Alpha (Cano de PVC)."""
    
    def __init__(self):
        self.altitude = 0.0
        self.velocity = 0.0
        self.tilt_x = 0.0
        self.thrust = 1500.0 # Newtons simulados
        self.mass = 1.2 # kg
        
    def step(self, servo_correction, dt):
        """Executa um passo físico na simulação."""
        # Gravidade
        g = 9.81
        
        # Influência do Vento (Perturbação)
        wind = random.normalvariate(0, 2.0)
        self.tilt_x += wind * dt - (servo_correction * 0.5)
        
        # Aceleração Vertical
        accel_y = (self.thrust / self.mass) - g if self.thrust > 0 else -g
        self.velocity += accel_y * dt
        self.altitude += self.velocity * dt
        
        # Efeito do arraste de aleta
        self.velocity *= 0.99
        
        if self.altitude < 0:
            self.altitude = 0
            self.velocity = 0
            
        return {
            "altitude": self.altitude,
            "tilt": self.tilt_x,
            "velocity": self.velocity
        }

if __name__ == "__main__":
    sim = VLS_Alpha_Sim()
    from vls_alpha_pid import VLS_PID_Controller
    
    pid = VLS_PID_Controller(kp=1.5, ki=0.1, kd=0.5)
    dt = 0.1
    
    print("🚀 [FLIGHT SIM] T-Minus 0. Lançamento VLS-Alpha!")
    
    for t in range(50):
        # 1. PID lê a inclinação simulada
        cmd = pid.compute(sim.tilt_x, dt)
        
        # 2. Simulador processa a correção
        state = sim.step(cmd, dt)
        
        print(f"T+{t*dt:.1f}s | Alt: {state['altitude']:6.2f}m | Tilt: {state['tilt']:5.2f}° | CMD: {cmd:5.2f}")
        
        if t > 30: sim.thrust = 0 # Fim da combustão
        time.sleep(0.05)
        
    print("\n✅ Simulação concluída com sucesso.")
