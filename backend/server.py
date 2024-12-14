from flask import Flask, request, jsonify
import random  # Simulating predictions for now
import torch
import numpy as np
import matplotlib.pyplot as plt
from torch import nn
from model import getModel
from flask_cors import CORS
from io import BytesIO
import base64
app = Flask(__name__)
CORS(app)



def generateRandomSample():
    '''
    This function will generate random signal with shape <1,1,22,1001>
    '''
    n_samples = 1  # We want to generate a single sample
    n_channels = 22  # 22 EEG channels
    n_timepoints = 1001  # Time points

    # Randomly generate EEG data (values typically in the range of -100 to 100 µV)
    randomSample = np.random.randn(n_samples, 1, n_channels, n_timepoints).astype(np.float32)  # Single channel, 22 channels, 1001 time points

    # Convert the random sample to a PyTorch tensor
    randomSampleTensor = torch.from_numpy(randomSample)
    return randomSampleTensor


    
    

@app.route('/predict', methods=['POST'])
def predict():
    randomSample = generateRandomSample()
    model = getModel()
    output = model(randomSample)
    _, predictClass = torch.max(output,dim=1)
    print(f"PredictClass: {predictClass}")
    resultDict = {
        0: "left hand",
        1: "right hand",
        2: "foot",
        3: "tongue"
    }
    res = predictClass.item()
    
    # plot image:
    # Generate the random sample
    sample = generateRandomSample()
    eeg_data = sample.squeeze().numpy()  # Extract data shape (22, 1001)
    eeg_signals = [
    "EEG-Fz", "EEG", "EEG", "EEG", "EEG", "EEG", "EEG", "EEG-C3", 
    "EEG", "EEG-Cz", "EEG", "EEG-C4", "EEG", "EEG", "EEG", "EEG", 
    "EEG", "EEG", "EEG", "EEG", "EEG-Pz", "EEG"
    ]

    # Create a mapping from 1 to 22 to the EEG signals
    eeg_mapping = {i + 1: eeg_signals[i] for i in range(22)}
    
    # Create the plot
    plt.figure(figsize=(15, 20))
    for channel in range(eeg_data.shape[0]):
        plt.subplot(11, 2, channel + 1)
        plt.plot(eeg_data[channel])
        plt.title(f'Channel {eeg_mapping[channel + 1]}')
        plt.xlabel('Time Points')
        plt.ylabel('Amplitude (µV)')
        plt.tight_layout()

    # Save the plot to a BytesIO object
    img_bytes = BytesIO()
    plt.savefig(img_bytes, format='png')
    img_bytes.seek(0)
    plt.close()  # Free up memory

    # Option 1: Send as file
    # return send_file(img_bytes, mimetype='image/png')

    # Option 2: Send as Base64
    img_base64 = base64.b64encode(img_bytes.read()).decode('utf-8')
    
    
    return jsonify({'predicted_class': resultDict[res], 'image': img_base64})

if __name__ == '__main__':
    app.run(debug=True)
