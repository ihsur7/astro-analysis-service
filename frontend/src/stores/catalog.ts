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

export const useCatalogStore = defineStore("catalog", {
  state: (): CatalogState => ({
    filters: { ...defaultFilters },
    stats: null,
    objects: [],
    total: 0,
    pages: 0,
    loading: true,
    error: null
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
    resetFilters() {
      this.filters = { ...defaultFilters };
      this.refresh();
    }
  }
});
