import pandas as pd
from models.data_model import SensorData

def preprocess_file(file_path: str, tags: Dict):
    """
    Read, validate, and preprocess the downloaded file.
    """
    # Load Excel into a DataFrame
    df = pd.read_excel(file_path)

    # Convert to dictionary for validation
    validated_data = []
    for measurement, variables in tags.items():
        data = {
            "timestamp": pd.Timestamp.now(),
            "measurement": measurement,
            "values": {var: df[var].iloc[0] for var in variables if var in df.columns}
        }
        validated_data.append(SensorData.validate_data(data))
    return validated_data
