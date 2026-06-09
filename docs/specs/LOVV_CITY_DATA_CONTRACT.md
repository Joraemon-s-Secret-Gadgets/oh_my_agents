# Lovv City Data Contract

## Purpose

This document describes the frontend city-data boundary created in Task 8. It keeps Lovv's map layer, selected-city detail card, and AI planner flow separable while the app still uses deterministic local data.

## Full City Record

The full city record is the product/detail object. It may come from local data today or a backend response later.

```ts
type SmallCity = {
  id: string
  country: 'KR' | 'JP'
  countryLabel: '한국' | '일본'
  region: string
  nameKo: string
  nameLocal?: string
  latitude: number
  longitude: number
  themes: SmallCityTheme[]
  summary: string
  detail: string
  highlights: string[]
  routeSeed: string[]
  image?: string
}
```

Rules:

- `nameKo` is the user-facing marker label source.
- `themes`, `summary`, `detail`, `highlights`, and `routeSeed` are detail/planner fields, not marker-label fields.
- `routeSeed` can contain itinerary hints such as craft, forest, market, or walk routes. Those hints must not become map marker names.

## Map Marker Record

The map marker record is the only shape the Leaflet map component should receive.

```ts
type SmallCityMapMarker = {
  id: string
  cityId: string
  country: 'KR' | 'JP'
  countryLabel: '한국' | '일본'
  region: string
  label: string
  localLabel?: string
  latitude: number
  longitude: number
}
```

Rules:

- `label` must be the city name, not a theme or itinerary hint.
- Marker records must not include `themes`, `summary`, `detail`, `highlights`, or `routeSeed`.
- Selecting a marker returns `cityId`; the parent view resolves the full city detail from the candidate list.

## Current Candidate Counts

- Korea: 40 city candidates.
- Japan: 40 unique city candidates.

The current Japanese data uses unique city candidates only. Theme or itinerary hints such as market, craft, forest, or walk routes belong in `themes`, `highlights`, `routeSeed`, selected-city detail, and planner flow. They must not create duplicate map/list records for the same city name.

Future backend data may expand Japan beyond 40 records, but that expansion must use unique city identities rather than generated variants of the same city.

## Future Backend Mapping

A future backend response can replace local data if it produces the full city record shape or can be adapted into it. The map component should remain unchanged as long as the frontend adapter can produce `SmallCityMapMarker[]`.

Recommended adapter boundary:

```ts
backendCityRows -> SmallCity[] -> SmallCityMapMarker[] -> SmallCityLeafletMap
```

The backend may add ranking, availability, personalization score, or provider metadata, but those fields should not be passed to the map layer or shown in user-facing copy unless a future Spec approves them.
