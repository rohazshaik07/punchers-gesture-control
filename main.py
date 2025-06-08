import logging
import sys
from gesture_recognition import GestureRecognizer, Role
from key_controller import KeyController

def select_role():
    print("\n=== Punchers Gesture Control ===")
    print("Choose your mode:")
    print("  [L] Left Man Training")
    print("  [R] Right Man Training")
    while True:
        role = input("Enter your choice (L/R): ").strip().upper()
        if role in ("L", "R"):
            return {"L": Role.LEFT, "R": Role.RIGHT}[role]
        print("Invalid input. Please enter 'L', 'R'.")

def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    role = select_role()
    try:
        recognizer = GestureRecognizer(role)
        controller = KeyController(role)

        for gestures, frame in recognizer.run():
            controller.handle_gestures(gestures)
            import cv2
            cv2.imshow("Punchers Gesture Control", frame)
            if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
                break
        recognizer.close()
        cv2.destroyAllWindows()
    except Exception as e:
        logging.exception("Fatal error occurred")
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()