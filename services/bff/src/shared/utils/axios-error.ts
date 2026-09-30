import { HttpException, HttpStatus } from '@nestjs/common';
import axios from 'axios';

export function handleUpstreamError(
  error: unknown,
  serviceName: string,
): never {
  if (axios.isAxiosError(error)) {
    if (error.response) {
      const status = error.response.status;
      const data = error.response.data;
      throw new HttpException(data, status);
    }
    throw new HttpException(
      `Микросервис ${serviceName} временно недоступен: ${error.message}`,
      HttpStatus.BAD_GATEWAY,
    );
  }
  throw error;
}
