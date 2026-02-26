import time

try:
    import smbus # Biblioteca I2C comum no Raspberry Pi
except ImportError:
    smbus = None

class MPU6050_Aura:
    """Driver simplificado para ler o sensor MPU6050 no VLS-Alpha."""
    
    def __init__(self, address=0x68):
        self.address = address
        if smbus:
            self.bus = smbus.SMBus(1)
            # Acordar o sensor (Power Management)
            self.bus.write_byte_data(self.address, 0x6b, 0)
        else:
            print("⚠️ [AVISO] spmbus não instalado. Entrando em MODO SIMULADO.")
            self.bus = None

    def read_raw_data(self, addr):
        if self.bus:
            high = self.bus.read_byte_data(self.address, addr)
            low = self.bus.read_byte_data(self.address, addr+1)
            value = (high << 8) | low
            if value > 32768:
                value = value - 65536
            return value
        return 0

    def get_angles(self):
        """Lê aceleração e converte para ângulos aproximados de inclinação."""
        if not self.bus:
            # Simulação: Foguete estável com vibração mínima
            import random
            return {"tilt_x": random.uniform(-0.5, 0.5), "tilt_y": random.uniform(-0.5, 0.5)}
            
        acc_x = self.read_raw_data(0x3b)
        acc_y = self.read_raw_data(0x3d)
        acc_z = self.read_raw_data(0x3f)
        
        # Cálculo de Pitch e Roll simples
        tilt_x = (math.atan2(acc_y, acc_z) * 180.0) / math.pi
        tilt_y = (math.atan2(-acc_x, math.sqrt(acc_y*acc_y + acc_z*acc_z)) * 180.0) / math.pi
        
        return {"tilt_x": tilt_x, "tilt_y": tilt_y}

if __name__ == "__main__":
    sensor = MPU6050_Aura()
    print("🚀 [AURA SENSORS] Iniciando leitura do MPU6050...")
    
    try:
        while True:
            angles = sensor.get_angles()
            print(f"Inclinação -> X: {angles['tilt_x']:.2f}° | Y: {angles['tilt_y']:.2f}°", end="\r")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nLeitura encerrada.")
