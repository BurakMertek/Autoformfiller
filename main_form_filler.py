#!/usr/bin/env python3
"""
Automatic Form Filler

A Python application that automatically fills out web forms using data from CSV files.
Uses PyAutoGUI for GUI automation and pandas for data handling.

Author: Your Name
License: MIT
"""

import csv
import time
import sys
import logging
from pathlib import Path
from typing import List, Dict, Optional, Tuple

import pyautogui
import pandas as pd
from config import FormFillerConfig


class FormFiller:
    """Main class for automatic form filling functionality."""
    
    def __init__(self, config: FormFillerConfig):
        """
        Initialize the FormFiller with configuration.
        
        Args:
            config: FormFillerConfig object containing all settings
        """
        self.config = config
        self.logger = self._setup_logging()
        
        # Configure PyAutoGUI
        pyautogui.FAILSAFE = True  # Move mouse to top-left corner to abort
        pyautogui.PAUSE = self.config.pause_between_actions
        
        self.logger.info("FormFiller initialized successfully")
    
    def _setup_logging(self) -> logging.Logger:
        """Set up logging configuration."""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def load_data(self, file_path: str) -> pd.DataFrame:
        """
        Load data from CSV file.
        
        Args:
            file_path: Path to the CSV file
            
        Returns:
            DataFrame containing the form data
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            pd.errors.EmptyDataError: If the file is empty
        """
        try:
            data = pd.read_csv(file_path)
            self.logger.info(f"Loaded {len(data)} records from {file_path}")
            return data
        except FileNotFoundError:
            self.logger.error(f"File not found: {file_path}")
            raise
        except pd.errors.EmptyDataError:
            self.logger.error(f"Empty file: {file_path}")
            raise
    
    def wait_for_user_setup(self, countdown: int = 5) -> None:
        """
        Give user time to position windows and prepare for automation.
        
        Args:
            countdown: Number of seconds to wait
        """
        print(f"\nPrepare your form and click on the first field.")
        print("Form filling will start in:")
        
        for i in range(countdown, 0, -1):
            print(f"{i}...")
            time.sleep(1)
        
        print("Starting form filling! Move mouse to top-left corner to abort.")
        time.sleep(1)
    
    def click_field(self, field_position: Optional[Tuple[int, int]] = None) -> bool:
        """
        Click on a form field.
        
        Args:
            field_position: (x, y) coordinates of the field. If None, uses current mouse position.
            
        Returns:
            True if click was successful, False otherwise
        """
        try:
            if field_position:
                pyautogui.click(field_position[0], field_position[1])
            else:
                pyautogui.click()
            return True
        except pyautogui.FailSafeException:
            self.logger.warning("FailSafe triggered - stopping automation")
            return False
        except Exception as e:
            self.logger.error(f"Error clicking field: {e}")
            return False
    
    def type_text(self, text: str, clear_field: bool = True) -> bool:
        """
        Type text into the current field.
        
        Args:
            text: Text to type
            clear_field: Whether to clear the field before typing
            
        Returns:
            True if typing was successful, False otherwise
        """
        try:
            if clear_field:
                pyautogui.hotkey('ctrl', 'a')  # Select all
                time.sleep(0.1)
            
            pyautogui.write(str(text), interval=self.config.typing_interval)
            return True
        except pyautogui.FailSafeException:
            self.logger.warning("FailSafe triggered - stopping automation")
            return False
        except Exception as e:
            self.logger.error(f"Error typing text: {e}")
            return False
    
    def move_to_next_field(self, method: str = 'tab') -> bool:
        """
        Move to the next form field.
        
        Args:
            method: Method to use ('tab', 'enter', or 'click')
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if method == 'tab':
                pyautogui.press('tab')
            elif method == 'enter':
                pyautogui.press('enter')
            elif method == 'click':
                # This would require predefined coordinates
                pass
            else:
                self.logger.warning(f"Unknown navigation method: {method}")
                return False
            
            time.sleep(self.config.field_transition_delay)
            return True
        except pyautogui.FailSafeException:
            self.logger.warning("FailSafe triggered - stopping automation")
            return False
        except Exception as e:
            self.logger.error(f"Error moving to next field: {e}")
            return False
    
    def submit_form(self, method: str = 'enter') -> bool:
        """
        Submit the form.
        
        Args:
            method: Method to use ('enter', 'click', or 'tab_enter')
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if method == 'enter':
                pyautogui.press('enter')
            elif method == 'tab_enter':
                pyautogui.press('tab')
                time.sleep(0.5)
                pyautogui.press('enter')
            elif method == 'click':
                # Would require submit button coordinates
                pass
            
            time.sleep(self.config.form_submission_delay)
            return True
        except pyautogui.FailSafeException:
            self.logger.warning("FailSafe triggered - stopping automation")
            return False
        except Exception as e:
            self.logger.error(f"Error submitting form: {e}")
            return False
    
    def fill_single_record(self, record: Dict[str, str], field_order: List[str]) -> bool:
        """
        Fill a single record into the form.
        
        Args:
            record: Dictionary containing field values
            field_order: List of field names in the order they appear in the form
            
        Returns:
            True if successful, False otherwise
        """
        try:
            for field_name in field_order:
                if field_name in record:
                    value = record[field_name]
                    if pd.notna(value):  # Skip NaN values
                        if not self.type_text(value):
                            return False
                        
                        if not self.move_to_next_field():
                            return False
                else:
                    self.logger.warning(f"Field '{field_name}' not found in record")
                    # Still move to next field
                    if not self.move_to_next_field():
                        return False
            
            return True
        except Exception as e:
            self.logger.error(f"Error filling record: {e}")
            return False
    
    def fill_forms(self, data: pd.DataFrame, field_order: List[str], 
                   start_row: int = 0, max_records: Optional[int] = None) -> None:
        """
        Fill multiple forms with data from DataFrame.
        
        Args:
            data: DataFrame containing form data
            field_order: List of field names in order
            start_row: Row to start from (for resuming)
            max_records: Maximum number of records to process
        """
        try:
            if max_records:
                end_row = min(start_row + max_records, len(data))
            else:
                end_row = len(data)
            
            self.logger.info(f"Processing records {start_row} to {end_row-1}")
            
            for index in range(start_row, end_row):
                record = data.iloc[index].to_dict()
                
                self.logger.info(f"Processing record {index + 1}/{len(data)}")
                
                # Fill the form
                if not self.fill_single_record(record, field_order):
                    self.logger.error(f"Failed to fill record {index + 1}")
                    break
                
                # Submit the form
                if not self.submit_form():
                    self.logger.error(f"Failed to submit record {index + 1}")
                    break
                
                # Wait before next record
                time.sleep(self.config.record_delay)
                
                # Optional: Wait for page to load/refresh
                if self.config.wait_for_page_load:
                    time.sleep(self.config.page_load_delay)
                
                self.logger.info(f"Successfully processed record {index + 1}")
            
            self.logger.info("Form filling completed!")
            
        except KeyboardInterrupt:
            self.logger.info(f"Process interrupted by user at record {index + 1}")
            print(f"\nStopped at record {index + 1}. You can resume from this point.")
        except pyautogui.FailSafeException:
            self.logger.info("FailSafe activated - automation stopped")
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
    
    def get_screen_info(self) -> Dict[str, int]:
        """Get screen dimensions and current mouse position."""
        screen_width, screen_height = pyautogui.size()
        mouse_x, mouse_y = pyautogui.position()
        
        return {
            'screen_width': screen_width,
            'screen_height': screen_height,
            'mouse_x': mouse_x,
            'mouse_y': mouse_y
        }


def main():
    """Main function to run the form filler."""
    config = FormFillerConfig()
    filler = FormFiller(config)
    
    # Example usage
    try:
        # Load data
        data_file = "data/sample_data.csv"
        data = filler.load_data(data_file)
        
        # Define field order (should match your form)
        field_order = ['name', 'email', 'phone', 'address', 'city', 'zipcode']
        
        # Show screen info
        screen_info = filler.get_screen_info()
        print(f"Screen size: {screen_info['screen_width']}x{screen_info['screen_height']}")
        print(f"Current mouse position: ({screen_info['mouse_x']}, {screen_info['mouse_y']})")
        
        # Wait for user setup
        filler.wait_for_user_setup()
        
        # Fill forms
        filler.fill_forms(data, field_order)
        
    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Exiting...")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
