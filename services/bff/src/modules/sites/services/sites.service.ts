import { Injectable, Logger } from '@nestjs/common';
import { getSites } from '../../../shared/api/orval/uptime-service/sites/sites.js';
import { getPings } from '../../../shared/api/orval/uptime-service/pings/pings.js';
import type {
  CreateSiteResponseDto,
  SiteResponseDto,
  VerifySiteResponseDto,
  PingRecord,
} from '../../../shared/api/orval/uptime-service/uptime-service.schemas.js';
import { handleUpstreamError } from '../../../shared/utils/axios-error.js';

@Injectable()
export class SitesService {
  private readonly logger = new Logger(SitesService.name);
  private readonly sitesClient = getSites();
  private readonly pingsClient = getPings();

  async createSite(
    userId: string,
    url: string,
    rawToken: string,
  ): Promise<CreateSiteResponseDto> {
    try {
      return await this.sitesClient.createSite(
        { site: url, user_id: userId },
        {
          headers: {
            Authorization: `Bearer ${rawToken}`,
          },
        },
      );
    } catch (error) {
      this.logger.error(`Error creating site for user ${userId}:`, error);
      handleUpstreamError(error, 'uptime-service');
    }
  }

  async getAllSites(
    userId: string,
    rawToken: string,
  ): Promise<SiteResponseDto[]> {
    try {
      return await this.sitesClient.getAllSites(userId, {
        headers: {
          Authorization: `Bearer ${rawToken}`,
        },
      });
    } catch (error) {
      this.logger.error(`Error fetching sites for user ${userId}:`, error);
      handleUpstreamError(error, 'uptime-service');
    }
  }

  async verifySite(
    siteId: string,
    rawToken: string,
  ): Promise<VerifySiteResponseDto> {
    try {
      return await this.sitesClient.verifySite(siteId, {
        headers: {
          Authorization: `Bearer ${rawToken}`,
        },
      });
    } catch (error) {
      this.logger.error(`Error verifying site ${siteId}:`, error);
      handleUpstreamError(error, 'uptime-service');
    }
  }

  async getPings(
    siteId: string,
    userId: string,
    rawToken: string,
  ): Promise<PingRecord[]> {
    try {
      return await this.pingsClient.getPings(
        siteId,
        { user_id: userId },
        {
          headers: {
            Authorization: `Bearer ${rawToken}`,
          },
        },
      );
    } catch (error) {
      this.logger.error(`Error fetching pings for site ${siteId}:`, error);
      handleUpstreamError(error, 'uptime-service');
    }
  }
}
