from rasa.train import train_nlu
import os
import asyncio

async def train_model():
    try:
        # Set the output directory for the model
        model_directory = "rasa_bot/models"
        
        # Create the model directory if it doesn't exist
        os.makedirs(model_directory, exist_ok=True)
        
        # Train the model
        await train_nlu(
            nlu_data="rasa_bot/data/nlu.yml",
            output=model_directory,
            config="rasa_bot/config.yml",
            domain="rasa_bot/domain.yml"
        )
        print("Rasa model training completed successfully!")
    except Exception as e:
        print(f"Error training Rasa model: {str(e)}")

if __name__ == "__main__":
    asyncio.run(train_model())
