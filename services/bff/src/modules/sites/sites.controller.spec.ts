import { Test, TestingModule } from '@nestjs/testing';
import { PassportModule } from '@nestjs/passport';
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { SitesController } from './sites.controller.js';
import { SitesService } from './services/sites.service.js';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard.js';

describe('SitesController', () => {
  let controller: SitesController;
  let sitesService: {
    createSite: ReturnType<typeof vi.fn>;
    getAllSites: ReturnType<typeof vi.fn>;
    verifySite: ReturnType<typeof vi.fn>;
    getPings: ReturnType<typeof vi.fn>;
  };

  const mockUser = {
    id: 'usr-123',
    email: 'user@example.com',
  };
  const mockToken = 'mock-bearer-token';

  beforeEach(async () => {
    sitesService = {
      createSite: vi.fn(),
      getAllSites: vi.fn(),
      verifySite: vi.fn(),
      getPings: vi.fn(),
    };

    const module: TestingModule = await Test.createTestingModule({
      imports: [PassportModule.register({ defaultStrategy: 'jwt' })],
      controllers: [SitesController],
      providers: [
        {
          provide: SitesService,
          useValue: sitesService,
        },
      ],
    })
      .overrideGuard(JwtAuthGuard)
      .useValue({ canActivate: () => true })
      .compile();

    controller = module.get<SitesController>(SitesController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });

  describe('createSite', () => {
    it('should forward user.id, site url and rawToken to sitesService', async () => {
      const dto = { site: 'https://example.com' };
      const expectedResponse = {
        id: 'site-uuid',
        status: 'pending_verification',
        challenge_token: 'token-uuid',
        challenge_path: '/upward',
      };
      sitesService.createSite.mockResolvedValue(expectedResponse);

      const result = await controller.createSite(mockUser, mockToken, dto);
      expect(sitesService.createSite).toHaveBeenCalledWith(
        mockUser.id,
        'https://example.com',
        mockToken,
      );
      expect(result).toEqual(expectedResponse);
    });
  });

  describe('getAllSites', () => {
    it('should forward user.id and rawToken to sitesService', async () => {
      const expectedSites = [
        {
          id: 'site-uuid',
          url: 'https://example.com',
          user_id: mockUser.id,
          active: true,
          status: 'idle',
          status_updated_at: '2026-09-30T10:00:00Z',
          created_at: '2026-09-30T10:00:00Z',
        },
      ];
      sitesService.getAllSites.mockResolvedValue(expectedSites);

      const result = await controller.getAllSites(mockUser, mockToken);
      expect(sitesService.getAllSites).toHaveBeenCalledWith(
        mockUser.id,
        mockToken,
      );
      expect(result).toEqual(expectedSites);
    });
  });

  describe('verifySite', () => {
    it('should forward site id and rawToken to sitesService', async () => {
      const siteId = 'site-uuid';
      const expectedResponse = { id: siteId, status: 'verified' };
      sitesService.verifySite.mockResolvedValue(expectedResponse);

      const result = await controller.verifySite(siteId, mockToken);
      expect(sitesService.verifySite).toHaveBeenCalledWith(siteId, mockToken);
      expect(result).toEqual(expectedResponse);
    });
  });

  describe('getPings', () => {
    it('should forward site id, user.id and rawToken to sitesService', async () => {
      const siteId = 'site-uuid';
      const expectedPings = [
        {
          site_id: siteId,
          duration_ms: 125,
          extra: { status_code: 200 },
        },
      ];
      sitesService.getPings.mockResolvedValue(expectedPings);

      const result = await controller.getPings(siteId, mockUser, mockToken);
      expect(sitesService.getPings).toHaveBeenCalledWith(
        siteId,
        mockUser.id,
        mockToken,
      );
      expect(result).toEqual(expectedPings);
    });
  });
});
