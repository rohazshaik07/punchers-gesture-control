# Punchers Gesture Control
*Python 3.11 • OpenCV 4.10 • MediaPipe 0.10.14 • MIT License*
Play the Punchers boxing game through body gestures – a hands-free gaming experience using computer vision! 🚀

📖 **Overview**  

Punchers Gesture Control is an innovative project that lets you play the [Punchers game](https://www.crazygames.com/gae/pnchers) using webcam-captured body movements. Built with MediaPipe for pose detection, it offers single-player trining mdes and a two-player fight mode, mapping precise gestures to keyboard inputs for immersive boxing fun.



✨ **Features**  
- **Precise Gestures**:  
  -  *Left/Right Jab*: Extend arm straight up (150–180° angle).  
  -  *Lean Straight*: Raise elbows above face (high guard).  
  -  *Lean Down*: Lower hands below 95° from torso (duck).  
- **Role-Based Modes**:  
  -  *Left Man Training*: `W` (left jab), `S` (right jab), `A` (lean straight), `D` (lean down).  
  - *Right Man Training*: Up arrow (right jab), Down arrow (left jab), Right arrow (lean straight), Left arrow (lan dwn).  
- No extra hardware – just a webcam! 📷  
- Modular design for easy customization. 🛠️  
- Intelligent cooldown to prevent input spamming. ⏲️  
- Interactive role selection (L, R, T). 🎮  
🚀 **Getting Started**  
**Prerequisites**  
- Python 3.11  
- Webcam  
- [Punchers game](https://www.crazygames.com/game/punchers)  
**Installation**  

```
# Clone the repository
git clone https://github.com/yourusername/punchers-gesture-control.git
cd punchers-gesture-control
# Create and activate virtual environment
python -m venv punchers_env
# On Windows:
punchers_env\Scripts\activate
# On Unix/Linux/Mac:
source punchers_env/bin/activate
# Install dependencies
pip install -r requirements.txt
```
🎮 **Usage**  
1. Open [Punchers](https://www.crazygames.com/game/punchers) in a browser.  
2. Click the game window to focus.  
3. Run the script:  
   ```bash
   python main.py
   ```  
4. Choose a role:  
   - `L`: Left Man Training  
   - `R`: Right Man Training  
   - `T`: Two-Player Fight  
5. Perform gestures:  
   - Straight arm up for jabs.  
   - Elbows above face for lean straight.  
   - Hands below 95° for lean down.  
6. Press `esc` to quit.

⚙️ **Configuration**  

Customize gestures and keys (future feature):  
- `gesture_config.json`: Gesture thresholds (e.g., jab angle).  
- `key_config.json`: Key mappings per mode.  
- `pose_config.json`: MediaPipe settings.  
Currently, edit `gesture_recognition.py` and `key_controller.py` for adjustments.  

🧠 **Technical Architecture**  
- **Core Module**:  
  - `main.py`: Webcam, role selection, orchestration.  
- **Gesture Module**:  
  - `gesture_recognition.py`: MediaPipe-based gesture detection.  
- **Control Module**:  
  - `key_controller.py`: Precise keyboard input mapping.  

📊 **Performance**  
- Optimized frame rate for low lag.  
- Cooldown (0.3s) and short presses (0.01s) for precise inputs.  
- High-confidence detection (0.7) for reliability.  

🙏 **Acknowledgements**  
- [MediaPipe](https://mediapipe.dev) for pose detection.  
- [OpenCV](https://opencv.org) for computer vision.  
- [Pynput](https://pynput.readthedocs.io) for input simulation.  
- [PyAutoGUI](https://pyautogui.readthedocs.io) for browser focus.  

🌟 **Contributing**  
Fork the repo, create a branch, and submit a pull request. Issues and feature requests welcome!  

