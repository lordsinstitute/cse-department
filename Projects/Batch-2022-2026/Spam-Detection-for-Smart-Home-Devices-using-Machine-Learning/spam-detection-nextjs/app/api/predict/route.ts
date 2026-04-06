import { NextRequest, NextResponse } from 'next/server';
import axios from 'axios';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { parameters } = body;

    if (!parameters || !Array.isArray(parameters) || parameters.length !== 10) {
      return NextResponse.json(
        { error: 'Invalid parameters. Must provide an array of 10 numeric values.' },
        { status: 400 }
      );
    }

    // In production, this would call the Flask backend
    // For now, we'll simulate with a random result or connect to the existing backend
    
    try {
      // Connect to the Flask backend
      const response = await axios.post('http://localhost:5020/predict', {
        p0: parameters[0],
        p1: parameters[1],
        p2: parameters[2],
        p3: parameters[3],
        p4: parameters[4],
        p5: parameters[5],
        p6: parameters[6],
        p7: parameters[7],
        p8: parameters[8],
        p9: parameters[9],
      }, {
        headers: { 'Content-Type': 'application/json' }
      });

      return NextResponse.json({ prediction: response.data.pred });
    } catch (error) {
      console.error('Could not connect to Flask backend:', error);
      return NextResponse.json(
        { error: 'Flask backend is unavailable. Please ensure the backend is running on port 5020.' },
        { status: 503 }
      );
    }
  } catch (error) {
    console.error('Error in prediction API:', error);
    return NextResponse.json(
      { error: 'An error occurred during prediction' },
      { status: 500 }
    );
  }
} 