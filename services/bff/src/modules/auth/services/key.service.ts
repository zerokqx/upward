import { Injectable, Logger } from '@nestjs/common';
import { getAuth } from '../../../shared/api/orval/identify-service/auth/auth.js';

@Injectable()
export class KeyService {
  private readonly logger = new Logger(KeyService.name);
  private cachedKey: string | null = null;
  private pendingPromise: Promise<string> | null = null;

  /**
   * Лениво получает открытый ключ RSA от сервиса identify.
   * Ключ кэшируется в памяти, предотвращая повторные запросы.
   */
  async getPublicKey(): Promise<string> {
    if (this.cachedKey) {
      return this.cachedKey;
    }

    if (!this.pendingPromise) {
      this.pendingPromise = this.fetchKey();
    }

    try {
      return await this.pendingPromise;
    } finally {
      this.pendingPromise = null;
    }
  }

  private async fetchKey(): Promise<string> {
    try {
      this.logger.log('Запрос открытого ключа (RSA Public Key) из identify-service...');
      const auth = getAuth();
      const response = await auth.getPublicKey();

      if (!response.public_key) {
        throw new Error('Публичный ключ отсутствует в ответе identify-service');
      }

      this.cachedKey = response.public_key.trim();
      this.logger.log('Открытый ключ успешно получен и сохранён в кэш');
      return this.cachedKey;
    } catch (error) {
      this.logger.error('Не удалось получить открытый ключ от identify-service', error);
      throw error;
    }
  }

  /**
   * Сбросить кэш открытого ключа (например, при ротации ключей)
   */
  clearCache(): void {
    this.cachedKey = null;
  }
}
