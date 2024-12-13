# Shoemaker2

Shoemaker2 is a modular RPA solution designed to automate the retrieval of real estate tax data. It includes:
- Command-Line and GUI interfaces.
- Modular architecture for scalability and flexibility.

## Directory Structure
Shoemaker2/
├─ src/
│  ├─ orchestrator/
│  │   ├─ __init__.py
│  │   ├─ main_orchestrator.py  # Entry point for CLI and GUI
│  │   ├─ gui_orchestrator.py  # GUI logic
│  │
│  ├─ cases/
│  │   ├─ __init__.py
│  │   └─ case_processor.py
│  │
│  ├─ parsers/
│  │   ├─ __init__.py
│  │   └─ html_parser.py
│  │
│  ├─ drivers/
│  │   ├─ __init__.py
│  │   └─ browser_driver.py
│  │
│  ├─ utils/
│  │   ├─ __init__.py
│  │   ├─ config.py
│  │   ├─ logger.py
│  │   └─ helpers.py
│  │
│  ├─ __init__.py
│
├─ tests/
│  ├─ __init__.py
│  └─ test_case_processor.py
│
├─ requirements.txt
├─ README.md
