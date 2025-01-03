import io
import csv
import json
import os

from fastapi import FastAPI, UploadFile, HTTPException
from google.cloud import pubsub_v1

app = FastAPI()


# Set up Google Pub/Sub client
PROJECT_ID = "berat-test"
TOPIC_ID = "users-read-data"
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)
print(topic_path)
@app.post("/process_csv/")
async def process_csv(file: UploadFile):
    # Step 1: Check file type
    if file.content_type != "text/csv":
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV file.")

    try:
        # Step 2: Read the CSV data
        content = await file.read()
        csv_data = io.StringIO(content.decode("utf-8"))
        reader = csv.DictReader(csv_data)

        # Step 3: Convert CSV to JSON
        data_list = [row for row in reader]
        json_data = json.dumps(data_list)

        # Step 4: Send JSON to Pub/Sub
        future = publisher.publish(topic_path, json_data.encode("utf-8"))
        message_id = future.result()

        return {"message": "CSV processed and sent to Pub/Sub", "message_id": message_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/test")
async def test():
    # Create the Protobuf message
    user = User('22',"Berat Yesbek","berat.yesbek@test.com")
    message_data = user.serialize()

    future = publisher.publish(topic_path, message_data)
    message_id = future.result()

    return {"message": "Test completed successfully", "message_id": message_id}
@app.get("/")
async def test():
    return {"message": "hiiii"}

class User:
    def __init__(self, id: str, name: str, email: str):
        self.id = id
        self.name = name
        self.email = email

    def serialize(self) -> bytes:
        """
        Serialize the User instance to a JSON byte string.
        """
        return json.dumps({
            "id": self.id,
            "name": self.name,
            "email": self.email
        }).encode("utf-8")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)