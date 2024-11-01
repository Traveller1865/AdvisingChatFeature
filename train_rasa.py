import os
import subprocess

def train_model():
    try:
        # Set the output directory for the model
        model_directory = "rasa_bot/models"

        # Create the model directory if it doesn't exist
        os.makedirs(model_directory, exist_ok=True)

        # Train the full Rasa model (NLU + Core)
        command = ["rasa", "train", "--config", "rasa_bot/config.yml", "--domain", "rasa_bot/domain.yml", "--data", "rasa_bot/data", "--out", "rasa_bot/models"]
        subprocess.run(command, check=True)
        print("Rasa model training completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error training Rasa model: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    train_model()
