import axios, { AxiosInstance, AxiosResponse } from 'axios';
import { store } from '../store/store';
import { logout } from '../store/authSlice';

interface ApiConfig {
  baseURL: string;
  timeout: number;
}

interface LoginCredentials {
  username: string;
  password: string;
}

interface RegisterCredentials extends LoginCredentials {
  email: string;
}

interface TradeRequest {
  asset: string;
  amount: number;
  type: 'buy' | 'sell';
}

class ApiService {
  private axiosInstance: AxiosInstance;

  constructor(config: ApiConfig) {
    this.axiosInstance = axios.create({
      baseURL: config.baseURL,
      timeout: config.timeout,
      headers: {
        'Content-Type': 'application/json'
      }
    });

    this.setupInterceptors();
  }

  private setupInterceptors() {
    // Request interceptor for adding auth token
    this.axiosInstance.interceptors.request.use(
      config => {
        const token = localStorage.getItem('token');
        if (token) {
          config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
      },
      error => Promise.reject(error)
    );

    // Response interceptor for handling errors
    this.axiosInstance.interceptors.response.use(
      response => response,
      error => {
        if (error.response?.status === 401) {
          // Token expired or invalid
          store.dispatch(logout());
        }
        return Promise.reject(error);
      }
    );
  }

  // Authentication Methods
  async login(credentials: LoginCredentials): Promise<AxiosResponse> {
    return this.axiosInstance.post('/auth/login', credentials);
  }

  async register(credentials: RegisterCredentials): Promise<AxiosResponse> {
    return this.axiosInstance.post('/auth/register', credentials);
  }

  async logout(): Promise<void> {
    await this.axiosInstance.post('/auth/logout');
    localStorage.removeItem('token');
    store.dispatch(logout());
  }

  // Trading Methods
  async getTradingAccounts(): Promise<AxiosResponse> {
    return this.axiosInstance.get('/trading/accounts');
  }

  async executeTrade(tradeRequest: TradeRequest): Promise<AxiosResponse> {
    return this.axiosInstance.post('/trading/trade', tradeRequest);
  }

  async getMarketData(asset: string): Promise<AxiosResponse> {
    return this.axiosInstance.get(`/market/data/${asset}`);
  }

  // Portfolio Methods
  async getPortfolio(): Promise<AxiosResponse> {
    return this.axiosInstance.get('/portfolio');
  }

  // Payment Methods
  async createPaymentRequest(amount: number): Promise<AxiosResponse> {
    return this.axiosInstance.post('/payments/request', { amount });
  }
}

const apiConfig: ApiConfig = {
  baseURL: process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000/api',
  timeout: 10000 // 10 seconds
};

export default new ApiService(apiConfig);
