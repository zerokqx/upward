import { Injectable } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { PassportStrategy } from '@nestjs/passport';
import {
  Strategy,
  type Profile,
  type VerifyCallback,
} from 'passport-google-oauth20';

export interface GoogleUser {
  provider: 'google';
  providerId: string;
  email?: string;
  name: string;
  picture?: string;
  accessToken: string;
}

@Injectable()
export class GoogleStrategy extends PassportStrategy(Strategy, 'google') {
  constructor(configService: ConfigService) {
    super({
      clientID: configService.get<string>(
        'GOOGLE_CLIENT_ID',
        'placeholder-google-client-id',
      ),
      clientSecret: configService.get<string>(
        'GOOGLE_CLIENT_SECRET',
        'placeholder-google-client-secret',
      ),
      callbackURL: configService.get<string>(
        'GOOGLE_CALLBACK_URL',
        'http://localhost:4000/auth/google/callback',
      ),
      scope: ['email', 'profile'],
    });
  }

  validate(
    accessToken: string,
    _refreshToken: string,
    profile: Profile,
    done: VerifyCallback,
  ): void {
    const { id, name, emails, photos } = profile;
    const user: GoogleUser = {
      provider: 'google',
      providerId: id,
      email: emails?.[0]?.value,
      name: `${name?.givenName ?? ''} ${name?.familyName ?? ''}`.trim(),
      picture: photos?.[0]?.value,
      accessToken,
    };
    done(null, user);
  }
}
