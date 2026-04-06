import { NextRequest, NextResponse } from 'next/server';
import axios from 'axios';
import { writeFile } from 'fs/promises';
import { join } from 'path';

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData();
    const file = formData.get('file') as File;

    if (!file) {
      return NextResponse.json(
        { error: 'No file uploaded' },
        { status: 400 }
      );
    }

    // Validate file is a CSV
    if (!file.name.endsWith('.csv')) {
      return NextResponse.json(
        { error: 'Uploaded file must be a CSV file' },
        { status: 400 }
      );
    }

    try {
      // Option 1: Forward to your Flask backend
      // Convert the File to FormData to send to the Flask backend
      const flaskFormData = new FormData();
      flaskFormData.append('file', file);
      
      const response = await axios.post('http://localhost:5000/admin_upload', flaskFormData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      return NextResponse.json({ 
        message: `File ${file.name} uploaded successfully`,
        name: file.name
      });
    } catch (error) {
      console.log('Could not connect to Flask backend, handling file locally');
      
      // Option 2: Handle locally if we can't connect to the Flask backend
      // Save the file to the public directory
      const bytes = await file.arrayBuffer();
      const buffer = Buffer.from(bytes);
      
      // Save to a temporary location in the public directory
      const path = join(process.cwd(), 'public/uploads', file.name);
      await writeFile(path, buffer);
      
      return NextResponse.json({ 
        message: `File ${file.name} uploaded successfully (stored locally)`,
        name: file.name
      });
    }
  } catch (error) {
    console.error('Error in upload API:', error);
    return NextResponse.json(
      { error: 'An error occurred during file upload' },
      { status: 500 }
    );
  }
} 