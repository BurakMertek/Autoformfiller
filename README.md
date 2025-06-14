# Automatic Form Filler

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python automation tool that automatically fills out forms using data from CSV files. Say goodbye to the tedious task of manually entering data into web forms or desktop applications!

## Features

- **Automated Form Filling**: Automatically fill out forms using data from CSV files
- **Multiple Navigation Methods**: Support for Tab, Enter, and Click navigation
- **Flexible Configuration**: Customizable timing, behavior, and safety settings
- **Resume Capability**: Resume from where you left off if interrupted
- **Safety Features**: Built-in failsafe and error handling
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Logging**: Comprehensive logging for debugging and monitoring
- **Multiple Form Types**: Works with web forms and desktop applications

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Install Dependencies

```bash
# Clone the repository
git clone https://github.com/BurakMertek/automatic-form-filler.git
cd automatic-form-filler

# Install required packages
pip install -r "Packages"

```

### Required Python Packages

- `pyautogui` - GUI automation
- `pandas` - Data manipulation
- `openpyxl` - Excel file support (optional)

## Quick Start

1. **Prepare your data**: Create a CSV file with your form data
   ```csv
   name,email,phone,address,city,zipcode
   John Doe,john@example.com,555-1234,123 Main St,Anytown,12345
   Jane Smith,jane@example.com,555-5678,456 Oak Ave,Somewhere,67890
   ```

2. **Configure field order**: Edit the field order in your script to match your form
   ```python
   field_order = ['name', 'email', 'phone', 'address', 'city', 'zipcode']
   ```

3. **Run the script**:
   ```bash
   python src/form_filler.py
   ```

4. **Position your form**: You'll have 5 seconds to click on the first field of your form

5. **Let it run**: The script will automatically fill and submit your forms!

## Usage

### Basic Usage

```python
from src.form_filler import FormFiller
from src.config import FormFillerConfig

# Create configuration
config = FormFillerConfig()

# Initialize form filler
filler = FormFiller(config)

# Load data
data = filler.load_data('data/your_data.csv')

# Define field order (must match your form)
field_order = ['name', 'email', 'phone']

# Fill forms
filler.wait_for_user_setup()
filler.fill_forms(data, field_order)
```

### Advanced Usage

```python
from src.config import CommonConfigs

# Use predefined configuration for web forms
config = CommonConfigs.web_forms()
filler = FormFiller(config)

# Process only first 10 records
filler.fill_forms(data, field_order, max_records=10)

# Resume from record 5
filler.fill_forms(data, field_order, start_row=5)
```

##  Configuration

The application supports extensive configuration through the `FormFillerConfig` class:

### Timing Settings
- `pause_between_actions`: General pause between actions (default: 0.5s)
- `typing_interval`: Delay between each character (default: 0.05s)
- `field_transition_delay`: Delay when moving between fields (default: 0.3s)
- `form_submission_delay`: Delay after submitting form (default: 2.0s)

### Navigation Settings
- `navigation_method`: How to move between fields ('tab', 'enter', 'click')
- `submission_method`: How to submit forms ('enter', 'tab_enter', 'click')

### Safety Settings
- `use_failsafe`: Enable failsafe (move mouse to corner to stop)
- `max_records_per_session`: Limit records processed per session

### Environment Variables

You can also configure the application using environment variables:

```bash
export FF_PAUSE_BETWEEN_ACTIONS=0.5
export FF_TYPING_INTERVAL=0.05
export FF_NAVIGATION_METHOD=tab
```

## Data Format

### CSV Format

Your CSV file should have column headers that match the field names you specify:

```csv
name,email,phone,company,address,city,state,zipcode
John Doe,john@example.com,555-1234,Acme Inc,123 Main St,Anytown,CA,12345
Jane Smith,jane@example.com,555-5678,Tech Corp,456 Oak Ave,Somewhere,NY,67890
```

### Supported Data Types

- Text fields
- Email addresses
- Phone numbers
- Addresses
- Numbers
- Dates (as text)

### Handling Empty Fields

The application will automatically skip empty fields (NaN values) unless configured otherwise.

## Examples

### Example 1: Simple Contact Form

```python
# Data: name, email, message
field_order = ['name', 'email', 'message']
filler.fill_forms(data, field_order)
```

### Example 2: Registration Form with Custom Config

```python
# Use slow, reliable configuration
config = CommonConfigs.slow_reliable()
filler = FormFiller(config)

field_order = ['first_name', 'last_name', 'email', 'password', 'phone']
filler.fill_forms(data, field_order)
```

### Example 3: Processing Large Dataset

```python
# Process in batches of 50
batch_size = 50
total_records = len(data)

for start_row in range(0, total_records, batch_size):
    print(f"Processing batch starting at record {start_row}")
    filler.fill_forms(data, field_order, start_row=start_row, max_records=batch_size)
    
    # Optional: pause between batches
    input("Press Enter to continue to next batch...")
```


