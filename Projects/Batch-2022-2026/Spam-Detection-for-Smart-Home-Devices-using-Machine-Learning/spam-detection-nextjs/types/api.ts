export interface ApiResponse<T> {
  status: 'success' | 'error';
  data?: T;
  message?: string;
  code?: string;
}

export interface LoginResponse {
  access_token: string;
  role: 'admin' | 'user';
}

export interface PredictionResult {
  prediction: 0 | 1;
  label: 'spam' | 'valid';
  prediction_id: number;
}

export interface BatchPredictionResult {
  results: Array<{
    index?: number;
    row?: number;
    prediction: 0 | 1;
    label: 'spam' | 'valid';
    prediction_id: number;
  }>;
  total: number;
  spam_count: number;
  valid_count: number;
}

export interface AlgorithmMetrics {
  name: string;
  accuracy: number;
  precision: number;
  recall: number;
  fscore: number;
}

export interface ModelVersion {
  id: number;
  version: string;
  accuracy: number;
  trained_at: string;
  is_active: boolean;
  algorithm_metrics: AlgorithmMetrics[] | null;
}

export interface Dataset {
  id: number;
  filename: string;
  row_count: number | null;
  upload_time: string;
  is_active: boolean;
}

export interface DashboardData {
  total_predictions: number;
  active_model: ModelVersion | null;
  active_dataset: Dataset | null;
}

export interface PredictionHistory {
  id: number;
  parameters: number[];
  result: 0 | 1;
  label: 'spam' | 'valid';
  source: string;
  created_at: string;
}
