/**
 * Global Error Handler
 * Handles API errors and provides user-friendly messages
 */

export interface ApiError {
  message: string;
  status?: number;
  code?: string;
  details?: any;
}

interface ApiErrorResponse {
  response?: {
    status: number;
    statusText: string;
    data: any;
  };
  request?: any;
  message?: string;
  code?: string;
}

/**
 * Extract error message from API response
 */
export function getErrorMessage(error: unknown): string {
  const apiError = error as ApiErrorResponse;
  
  // Server responded with error
  if (apiError.response) {
    const data = apiError.response.data;
      
      // FastAPI error format
      if (data?.detail) {
        if (typeof data.detail === 'string') {
          return data.detail;
        }
        if (Array.isArray(data.detail)) {
          return data.detail.map((d: any) => d.msg).join(', ');
        }
      }

      // Generic error message
      if (data?.message) {
        return data.message;
      }

      // HTTP status messages
      switch (apiError.response.status) {
        case 400:
          return 'Requisição inválida. Verifique os dados enviados.';
        case 401:
          return 'Não autorizado. Faça login novamente.';
        case 403:
          return 'Acesso negado. Você não tem permissão para esta ação.';
        case 404:
          return 'Recurso não encontrado.';
        case 409:
          return 'Conflito. O recurso já existe.';
        case 422:
          return 'Dados inválidos. Verifique os campos do formulário.';
        case 500:
          return 'Erro interno do servidor. Tente novamente mais tarde.';
        case 503:
          return 'Serviço temporariamente indisponível. Tente novamente.';
        default:
          return `Erro ${apiError.response.status}: ${apiError.response.statusText}`;
      }
    }

  // Network error
  if (apiError.request) {
    return 'Erro de conexão. Verifique sua internet e tente novamente.';
  }

  // Request setup error
  if (apiError.message) {
    return apiError.message;
  }

  // Generic error
  if (error instanceof Error) {
    return error.message;
  }

  return 'Erro desconhecido. Tente novamente.';
}

/**
 * Parse API error into structured format
 */
export function parseApiError(error: unknown): ApiError {
  const apiError = error as ApiErrorResponse;
  
  return {
    message: getErrorMessage(error),
    status: apiError.response?.status,
    code: apiError.code,
    details: apiError.response?.data,
  };
}

/**
 * Log error to console (development) or external service (production)
 */
export function logError(error: unknown, context?: string) {
  const apiError = parseApiError(error);

  if (import.meta.env.DEV) {
    console.error(`[Error${context ? ` - ${context}` : ''}]:`, {
      message: apiError.message,
      status: apiError.status,
      code: apiError.code,
      details: apiError.details,
      originalError: error,
    });
  }

  if (import.meta.env.PROD) {
    // TODO: Send to error tracking service (e.g., Sentry)
    // sendToErrorTracking(apiError, context);
  }
}

/**
 * Handle error and show user notification
 */
export function handleError(error: unknown, context?: string): ApiError {
  const apiError = parseApiError(error);
  logError(error, context);

  // Show toast notification (if toast library is available)
  // toast.error(apiError.message);

  return apiError;
}

/**
 * Check if error is authentication error
 */
export function isAuthError(error: unknown): boolean {
  const apiError = error as ApiErrorResponse;
  return apiError.response?.status === 401;
}

/**
 * Check if error is network error
 */
export function isNetworkError(error: unknown): boolean {
  const apiError = error as ApiErrorResponse;
  return !apiError.response && !!apiError.request;
}

/**
 * Check if error is validation error
 */
export function isValidationError(error: unknown): boolean {
  const apiError = error as ApiErrorResponse;
  return apiError.response?.status === 422 || apiError.response?.status === 400;
}

/**
 * Retry function with exponential backoff
 */
export async function retryWithBackoff<T>(
  fn: () => Promise<T>,
  maxRetries: number = 3,
  baseDelay: number = 1000
): Promise<T> {
  let lastError: unknown;

  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;

      // Don't retry on client errors (4xx)
      const apiError = error as ApiErrorResponse;
      if (apiError.response?.status && apiError.response.status < 500) {
        throw error;
      }

      // Wait before retrying (exponential backoff)
      if (i < maxRetries - 1) {
        const delay = baseDelay * Math.pow(2, i);
        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }
  }

  throw lastError;
}
