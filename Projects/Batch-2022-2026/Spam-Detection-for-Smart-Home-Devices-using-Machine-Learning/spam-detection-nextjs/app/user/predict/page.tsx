'use client';

import { useState } from 'react';
import Header from '@/components/Header';
import axios from 'axios';

// Define IoT parameters with descriptions
const IOT_PARAMETERS = [
  {
    id: 0,
    name: 'Source ID Encoding',
    description: 'Encoded identifier of the IoT device source',
    range: '[-5.0, 5.0]'
  },
  {
    id: 1,
    name: 'Source Address Type',
    description: 'Encoded classification of source address pattern',
    range: '[-2.0, 2.0]'
  },
  {
    id: 2,
    name: 'Source Type Factor',
    description: 'Numerical representation of device type category',
    range: '[-3.0, 3.0]'
  },
  {
    id: 3,
    name: 'Location Factor',
    description: 'Spatial position encoding of the device',
    range: '[-2.0, 2.0]'
  },
  {
    id: 4,
    name: 'Destination Service Pattern',
    description: 'Encoded pattern of services being accessed',
    range: '[-1.0, 1.0]'
  },
  {
    id: 5,
    name: 'Service Type Classification',
    description: 'Category of service being requested',
    range: '[-1.0, 1.0]'
  },
  {
    id: 6,
    name: 'Operation Behavior',
    description: 'Encoded pattern of operation characteristics',
    range: '[-2.0, 2.0]'
  },
  {
    id: 7,
    name: 'Time Pattern',
    description: 'Temporal pattern of requests',
    range: '[-0.5, 0.5]'
  },
  {
    id: 8,
    name: 'Access Frequency',
    description: 'Rate of access requests normalized',
    range: '[-0.5, 0.5]'
  },
  {
    id: 9,
    name: 'Data Volume Factor',
    description: 'Normalized measure of data volume in requests',
    range: '[-0.5, 0.5]'
  }
];

export default function PredictPage() {
  const [parameters, setParameters] = useState<number[]>(Array(10).fill(0));
  const [result, setResult] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (index: number, value: string) => {
    const newParameters = [...parameters];
    newParameters[index] = parseFloat(value) || 0;
    setParameters(newParameters);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    
    try {
      // Call the prediction API
      const response = await axios.post('/api/predict', { parameters });
      setResult(response.data.prediction);
    } catch (err) {
      console.error('Error predicting:', err);
      setError('An error occurred while making the prediction. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleRandom = () => {
    // Generate random reasonable values based on provided ranges
    const randomParams = IOT_PARAMETERS.map(param => {
      const rangeStr = param.range;
      const matches = rangeStr.match(/\[(.*),\s*(.*)\]/);
      if (matches) {
        const min = parseFloat(matches[1]);
        const max = parseFloat(matches[2]);
        return Number((Math.random() * (max - min) + min).toFixed(6));
      }
      return 0;
    });
    setParameters(randomParams);
  };

  const handleResetForm = () => {
    setParameters(Array(10).fill(0));
    setResult(null);
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Header isUser={true} />
      <main className="flex-grow container mx-auto px-4 py-8">
        <div className="max-w-5xl mx-auto bg-white rounded-lg shadow-md p-8">
          <h1 className="text-3xl font-bold mb-6">IoT Device Spam Detection</h1>
          
          <div className="mb-6 bg-blue-50 p-4 rounded-lg border border-blue-200">
            <h2 className="text-lg font-semibold text-blue-800 mb-2">What is IoT Spam?</h2>
            <p className="text-gray-700">
              IoT spam refers to unauthorized or malicious communication patterns from Internet of Things devices. 
              By analyzing the network behavior and communication patterns using the parameters below, our machine 
              learning model can identify potentially compromised or misbehaving devices.
            </p>
          </div>
          
          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
              {error}
            </div>
          )}
          
          <form onSubmit={handleSubmit} className="mb-8">
            <div className="flex justify-end space-x-4 mb-4">
              <button
                type="button"
                onClick={handleRandom}
                className="btn bg-gray-500 text-white hover:bg-gray-600"
              >
                Generate Random Values
              </button>
              <button
                type="button"
                onClick={handleResetForm}
                className="btn bg-gray-300 text-gray-800 hover:bg-gray-400"
              >
                Reset Form
              </button>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {IOT_PARAMETERS.map((param, index) => (
                <div key={index} className="parameter-input">
                  <label htmlFor={`param-${index}`} className="label">
                    {param.name}
                  </label>
                  <p className="description mb-2">{param.description}</p>
                  <p className="text-xs text-gray-500 mb-2">Suggested range: {param.range}</p>
                  <input
                    type="number"
                    id={`param-${index}`}
                    name={`p${index}`}
                    value={parameters[index]}
                    onChange={(e) => handleChange(index, e.target.value)}
                    step="any"
                    className="input-field"
                    required
                  />
                </div>
              ))}
            </div>
            
            <div className="mt-6 flex justify-center">
              <button
                type="submit"
                className="btn btn-primary text-lg px-8 py-3"
                disabled={isLoading}
              >
                {isLoading ? 'Analyzing...' : 'Analyze Device Behavior'}
              </button>
            </div>
          </form>
          
          {result !== null && (
            <div className="mt-8 p-6 border rounded-lg bg-gray-50">
              <h2 className="text-2xl font-semibold mb-4">Analysis Result</h2>
              {result === 1 ? (
                <div className="p-5 bg-red-100 text-red-800 rounded-md border-l-4 border-red-500">
                  <div className="flex items-center">
                    <svg className="w-8 h-8 mr-3 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
                    </svg>
                    <h3 className="text-xl font-bold">SPAM DETECTED!</h3>
                  </div>
                  <p className="mt-3">The IoT device behavior is classified as suspicious. This may indicate:</p>
                  <ul className="list-disc ml-8 mt-2 space-y-1">
                    <li>Unauthorized access attempts</li>
                    <li>Compromised device behavior</li>
                    <li>Botnet participation</li>
                    <li>Data exfiltration attempts</li>
                  </ul>
                  <p className="mt-3 font-medium">Recommendation: Isolate this device and investigate further.</p>
                </div>
              ) : (
                <div className="p-5 bg-green-100 text-green-800 rounded-md border-l-4 border-green-500">
                  <div className="flex items-center">
                    <svg className="w-8 h-8 mr-3 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                    <h3 className="text-xl font-bold">VALID BEHAVIOR</h3>
                  </div>
                  <p className="mt-3">The IoT device behavior is classified as normal and legitimate.</p>
                  <p className="mt-2">The communication patterns are consistent with expected behavior for this device type.</p>
                  <p className="mt-3 font-medium">Recommendation: No action required. Continue monitoring.</p>
                </div>
              )}
            </div>
          )}
        </div>
      </main>
    </div>
  );
} 