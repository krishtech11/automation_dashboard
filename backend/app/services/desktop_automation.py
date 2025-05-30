import os
import time
import subprocess
import pyautogui
from typing import Dict, Any, Optional

# Set a small delay between PyAutoGUI actions
pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = True

def open_application(app_name: str) -> Dict[str, Any]:
    """
    Open a desktop application.
    
    Args:
        app_name: Name of the application to open (e.g., 'notepad', 'wordpad', 'calc')
        
    Returns:
        Dict containing the result of the operation
    """
    try:
        app_paths = {
            'notepad': 'notepad.exe',
            'wordpad': 'wordpad.exe',
            'calculator': 'calc.exe',
            'paint': 'mspaint.exe',
            'chrome': 'chrome.exe',
            'firefox': 'firefox.exe',
            'edge': 'msedge.exe'
        }
        
        app = app_paths.get(app_name.lower())
        if not app:
            return {"status": "error", "message": f"Application '{app_name}' is not supported"}
        
        # Close the application if it's already running
        close_application(app_name)
        
        # Open the application
        os.startfile(app)
        time.sleep(2)  # Wait for the application to open
        
        return {"status": "success", "message": f"Successfully opened {app_name}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def close_application(app_name: str) -> Dict[str, Any]:
    """
    Close a running application.
    
    Args:
        app_name: Name of the application to close
        
    Returns:
        Dict containing the result of the operation
    """
    try:
        app_names = {
            'notepad': 'notepad.exe',
            'wordpad': 'wordpad.exe',
            'calculator': 'calculator.exe',
            'paint': 'mspaint.exe',
            'chrome': 'chrome.exe',
            'firefox': 'firefox.exe',
            'edge': 'msedge.exe'
        }
        
        process_name = app_names.get(app_name.lower())
        if not process_name:
            return {"status": "error", "message": f"Application '{app_name}' is not supported"}
        
        # Kill the process
        subprocess.call(f'taskkill /f /im {process_name}', shell=True)
        time.sleep(1)  # Wait for the process to close
        
        return {"status": "success", "message": f"Successfully closed {app_name}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def type_text(text: str) -> Dict[str, Any]:
    """
    Type text at the current cursor position.
    
    Args:
        text: Text to type
        
    Returns:
        Dict containing the result of the operation
    """
    try:
        pyautogui.write(text, interval=0.1)
        return {"status": "success", "message": f"Successfully typed {len(text)} characters"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def press_key(key: str) -> Dict[str, Any]:
    """
    Simulate pressing a key.
    
    Args:
        key: Key to press (e.g., 'enter', 'tab', 'esc')
        
    Returns:
        Dict containing the result of the operation
    """
    try:
        pyautogui.press(key)
        return {"status": "success", "message": f"Successfully pressed {key} key"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def automate_desktop(
    app_name: str,
    action: str,
    text: Optional[str] = None
) -> Dict[str, Any]:
    """
    Main function to handle desktop automation.
    """
    try:
        result = {}

        if not app_name:
            return {"status": "error", "message": "Application name is required"}

        if action == 'open':
            result = open_application(app_name)
        elif action == 'close':
            result = close_application(app_name)
        elif action == 'type':
            if not text:
                return {"status": "error", "message": "Text is required for 'type' action"}
            open_result = open_application(app_name)
            if open_result.get("status") == "error":
                return open_result
            time.sleep(1)
            result = type_text(text)
        elif action == 'press':
            if not text:
                return {"status": "error", "message": "Key is required for 'press' action"}
            result = press_key(text)
        else:
            return {"status": "error", "message": f"Unsupported action: {action}"}

        return result
    except Exception as e:
        return {"status": "error", "message": f"Unexpected backend error: {str(e)}"}

