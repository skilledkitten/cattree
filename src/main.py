import time
import socketio
from pymongo import MongoClient

# Function to compute the Collatz sequence for a given number.
def collatz_sequence(n):
    sequence = [n]
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        sequence.append(n)
    return sequence

# Function to generate Collatz data for numbers from 1 upwards.
def generate_collatz_data():
    collatz_tree = {}
    number = 1

    while True:
        sequence = collatz_sequence(number)
        collatz_tree[number] = sequence
        if sequence[-3:] == [4, 2, 1]:
            print(f"Success: Number {number} ends with the sequence [4, 2, 1].")
        
        # Emit data to the WebSocket server
        sio.emit('collatzData', {'_id': number, 'sequence': sequence})

        # Save to MongoDB (optional)
        save_to_mongodb(number, sequence)

        # Increment the number for the next Collatz sequence
        number += 1

        # Sleep to simulate real-time data generation (optional)
        time.sleep(0.5)

# Function to save the Collatz data to MongoDB Atlas.
def save_to_mongodb(number, sequence):
    # MongoDB Atlas connection string (replace <db_password> with your actual password)
    client = MongoClient("mongodb+srv://lucasretzer0:FB3fInnEvvG8xnIz@meow.kihc9.mongodb.net/?retryWrites=true&w=majority&appName=meow")
    db = client['cattree']  # Database name
    collection = db['catdata']  # Collection name

    # Insert document into MongoDB
    collection.update_one(
        {"_id": number},  # Use the number as the unique identifier
        {"$set": {"sequence": sequence}},  # Update the sequence
        upsert=True  # If the document doesn't exist, it will be inserted
    )

    print(f"Collatz data for {number} has been saved to MongoDB.")

# Set up the WebSocket client
sio = socketio.Client()

# Connect to the WebSocket server
@sio.event
def connect():
    print("Connected to the WebSocket server.")

@sio.event
def disconnect():
    print("Disconnected from the WebSocket server.")

# Start the WebSocket server
def start_socket_server():
    sio.connect("http://localhost:3000")  # Adjust to your server URL
    print("WebSocket server is running...")
    generate_collatz_data()

if __name__ == "__main__":
    start_socket_server()
