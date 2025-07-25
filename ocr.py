import pygetwindow as gw
import pyautogui
import pytesseract
import time
import cv2
import numpy as np
from PIL import Image


def capture_and_extract_message():
    windows = [w for w in gw.getAllTitles() if 'WhatsApp' in w]
    if not windows:
        return None
    try:
        win = gw.getWindowsWithTitle(windows[0])[0]
        win.activate()
        time.sleep(1)
        bbox = (win.left, win.top, win.left + win.width, win.top + win.height)
        screenshot = pyautogui.screenshot(region=bbox)
        screenshot.save('debug_whatsapp_screenshot.png')

        # Convert PIL image to OpenCV format
        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        # Convert to grayscale and threshold to find light areas
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

        # Find contours
        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        # Find the largest contour (likely the chat area)
        largest_area = 0
        chat_rect = None
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            area = w * h
            if area > largest_area:
                largest_area = area
                chat_rect = (x, y, w, h)

        if chat_rect:
            x, y, w, h = chat_rect
            # Draw rectangle on the original image
            highlighted_img = img.copy()
            cv2.rectangle(highlighted_img, (x, y), (x + w, y + h), (0, 0, 255), 3)
            cv2.imwrite('debug_highlighted_chat_area.png', highlighted_img)

            # Save the cropped chat area
            chat_img = img[y:y+h, x:x+w]
            cv2.imwrite('debug_chat_area.png', chat_img)
            
            # Preprocess the image for better OCR
            # Convert to grayscale
            chat_gray = cv2.cvtColor(chat_img, cv2.COLOR_BGR2GRAY)
            # Apply Gaussian blur to reduce noise
            chat_blur = cv2.GaussianBlur(chat_gray, (1, 1), 0)
            # Apply adaptive thresholding
            chat_thresh = cv2.adaptiveThreshold(
                chat_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                cv2.THRESH_BINARY, 11, 2
            )
            
            # Save preprocessed image for debugging
            cv2.imwrite('debug_preprocessed_chat.png', chat_thresh)
            
            # Convert back to PIL for pytesseract
            chat_pil = Image.fromarray(chat_thresh)
            
            # Use better OCR configuration for longer text
            custom_config = (
                r'--oem 3 --psm 6 -c tessedit_char_whitelist='
                r'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
                r'0123456789.,!?@#$%&*()_+-=[]{}|;:,.<>?/~` '
            )
            text = pytesseract.image_to_string(chat_pil, config=custom_config)
            print("OCR Output:", text)
            
            # Extract multiple lines instead of just the last one
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            if lines:
                # Return the last 3 lines (or fewer if less available) to get more context
                num_lines = min(3, len(lines))
                return '\n'.join(lines[-num_lines:])
            return None
        else:
            print("Chat area not detected.")
            return None
    except Exception as e:
        print(f'Error capturing message: {e}')
        return None 