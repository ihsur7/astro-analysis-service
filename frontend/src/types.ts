export interface AstronomicalObject {
  id: number;
  name: string;
  constellation: string;
  magnitude: number;
  distance_ly: number;
  spectral_type: string;
}

export interface PaginatedObjectsResponse {
  total: number;
  page: number;
  page_size: number;
  pages: number;
  items: AstronomicalObject[];
}

export interface StatsResponse {
  count: number;
  magnitude_min: number | null;
  magnitude_max: number | null;
  magnitude_avg: number | null;
  brightest_object: AstronomicalObject | null;
  dimmest_object: AstronomicalObject | null;
}

export interface FiltersPayload {
  magnitude_min?: number;
  magnitude_max?: number;
  distance_min?: number;
  distance_max?: number;
  constellation?: string;
  spectral_type?: string;
  search?: string;
  page: number;
  page_size: number;
}
