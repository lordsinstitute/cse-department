# IoT Spam Detection Next.js Application

This is a modern Next.js application that provides a user interface for IoT spam detection, with machine learning model training capabilities.

## Features

- **User Authentication**: Simple login for both admin and user roles
- **Prediction Interface**: Input parameters to detect if an IoT device record is spam or valid
- **Machine Learning Visualization**: Compare different ML algorithms for spam detection
- **Model Training**: Train and create spam detection models
- **Dataset Management**: Upload and manage datasets

## Getting Started

### Prerequisites

- Node.js 18.x or later
- npm or yarn
- Python 3.8+ (for the backend ML service)

### Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd spam-detection-nextjs
```

2. Install dependencies:
```bash
npm install
```

3. Create a `public/uploads` directory for file uploads:
```bash
mkdir -p public/uploads
```

### Development

Run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser to see the application.

### Backend Integration

This Next.js application is designed to work with the existing Flask backend for ML functionality. The backend should be running on `http://localhost:5000`.

If the Flask backend is not available, the application will simulate responses for demonstration purposes.

To start the Flask backend:

```bash
cd ../
python app.py
```

## Usage

1. **Home Page**: Navigate to the homepage to see the application overview
2. **User Login**: Use 'user' for both username and password
3. **Admin Login**: Use 'admin' for both username and password
4. **Prediction**: Input IoT device parameters to predict spam/valid status
5. **Algorithm Comparison**: View performance metrics of different ML algorithms
6. **Model Training**: Create and train new models with uploaded datasets

## Technology Stack

- **Frontend**: Next.js 14, React, TypeScript, Tailwind CSS
- **Data Visualization**: Recharts
- **API Communication**: Axios
- **Backend**: Flask (Python)
- **ML Libraries**: TensorFlow, scikit-learn, Keras, NumPy, Pandas

## Project Structure

- `app/` - Next.js app router pages and API routes
- `components/` - Reusable UI components
- `public/` - Static assets and uploaded files
- `app/api/` - API routes that connect to the Flask backend

## License

This project is licensed under the MIT License. 