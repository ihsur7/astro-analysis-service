import { defineStore } from "pinia";
import axios from "axios";
import type { AstronomicalObject, FiltersPayload, PaginatedObjectsResponse, StatsResponse } from "../types";

interface CatalogState {
  filters: FiltersPayload;
  stats: StatsResponse | null;
  objects: AstronomicalObject[];
  total: number;
  pages: number;
  loading: boolean;
  error: string | null;
  magnitudeDistribution: { bins: number[]; counts: number[] } | null;
  spectralBreakdown: Record<string, number> | null;
  distanceDistribution: { bins: number[]; counts: number[] } | null;
  correlation: { magnitudes: number[]; distances: number[] } | null;
  maxRecords: number;
}

const defaultFilters: FiltersPayload = {
  magnitude_min: undefined,
  magnitude_max: undefined,
  distance_min: undefined,
  distance_max: undefined,
  constellation: undefined,
  spectral_type: undefined,
  search: undefined,
  page: 1,
  page_size: 10
};

const STORAGE_KEY = 'astro-settings';

function loadMaxRecords(): number {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      const settings = JSON.parse(stored);
      return settings.maxRecords || 150;
    }
  } catch (e) {
    console.warn('Failed to load settings from localStorage', e);
  }
  return 150;
}

function saveMaxRecords(value: number) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({ maxRecords: value }));
  } catch (e) {
    console.warn('Failed to save settings to localStorage', e);
  }
}

export const useCatalogStore = defineStore("catalog", {
  state: (): CatalogState => ({
    filters: { ...defaultFilters },
    stats: null,
    objects: [],
    total: 0,
    pages: 0,
    loading: true,
    error: null,
    magnitudeDistribution: null,
    spectralBreakdown: null,
    distanceDistribution: null,
    correlation: null,
    maxRecords: loadMaxRecords()
  }),
  actions: {
    setFilters(partial: Partial<FiltersPayload>) {
      this.filters = { ...this.filters, ...partial };
    },
    async refresh() {
      this.loading = true;
      this.error = null;
      try {
        const [statsResponse, objectsResponse] = await Promise.all([
          axios.get<StatsResponse>("/stats"),
          axios.get<PaginatedObjectsResponse>("/objects", { params: this.filters })
        ]);
        this.stats = statsResponse.data;
        this.objects = objectsResponse.data.items;
        this.total = objectsResponse.data.total;
        this.pages = objectsResponse.data.pages;
        this.filters.page = objectsResponse.data.page;
        this.filters.page_size = objectsResponse.data.page_size;
      } catch (error) {
        this.error = error instanceof Error ? error.message : "Unknown error";
      } finally {
        this.loading = false;
      }
    },
    async fetchMagnitudeDistribution(bins = 10) {
      const response = await axios.get<{ bins: number[]; counts: number[] }>(
        "/analysis/magnitude-distribution",
        { params: { bins } }
      );
      this.magnitudeDistribution = response.data;
    },
    async fetchSpectralBreakdown() {
      const response = await axios.get<Record<string, number>>("/analysis/spectral-breakdown");
      this.spectralBreakdown = response.data;
    },
    async fetchDistanceDistribution(bins = 10) {
      const response = await axios.get<{ bins: number[]; counts: number[] }>(
        "/analysis/distance-distribution",
        { params: { bins } }
      );
      this.distanceDistribution = response.data;
    },
    async fetchCorrelation() {
      const response = await axios.get<{ magnitudes: number[]; distances: number[] }>(
        "/analysis/magnitude-distance-correlation"
      );
      this.correlation = response.data;
    },
    resetFilters() {
      this.filters = { ...defaultFilters };
      this.refresh();
    },
    async updateMaxRecords(limit: number) {
      try {
        // Trigger backend to refresh data with new limit
        await axios.post('/admin/refresh-data', { limit });
        
        // Save to localStorage
        this.maxRecords = limit;
        saveMaxRecords(limit);
        
        // Refresh the UI data
        await this.refresh();
      } catch (error) {
        throw new Error(error instanceof Error ? error.message : 'Failed to update max records');
      }
    }
  }
});
