import { Injectable, UnauthorizedException } from '@nestjs/common';
import { PassportStrategy } from '@nestjs/passport';
import { ExtractJwt, Strategy } from 'passport-jwt';
import { KeyService } from '../services/key.service.js';

export interface JwtPayload {
  sub: string;
  email: string;
  iat: number;
  exp: number;
}

export interface AuthenticatedUser {
  id: string;
  email: string;
}

@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy, 'jwt') {
  constructor(private readonly keyService: KeyService) {
    super({
      jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
      ignoreExpiration: false,
      algorithms: ['RS256'],
      secretOrKeyProvider: async (_request, _rawJwtToken, done) => {
        try {
          const key = await this.keyService.getPublicKey();
          done(null, key);
        } catch (err) {
          done(err as Error, undefined);
        }
      },
    });
  }

  validate(payload: JwtPayload): AuthenticatedUser {
    if (!payload?.sub) {
      throw new UnauthorizedException(
        'Невалидный токен: отсутствует идентификатор пользователя (sub)',
      );
    }
    return {
      id: payload.sub,
      email: payload.email,
    };
  }
}
