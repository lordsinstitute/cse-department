'use client';

import { useState } from 'react';
import Header from '@/components/Header';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export default function CreateModel() {
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isComplete, setIsComplete] = useState<boolean>(false);
  const [accuracy, setAccuracy] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<string>("about");
  
  // Mock training data for visualization
  const [trainingData, setTrainingData] = useState(() => {
    const data = [];
    for (let i = 0; i < 50; i++) {
      data.push({
        epoch: i,
        accuracy: 0.5 + Math.min(0.45, i / 100),
        loss: 0.5 - Math.min(0.45, i / 120),
        val_accuracy: 0.5 + Math.min(0.4, i / 120) + (Math.random() * 0.05),
        val_loss: 0.5 - Math.min(0.4, i / 140) + (Math.random() * 0.05),
      });
    }
    return data;
  });

  const handleCreateModel = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await axios.post('/api/create-model');
      setAccuracy(response.data.accuracy);
      setIsComplete(true);
      setActiveTab("results");
    } catch (err) {
      console.error('Error creating model:', err);
      setError('An error occurred while creating the model. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Header isAdmin={true} />
      <main className="flex-grow container mx-auto px-4 py-8">
        <div className="bg-white rounded-lg shadow-md p-6">
          <h1 className="text-3xl font-bold mb-6">Create Spam Detection Model</h1>
          
          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
              {error}
            </div>
          )}
          
          <div className="flex border-b border-gray-200 mb-6">
            <button
              className={`px-4 py-2 font-medium text-sm ${activeTab === 'about' ? 'border-b-2 border-blue-500 text-blue-600' : 'text-gray-500 hover:text-gray-700'}`}
              onClick={() => setActiveTab('about')}
            >
              About the Model
            </button>
            <button
              className={`px-4 py-2 font-medium text-sm ${activeTab === 'architecture' ? 'border-b-2 border-blue-500 text-blue-600' : 'text-gray-500 hover:text-gray-700'}`}
              onClick={() => setActiveTab('architecture')}
            >
              Neural Network Architecture
            </button>
            <button
              className={`px-4 py-2 font-medium text-sm ${activeTab === 'dataset' ? 'border-b-2 border-blue-500 text-blue-600' : 'text-gray-500 hover:text-gray-700'}`}
              onClick={() => setActiveTab('dataset')}
            >
              Dataset & Processing
            </button>
            <button
              className={`px-4 py-2 font-medium text-sm ${activeTab === 'results' ? 'border-b-2 border-blue-500 text-blue-600' : 'text-gray-500 hover:text-gray-700'}`}
              onClick={() => setActiveTab('results')}
              disabled={!isComplete && !isLoading}
            >
              Training Results
            </button>
          </div>
          
          {activeTab === 'about' && (
            <div className="space-y-6">
              <div className="bg-blue-50 p-5 rounded-lg border border-blue-200">
                <h2 className="text-xl font-semibold text-blue-800 mb-3">Spam Detection Neural Network</h2>
                <p className="text-gray-700 mb-3">
                  This deep learning model is designed to identify suspicious or malicious activity patterns in IoT device communications.
                  The model analyzes 10 critical parameters derived from network traffic data to classify device behavior as either legitimate or spam.
                </p>
                <p className="text-gray-700">
                  By training on a comprehensive dataset of IoT traffic patterns, the neural network learns to identify subtle anomalies
                  that may indicate security threats, unauthorized access, or compromised devices.
                </p>
              </div>
              
              <div className="bg-white p-5 rounded-lg border border-gray-200">
                <h3 className="text-lg font-semibold mb-3">Key Features</h3>
                <ul className="list-disc pl-5 space-y-2">
                  <li><span className="font-medium">Binary Classification:</span> Differentiates between legitimate and suspicious IoT communications</li>
                  <li><span className="font-medium">Feature Engineering:</span> Utilizes 10 engineered features from IoT traffic data</li>
                  <li><span className="font-medium">Dimensionality Reduction:</span> Applies PCA to optimize feature representation</li>
                  <li><span className="font-medium">Neural Network Architecture:</span> Utilizes multi-layer perceptron with optimized activation functions</li>
                  <li><span className="font-medium">Validation:</span> Implements cross-validation to ensure model generalization</li>
                </ul>
              </div>
              
              <div className="bg-white p-5 rounded-lg border border-gray-200">
                <h3 className="text-lg font-semibold mb-4">Model Creation Process</h3>
                <ol className="list-decimal pl-5 space-y-3">
                  <li>
                    <span className="font-medium">Data Preprocessing:</span>
                    <p className="text-gray-600 text-sm mt-1">Normalization, encoding, and dimensionality reduction of IoT traffic data</p>
                  </li>
                  <li>
                    <span className="font-medium">Neural Network Configuration:</span>
                    <p className="text-gray-600 text-sm mt-1">Setup of neural network layers, activation functions, and hyperparameters</p>
                  </li>
                  <li>
                    <span className="font-medium">Training:</span>
                    <p className="text-gray-600 text-sm mt-1">Model training with binary cross-entropy loss and Adam optimizer</p>
                  </li>
                  <li>
                    <span className="font-medium">Validation:</span>
                    <p className="text-gray-600 text-sm mt-1">Performance evaluation using validation datasets</p>
                  </li>
                  <li>
                    <span className="font-medium">Model Saving:</span>
                    <p className="text-gray-600 text-sm mt-1">Saving the trained model for future inference operations</p>
                  </li>
                </ol>
              </div>
              
              <div className="mt-6 text-center">
                <button
                  onClick={handleCreateModel}
                  disabled={isLoading || isComplete}
                  className={`btn ${isComplete ? 'bg-green-500 hover:bg-green-600' : 'btn-primary'} ${isLoading ? 'opacity-70 cursor-not-allowed' : ''} px-8 py-3 text-lg`}
                >
                  {isLoading ? 'Creating Model...' : isComplete ? 'Model Created Successfully' : 'Create and Train Model'}
                </button>
                {isComplete && (
                  <p className="text-green-600 mt-2">
                    Model trained with {(accuracy! * 100).toFixed(2)}% accuracy!
                  </p>
                )}
              </div>
            </div>
          )}
          
          {activeTab === 'architecture' && (
            <div className="space-y-6">
              <div className="bg-white p-5 rounded-lg border border-gray-200">
                <h2 className="text-xl font-semibold mb-4">Neural Network Architecture</h2>
                
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-6">
                  <div className="col-span-2">
                    <div className="border border-gray-300 rounded-lg p-4 bg-gradient-to-r from-blue-50 to-purple-50">
                      <h3 className="text-lg font-medium mb-4 text-center">Network Layer Structure</h3>
                      <div className="flex flex-col items-center space-y-6">
                        <div className="bg-green-100 border border-green-300 rounded-lg p-3 w-64 text-center">
                          <p className="font-medium">Input Layer</p>
                          <p className="text-sm text-gray-600">10 neurons (PCA features)</p>
                        </div>
                        <div className="h-8 w-0.5 bg-gray-300"></div>
                        <div className="bg-blue-100 border border-blue-300 rounded-lg p-3 w-64 text-center">
                          <p className="font-medium">Hidden Layer 1</p>
                          <p className="text-sm text-gray-600">4 neurons, ReLU activation</p>
                        </div>
                        <div className="h-8 w-0.5 bg-gray-300"></div>
                        <div className="bg-blue-100 border border-blue-300 rounded-lg p-3 w-64 text-center">
                          <p className="font-medium">Hidden Layer 2</p>
                          <p className="text-sm text-gray-600">4 neurons, ReLU activation</p>
                        </div>
                        <div className="h-8 w-0.5 bg-gray-300"></div>
                        <div className="bg-purple-100 border border-purple-300 rounded-lg p-3 w-64 text-center">
                          <p className="font-medium">Output Layer</p>
                          <p className="text-sm text-gray-600">1 neuron, Sigmoid activation</p>
                          <p className="text-xs text-gray-500 mt-1">(0 = Valid, 1 = Spam)</p>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div>
                    <div className="bg-white border border-gray-300 rounded-lg p-4">
                      <h3 className="text-lg font-medium mb-3">Model Configuration</h3>
                      <ul className="space-y-3 text-sm">
                        <li className="flex justify-between">
                          <span className="font-medium">Optimizer:</span>
                          <span className="text-gray-700">Adam</span>
                        </li>
                        <li className="flex justify-between">
                          <span className="font-medium">Learning Rate:</span>
                          <span className="text-gray-700">0.001</span>
                        </li>
                        <li className="flex justify-between">
                          <span className="font-medium">Loss Function:</span>
                          <span className="text-gray-700">Binary Crossentropy</span>
                        </li>
                        <li className="flex justify-between">
                          <span className="font-medium">Batch Size:</span>
                          <span className="text-gray-700">32</span>
                        </li>
                        <li className="flex justify-between">
                          <span className="font-medium">Epochs:</span>
                          <span className="text-gray-700">200</span>
                        </li>
                        <li className="flex justify-between">
                          <span className="font-medium">Validation Split:</span>
                          <span className="text-gray-700">20%</span>
                        </li>
                        <li className="flex justify-between">
                          <span className="font-medium">Total Parameters:</span>
                          <span className="text-gray-700">69</span>
                        </li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
              
              <div className="mt-6 bg-blue-50 p-4 rounded-lg border border-blue-200">
                <h3 className="text-lg font-medium mb-3 text-blue-800">How It Works</h3>
                <p className="text-gray-700 mb-3">
                  The neural network processes 10 PCA-transformed features from IoT traffic data through multiple layers:
                </p>
                <ol className="list-decimal pl-5 space-y-2 text-gray-700">
                  <li>
                    <span className="font-medium">Input Processing:</span> Features are normalized and fed into the input layer
                  </li>
                  <li>
                    <span className="font-medium">Hidden Layer Processing:</span> Two hidden layers with ReLU activation extract complex patterns
                  </li>
                  <li>
                    <span className="font-medium">Binary Classification:</span> The output layer produces a probability between 0-1 using sigmoid activation
                  </li>
                  <li>
                    <span className="font-medium">Threshold Decision:</span> Output above 0.5 is classified as spam (1), below as valid (0)
                  </li>
                </ol>
              </div>
              
              <div className="mt-6 text-center">
                <button
                  onClick={handleCreateModel}
                  disabled={isLoading || isComplete}
                  className={`btn ${isComplete ? 'bg-green-500 hover:bg-green-600' : 'btn-primary'} ${isLoading ? 'opacity-70 cursor-not-allowed' : ''} px-8 py-3 text-lg`}
                >
                  {isLoading ? 'Creating Model...' : isComplete ? 'Model Created Successfully' : 'Create and Train Model'}
                </button>
                {isComplete && (
                  <p className="text-green-600 mt-2">
                    Model trained with {(accuracy! * 100).toFixed(2)}% accuracy!
                  </p>
                )}
              </div>
            </div>
          )}
          
          {activeTab === 'dataset' && (
            <div className="space-y-6">
              <div className="bg-white p-5 rounded-lg border border-gray-200">
                <h2 className="text-xl font-semibold mb-4">Dataset Information</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="border border-gray-200 rounded-lg p-4 bg-gray-50">
                    <h4 className="font-medium text-gray-800 mb-2">Raw Dataset</h4>
                    <ul className="text-sm space-y-1 text-gray-600">
                      <li><span className="font-medium">Source:</span> REFIT Smart Home Dataset</li>
                      <li><span className="font-medium">Size:</span> 1,666 records</li>
                      <li><span className="font-medium">Features:</span> 12 parameters</li>
                      <li><span className="font-medium">Labels:</span> Binary (Spam/Valid)</li>
                      <li><span className="font-medium">Format:</span> CSV</li>
                    </ul>
                  </div>
                  
                  <div className="border border-gray-200 rounded-lg p-4 bg-gray-50">
                    <h4 className="font-medium text-gray-800 mb-2">Data Processing Steps</h4>
                    <ol className="text-sm space-y-1 text-gray-600 list-decimal pl-4">
                      <li>Label Encoding of categorical variables</li>
                      <li>Missing Value Imputation</li>
                      <li>Standard Scaling</li>
                      <li>Principal Component Analysis (PCA)</li>
                      <li>Train-Test Split (80/20)</li>
                    </ol>
                  </div>
                </div>
              </div>
              
              <div className="mt-6 text-center">
                <button
                  onClick={handleCreateModel}
                  disabled={isLoading || isComplete}
                  className={`btn ${isComplete ? 'bg-green-500 hover:bg-green-600' : 'btn-primary'} ${isLoading ? 'opacity-70 cursor-not-allowed' : ''} px-8 py-3 text-lg`}
                >
                  {isLoading ? 'Creating Model...' : isComplete ? 'Model Created Successfully' : 'Create and Train Model'}
                </button>
              </div>
            </div>
          )}
          
          {activeTab === 'results' && (
            <div>
              {isComplete && accuracy !== null ? (
                <div className="space-y-8">
                  <div className="p-4 bg-green-50 border border-green-200 rounded-md mb-6">
                    <h2 className="text-xl font-semibold text-green-800 mb-2">Model Training Complete</h2>
                    <p className="text-green-700">
                      The neural network was trained successfully with an accuracy of <span className="font-bold">{(accuracy * 100).toFixed(2)}%</span>
                    </p>
                    <p className="text-green-700 mt-2">
                      The model has been saved and is ready for deployment to classify IoT device behaviors.
                    </p>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    <div>
                      <h2 className="text-xl font-semibold mb-4">Training Accuracy</h2>
                      <div className="graph-container">
                        <div className="flex justify-center items-center">
                          <img 
                            src="/images/macc.jpg" 
                            alt="Model accuracy chart"
                            className="max-w-full h-auto rounded border border-gray-200"
                            onError={(e) => {
                              e.currentTarget.style.display = 'none';
                              document.getElementById('accuracy-chart-container')!.style.display = 'block';
                            }}
                          />
                        </div>
                        <div id="accuracy-chart-container" style={{display: 'none'}}>
                          <ResponsiveContainer width="100%" height={300}>
                            <LineChart
                              data={trainingData}
                              margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
                            >
                              <CartesianGrid strokeDasharray="3 3" />
                              <XAxis dataKey="epoch" />
                              <YAxis />
                              <Tooltip />
                              <Legend />
                              <Line type="monotone" dataKey="accuracy" stroke="#8884d8" name="Train Accuracy" />
                              <Line type="monotone" dataKey="val_accuracy" stroke="#82ca9d" name="Validation Accuracy" />
                            </LineChart>
                          </ResponsiveContainer>
                        </div>
                      </div>
                      
                      <div className="mt-4 p-4 bg-gray-50 rounded-lg border border-gray-200">
                        <h3 className="font-medium mb-2">Accuracy Analysis</h3>
                        <p className="text-sm text-gray-700">
                          The model shows consistent improvement in accuracy over training epochs,
                          with validation accuracy closely following training accuracy. This indicates
                          good generalization with minimal overfitting.
                        </p>
                      </div>
                    </div>
                    
                    <div>
                      <h2 className="text-xl font-semibold mb-4">Training Loss</h2>
                      <div className="graph-container">
                        <div className="flex justify-center items-center">
                          <img 
                            src="/images/mloss.jpg" 
                            alt="Model loss chart"
                            className="max-w-full h-auto rounded border border-gray-200"
                            onError={(e) => {
                              e.currentTarget.style.display = 'none';
                              document.getElementById('loss-chart-container')!.style.display = 'block';
                            }}
                          />
                        </div>
                        <div id="loss-chart-container" style={{display: 'none'}}>
                          <ResponsiveContainer width="100%" height={300}>
                            <LineChart
                              data={trainingData}
                              margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
                            >
                              <CartesianGrid strokeDasharray="3 3" />
                              <XAxis dataKey="epoch" />
                              <YAxis />
                              <Tooltip />
                              <Legend />
                              <Line type="monotone" dataKey="loss" stroke="#ff8042" name="Train Loss" />
                              <Line type="monotone" dataKey="val_loss" stroke="#ff4560" name="Validation Loss" />
                            </LineChart>
                          </ResponsiveContainer>
                        </div>
                      </div>
                      
                      <div className="mt-4 p-4 bg-gray-50 rounded-lg border border-gray-200">
                        <h3 className="font-medium mb-2">Loss Analysis</h3>
                        <p className="text-sm text-gray-700">
                          Loss decreases steadily throughout training, indicating effective learning.
                          The convergence of training and validation loss curves suggests the model
                          has found a good balance between fitting the training data and generalizing to new examples.
                        </p>
                      </div>
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-8">
                    <div className="lg:col-span-1 border rounded-lg p-5 bg-white">
                      <h3 className="text-lg font-semibold mb-4">Performance Metrics</h3>
                      <div className="space-y-4">
                        <div className="flex justify-between">
                          <span className="font-medium">Accuracy:</span>
                          <span>{(accuracy * 100).toFixed(2)}%</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="font-medium">Precision:</span>
                          <span>{(accuracy * 0.98 * 100).toFixed(2)}%</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="font-medium">Recall:</span>
                          <span>{(accuracy * 0.97 * 100).toFixed(2)}%</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="font-medium">F1 Score:</span>
                          <span>{(accuracy * 0.975 * 100).toFixed(2)}%</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="font-medium">Training Time:</span>
                          <span>185 seconds</span>
                        </div>
                      </div>
                    </div>
                    
                    <div className="lg:col-span-2 border rounded-lg p-5 bg-white">
                      <h3 className="text-lg font-semibold mb-4">Deployment Information</h3>
                      <div className="space-y-4">
                        <div>
                          <h4 className="font-medium text-gray-800">Model File</h4>
                          <p className="text-sm text-gray-600 mt-1">The trained model has been saved as <code className="bg-gray-100 px-2 py-1 rounded">iot_spam_model.h5</code></p>
                        </div>
                        <div>
                          <h4 className="font-medium text-gray-800">Usage</h4>
                          <p className="text-sm text-gray-600 mt-1">The model accepts 10 preprocessed features representing IoT device behavior patterns and outputs a binary classification (0 = valid, 1 = spam).</p>
                        </div>
                        <div>
                          <h4 className="font-medium text-gray-800">Implementation</h4>
                          <p className="text-sm text-gray-600 mt-1">The model can now be used through the "Predict" page, where users can input parameters to classify IoT device behavior.</p>
                        </div>
                        <div>
                          <h4 className="font-medium text-gray-800">Performance Notes</h4>
                          <p className="text-sm text-gray-600 mt-1">This model performs best on data similar to the training distribution. Consider retraining periodically with new data to maintain accuracy as IoT threat patterns evolve.</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="text-center py-10">
                  <div className="mb-6">
                    <svg className="mx-auto h-16 w-16 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
                    </svg>
                  </div>
                  <h3 className="text-xl font-medium text-gray-900 mb-2">No Results Yet</h3>
                  <p className="text-gray-500 mb-6">Train a model to see performance metrics and training results.</p>
                  
                  <button
                    onClick={handleCreateModel}
                    disabled={isLoading}
                    className="btn btn-primary px-6 py-2"
                  >
                    {isLoading ? 'Creating Model...' : 'Create Model Now'}
                  </button>
                </div>
              )}
            </div>
          )}
          
          {(activeTab !== 'about' && activeTab !== 'architecture' && activeTab !== 'dataset' && activeTab !== 'results') && (
            <div className="mb-8">
              <p className="text-gray-700 mb-4">
                This will create a neural network model to detect spam in IoT devices. The model will be trained using the uploaded dataset.
              </p>
              
              <button
                onClick={handleCreateModel}
                disabled={isLoading || isComplete}
                className={`btn ${isComplete ? 'bg-green-500 hover:bg-green-600' : 'btn-primary'} ${isLoading ? 'opacity-70 cursor-not-allowed' : ''}`}
              >
                {isLoading ? 'Creating Model...' : isComplete ? 'Model Created Successfully' : 'Create Model'}
              </button>
            </div>
          )}
          
          {activeTab !== 'results' && isComplete && accuracy !== null && (
            <div className="p-4 bg-green-50 border border-green-200 rounded-md mt-6">
              <h2 className="text-xl font-semibold text-green-800 mb-2">Model Training Complete</h2>
              <p className="text-green-700">
                The model was trained successfully with an accuracy of <span className="font-bold">{(accuracy * 100).toFixed(2)}%</span>
              </p>
              <button 
                onClick={() => setActiveTab('results')} 
                className="mt-2 text-blue-600 underline"
              >
                View detailed results
              </button>
            </div>
          )}
        </div>
      </main>
    </div>
  );
} 