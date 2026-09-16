# check-digit-format

Reading the VIN from a text file and testing the check digit formatting

## Project Structure

```
check-digit-format/
├── src/
│   ├── vin_reader.py       # Read VIN from a local text file
│   └── vin_validator.py    # Checkdigit format validation
├── tests/
│   ├── fixtures/vins.txt   # Sample input file
│   ├── test_vin_reader.py
│   ├── test_vin_validator.py
│   └── test_integration.py
├── Jenkinsfile
├── pyproject.toml
└── requirements.txt
```

## Run in Local Environment

```bash
python3 -m venv .venv
source .venv/bin/activate 
.venv\Scripts\Activate.ps1   
pip install -r requirements.txt
pytest
python -m pytest
```

## Input file format

```
# Samples
1M8GDM9AXKP042788
1HGCM82633A004352
```

## Validation

- VIN Length must be exactly 17 characters
- Only numbers and uppercase English letters are allowed (except I,Q,O)
- The check digit at the ninth position is validated based on the standard NHTSA algorithm
(To disable this check: `validate_vin(vin, check_digit=False)`)

## An important note about using Jenkins for this project

The `recordCoverage` stage in the Jenkinsfile requires the **Coverage Plugin**.
If it is not installed, either remove that stage from the file or install the plugin via **Manage Jenkins → Plugins**; otherwise, the build will fail at that stage.
