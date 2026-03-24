import logging
from typing import Optional, Dict, Any
import json
import time
from datetime import datetime
import os

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class AnalyticsWorker:
    def __init__(self, config_path: Optional[str] = None):
        self.config = self._load_config(config_path)
        self._validate_config()

    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        default_config = {
            "input_dir": "./data/input",
            "output_dir": "./data/output",
            "processing_interval": 60,
            "max_retries": 3
        }

        if not config_path:
            return default_config

        try:
            with open(config_path, 'r') as f:
                return {**default_config, **json.load(f)}
        except FileNotFoundError:
            logger.warning(f"Config file {config_path} not found. Using defaults.")
            return default_config
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in config file {config_path}. Using defaults.")
            return default_config

    def _validate_config(self) -> None:
        if not isinstance(self.config["processing_interval"], int) or self.config["processing_interval"] <= 0:
            raise ValueError("processing_interval must be a positive integer")
        if not isinstance(self.config["max_retries"], int) or self.config["max_retries"] < 0:
            raise ValueError("max_retries must be a non-negative integer")

    def _process_file(self, file_path: str) -> bool:
        try:
            logger.info(f"Processing file: {file_path}")
            # Simulate processing
            time.sleep(1)
            output_path = os.path.join(self.config["output_dir"], os.path.basename(file_path) + ".processed")
            with open(output_path, 'w') as f:
                f.write(f"Processed at {datetime.utcnow().isoformat()}")
            return True
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {str(e)}")
            return False

    def run(self) -> None:
        logger.info("Starting analytics worker")
        while True:
            try:
                files = [f for f in os.listdir(self.config["input_dir"]) if os.path.isfile(os.path.join(self.config["input_dir"], f))]
                for file in files:
                    file_path = os.path.join(self.config["input_dir"], file)
                    retries = 0
                    success = False
                    while not success and retries < self.config["max_retries"]:
                        success = self._process_file(file_path)
                        if not success:
                            retries += 1
                            time.sleep(1)
                time.sleep(self.config["processing_interval"])
            except KeyboardInterrupt:
                logger.info("Shutting down analytics worker")
                break
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
                time.sleep(5)

if __name__ == "__main__":
    worker = AnalyticsWorker()
    worker.run()