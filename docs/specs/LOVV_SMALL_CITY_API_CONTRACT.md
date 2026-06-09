# Lovv Small City API Contract

## Purpose

This contract defines the future backend/API boundary for loading small-city candidates into the Lovv frontend. The current implementation remains frontend-only, but the data adapter now expects a backend-friendly shape and converts it into the existing `SmallCity` model.

## Endpoints

```text
GET /api/small-cities
GET /api/small-cities/:cityId
```

No real request is made in Task 9. These paths are contract placeholders for the future backend.

## List Query Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `country` | `KR` or `JP` | No | Country filter. |
| `q` | string | No | Search keyword for city, region, theme, route hint, or detail text. |
| `themes` | comma-separated theme labels | No | Theme filters such as `자연,바다`. |
| `page` | positive integer | No | Page number. Defaults to `1`. |
| `page_size` | positive integer | No | Page size. Defaults to `120`. |

## List Response

```ts
type SmallCityApiListResponse = {
  data: SmallCityApiRecord[]
  page: {
    page: number
    pageSize: number
    total: number
    hasNext: boolean
  }
}
```

## City Record

```ts
type SmallCityApiRecord = {
  id: string
  country: 'KR' | 'JP'
  country_label?: '한국' | '일본'
  region: string
  name_ko: string
  name_local?: string | null
  latitude: number
  longitude: number
  themes: string[]
  summary: string
  detail: string
  highlights: string[]
  route_seed: string[]
  image_url?: string | null
  internal_meta?: {
    rankingScore?: number
    source?: string
    provider?: string
    updatedAt?: string
  }
}
```

## Frontend Adapter Rules

- `country_label` is optional. The frontend derives `한국` or `일본` from `country`.
- Unknown theme strings are dropped.
- Rows without valid id, country, coordinates, text fields, themes, highlights, or route seed are rejected.
- Rejected rows are reported in adapter output and do not crash the UI.
- `internal_meta` is backend/internal only.
- `internal_meta` must not be passed to `SmallCityMapMarker`.
- Marker labels must use `name_ko` only.

## Data Flow

```text
SmallCityApiListResponse
  -> adaptSmallCityApiResponse()
  -> SmallCity[]
  -> createSmallCityMapMarkers()
  -> SmallCityLeafletMap
```

The selected-city detail card and AI planner resolve the full `SmallCity` record in the parent view. The map component receives only normalized marker records.

## Future Backend Notes

- Backend can add ranking, personalization, provider provenance, or update metadata through `internal_meta`.
- If ranking or personalization becomes user-facing, it needs a separate Spec and copy review.
- Country-scale Japan data should support pagination or server-side filtering before production.
- Client-side validation remains UX support only; backend must validate all query parameters and response fields.
