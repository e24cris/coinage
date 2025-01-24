import axios from 'axios';

class ApiService {
    constructor() {
        this.baseURL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000';
        this.token = localStorage.getItem('token');
        
        this.axiosInstance = axios.create({
            baseURL: this.baseURL,
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.token}`
            }
        });

        // Interceptor for handling authentication errors
        this.axiosInstance.interceptors.response.use(
            response => response,
            error => {
                if (error.response && error.response.status === 401) {
                    // Token expired or invalid, logout user
                    this.logout();
                }
                return Promise.reject(error);
            }
        );
    }

    // Authentication Methods
    async register(userData) {
        try {
            const response = await this.axiosInstance.post('/auth/register', userData);
            return response.data;
        } catch (error) {
            this.handleError(error);
        }
    }

    async login(credentials) {
        try {
            const response = await this.axiosInstance.post('/auth/login', credentials);
            const { token, user } = response.data;
            
            // Store token and user info
            localStorage.setItem('token', token);
            localStorage.setItem('user', JSON.stringify(user));
            
            return user;
        } catch (error) {
            this.handleError(error);
        }
    }

    logout() {
        try {
            this.axiosInstance.post('/auth/logout');
        } catch (error) {
            console.error('Logout failed', error);
        } finally {
            // Clear local storage
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            window.location.href = '/login';
        }
    }

    // Trading Methods
    async getTradeAccounts() {
        try {
            const response = await this.axiosInstance.get('/trading/accounts');
            return response.data;
        } catch (error) {
            this.handleError(error);
        }
    }

    async executeTrade(tradeData) {
        try {
            const response = await this.axiosInstance.post('/trading/trade', tradeData);
            return response.data;
        } catch (error) {
            this.handleError(error);
        }
    }

    // Payment Methods
    async createPaymentRequest(paymentData) {
        try {
            const response = await this.axiosInstance.post('/payments/request', paymentData);
            return response.data;
        } catch (error) {
            this.handleError(error);
        }
    }

    // Error Handling
    handleError(error) {
        const errorMessage = error.response?.data?.error || 'An unexpected error occurred';
        console.error('API Error:', errorMessage);
        throw new Error(errorMessage);
    }
}

export default new ApiService();
