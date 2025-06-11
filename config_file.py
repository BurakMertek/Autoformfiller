#!/usr/bin/env python3
"""
Configuration settings for the Automatic Form Filler.

This module contains all configurable parameters for the form filling automation.
Adjust these values based on your specific form requirements and system performance.
"""

import os
from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class FormFillerConfig:
    """Configuration class for Form Filler settings."""
    
    # Timing settings (in seconds)
    pause_between_actions: float = 0.5  # General pause between PyAutoGUI actions
    typing_interval: float = 0.05        # Interval between each character typed
    field_transition_delay: float = 0.3  # Delay when moving between fields
    form_submission_delay: float = 2.0   # Delay after submitting form
    record_delay: float = 1.0            # Delay between processing records
    page_load_delay: float = 3.0         # Wait time for page to load after submission
    
    # Behavior settings
    wait_for_page_load: bool = True      # Whether to wait for page load after submission
    clear_fields: bool = True            # Whether to clear fields before typing
    use_failsafe: bool = True            # Enable PyAutoGUI failsafe (move mouse to corner)
    
    # Form navigation settings
    navigation_method: str = 'tab'       # Method to move between fields ('tab', 'enter', 'click')
    submission_method: str = 'enter'     # Method to submit form ('enter', 'tab_enter', 'click')
    
    # Data handling settings
    skip_empty_fields: bool = True       # Skip fields with empty/NaN values
    max_field_length: Optional[int] = None  # Maximum characters per field (None for unlimited)
    encoding: str = 'utf-8'              # File encoding for CSV files
    
    # Safety settings
    max_records_per_session: Optional[int] = None  # Limit records per session
    confirmation_required: bool = True    # Require user confirmation before starting
    
    # Logging settings
    log_level: str = 'INFO'              # Logging level ('DEBUG', 'INFO', 'WARNING', 'ERROR')
    log_file: Optional[str] = None       # Log file path (None for console only)
    
    # Screen/UI settings
    screen_resolution: Optional[Tuple[int, int]] = None  # Expected screen resolution
    
    @classmethod
    def from_env(cls) -> 'FormFillerConfig':
        """
        Create configuration from environment variables.
        
        Returns:
            FormFillerConfig instance with values from environment
        """
        return cls(
            pause_between_actions=float(os.getenv('FF_PAUSE_BETWEEN_ACTIONS', '0.5')),
            typing_interval=float(os.getenv('FF_TYPING_INTERVAL', '0.05')),
            field_transition_delay=float(os.getenv('FF_FIELD_TRANSITION_DELAY', '0.3')),
            form_submission_delay=float(os.getenv('FF_FORM_SUBMISSION_DELAY', '2.0')),
            record_delay=float(os.getenv('FF_RECORD_DELAY', '1.0')),
            page_load_delay=float(os.getenv('FF_PAGE_LOAD_DELAY', '3.0')),
            
            wait_for_page_load=os.getenv('FF_WAIT_FOR_PAGE_LOAD', 'True').lower() == 'true',
            clear_fields=os.getenv('FF_CLEAR_FIELDS', 'True').lower() == 'true',
            use_failsafe=os.getenv('FF_USE_FAILSAFE', 'True').lower() == 'true',
            
            navigation_method=os.getenv('FF_NAVIGATION_METHOD', 'tab'),
            submission_method=os.getenv('FF_SUBMISSION_METHOD', 'enter'),
            
            skip_empty_fields=os.getenv('FF_SKIP_EMPTY_FIELDS', 'True').lower() == 'true',
            max_field_length=int(os.getenv('FF_MAX_FIELD_LENGTH')) if os.getenv('FF_MAX_FIELD_LENGTH') else None,
            encoding=os.getenv('FF_ENCODING', 'utf-8'),
            
            max_records_per_session=int(os.getenv('FF_MAX_RECORDS_PER_SESSION')) if os.getenv('FF_MAX_RECORDS_PER_SESSION') else None,
            confirmation_required=os.getenv('FF_CONFIRMATION_REQUIRED', 'True').lower() == 'true',
            
            log_level=os.getenv('FF_LOG_LEVEL', 'INFO'),
            log_file=os.getenv('FF_LOG_FILE'),
        )
    
    def validate(self) -> None:
        """
        Validate configuration values.
        
        Raises:
            ValueError: If any configuration values are invalid
        """
        if self.pause_between_actions < 0:
            raise ValueError("pause_between_actions must be non-negative")
        
        if self.typing_interval < 0:
            raise ValueError("typing_interval must be non-negative")
        
        if self.navigation_method not in ['tab', 'enter', 'click']:
            raise ValueError("navigation_method must be 'tab', 'enter', or 'click'")
        
        if self.submission_method not in ['enter', 'tab_enter', 'click']:
            raise ValueError("submission_method must be 'enter', 'tab_enter', or 'click'")
        
        if self.log_level not in ['DEBUG', 'INFO', 'WARNING', 'ERROR']:
            raise ValueError("log_level must be 'DEBUG', 'INFO', 'WARNING', or 'ERROR'")
        
        if self.max_field_length is not None and self.max_field_length <= 0:
            raise ValueError("max_field_length must be positive or None")
        
        if self.max_records_per_session is not None and self.max_records_per_session <= 0:
            raise ValueError("max_records_per_session must be positive or None")


# Predefined configurations for common scenarios
class CommonConfigs:
    """Predefined configurations for common use cases."""
    
    @staticmethod
    def fast_filling() -> FormFillerConfig:
        """Configuration for fast form filling (minimal delays)."""
        return FormFillerConfig(
            pause_between_actions=0.1,
            typing_interval=0.01,
            field_transition_delay=0.1,
            form_submission_delay=1.0,
            record_delay=0.5,
            page_load_delay=1.5,
        )
    
    @staticmethod
    def slow_reliable() -> FormFillerConfig:
        """Configuration for slow but reliable form filling."""
        return FormFillerConfig(
            pause_between_actions=1.0,
            typing_interval=0.1,
            field_transition_delay=0.5,
            form_submission_delay=3.0,
            record_delay=2.0,
            page_load_delay=5.0,
        )
    
    @staticmethod
    def web_forms() -> FormFillerConfig:
        """Configuration optimized for web forms."""
        return FormFillerConfig(
            pause_between_actions=0.5,
            typing_interval=0.05,
            field_transition_delay=0.3,
            form_submission_delay=2.0,
            record_delay=1.5,
            page_load_delay=4.0,
            navigation_method='tab',
            submission_method='enter',
            wait_for_page_load=True,
        )
    
    @staticmethod
    def desktop_apps() -> FormFillerConfig:
        """Configuration optimized for desktop applications."""
        return FormFillerConfig(
            pause_between_actions=0.3,
            typing_interval=0.03,
            field_transition_delay=0.2,
            form_submission_delay=1.0,
            record_delay=0.5,
            page_load_delay=1.0,
            navigation_method='tab',
            submission_method='enter',
            wait_for_page_load=False,
        )


# Default configuration instance
DEFAULT_CONFIG = FormFillerConfig()
