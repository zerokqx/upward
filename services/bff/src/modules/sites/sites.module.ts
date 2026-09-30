import { Module } from '@nestjs/common';
import { SitesController } from './sites.controller.js';
import { SitesService } from './services/sites.service.js';
import { AuthModule } from '../auth/auth.module.js';

@Module({
  imports: [AuthModule],
  controllers: [SitesController],
  providers: [SitesService],
  exports: [SitesService],
})
export class SitesModule {}
