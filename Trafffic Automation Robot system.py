import time
import random
import threading
from enum import Enum

class SignalState(Enum):
    RED = "RED"
    YELLOW = "YELLOW"
    GREEN = "GREEN"

class RobotSpeaker:
    """Robot guidance interface providing audio/text alerts for commuters."""
    @staticmethod
    def speak(message: str, target: str):
        prefix = f"🤖 [ROBOT ANNOUNCEMENT -> {target.upper()}]:"
        print(f"\033[94m{prefix} '{message}'\033[00m")

class TrafficRobotController:
    def __init__(self):
        # Current Signal States
        self.vehicle_signal = SignalState.RED
        self.pedestrian_signal = SignalState.RED
        
        # Sensor Inputs
        self.vehicle_queue = 0
        self.pedestrian_waiting = False
        self.is_running = False

    def update_sensors(self):
        """Simulates real-time sensor readings (cameras, induction loops)."""
        while self.is_running:
            # Simulate dynamic incoming vehicles and pedestrian button presses
            self.vehicle_queue = random.randint(1, 25)
            if not self.pedestrian_waiting and random.random() > 0.6:
                self.pedestrian_waiting = True
                print("\n[SENSOR]: Pedestrian crosswalk button pressed! 🚶")
            time.sleep(4)

    def display_status(self):
        """Displays current intersection status visually."""
        print("\n" + "="*50)
        print(f"🚦 VEHICLE SIGNAL  : [{self.vehicle_signal.value}] (Cars waiting: {self.vehicle_queue})")
        print(f"🚶 PEDESTRIAN SIGNAL: [{self.pedestrian_signal.value}] (Waiting: {self.pedestrian_waiting})")
        print("="*50)

    def run_cycle(self):
        """Core logic governing signal transitions and safety guidance."""
        while self.is_running:
            self.display_status()

            # --- CASE 1: Pedestrian Crossing Priority ---
            if self.pedestrian_waiting:
                RobotSpeaker.speak("Vehicle signal turning RED in 3 seconds. Drivers, prepare to stop.", "Drivers")
                time.sleep(2)
                
                # Switch vehicles to Yellow then Red
                self.vehicle_signal = SignalState.YELLOW
                self.display_status()
                time.sleep(2)
                
                self.vehicle_signal = SignalState.RED
                self.pedestrian_signal = SignalState.GREEN
                self.display_status()
                
                RobotSpeaker.speak("Walk signal is ACTIVE. Pedestrians may cross safely.", "Pedestrians")
                time.sleep(6)  # Safe pedestrian crossing duration
                
                # Clear pedestrian state
                RobotSpeaker.speak("Crosswalk closing. Pedestrians, please wait on the curb.", "Pedestrians")
                self.pedestrian_signal = SignalState.RED
                self.pedestrian_waiting = False
                time.sleep(1)

            # --- CASE 2: Vehicle Flow Control (Adaptive Timing) ---
            else:
                self.pedestrian_signal = SignalState.RED
                self.vehicle_signal = SignalState.GREEN
                
                # Dynamic timing: heavier traffic keeps green light longer
                green_duration = 8 if self.vehicle_queue > 12 else 4
                
                RobotSpeaker.speak(f"Green light active. Proceed safely at current speed limit.", "Drivers")
                self.display_status()
                time.sleep(green_duration)

                # Transition to Yellow
                self.vehicle_signal = SignalState.YELLOW
                RobotSpeaker.speak("Signal changing to RED. Clear the intersection.", "Drivers")
                self.display_status()
                time.sleep(2)

                self.vehicle_signal = SignalState.RED

    def start(self):
        """Starts sensor thread and automation controller."""
        self.is_running = True
        
        # Run sensor updating in a background thread
        sensor_thread = threading.Thread(target=self.update_sensors, daemon=True)
        sensor_thread.start()

        print("🤖 Traffic Robot Assistant Activated. Initializing intersection loop...")
        try:
            self.run_cycle()
        except KeyboardInterrupt:
            self.is_running = False
            print("\n🛑 Traffic Automation Controller Shutdown.")

if __name__ == "__main__":
    controller = TrafficRobotController()
    controller.start()