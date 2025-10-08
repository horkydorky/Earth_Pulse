/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_BASE_URL: string
  readonly VITE_API_VERSION: string
  readonly VITE_API_TIMEOUT: string
  readonly VITE_MAPBOX_TOKEN: string
  readonly VITE_MAPBOX_STYLE_ID: string
  readonly VITE_NASA_API_KEY: string
  readonly VITE_NASA_DISCOVERY_API: string
  readonly VITE_CARTODB_API_KEY: string
  readonly VITE_CARTODB_BASE_URL: string
  readonly VITE_APP_NAME: string
  readonly VITE_APP_VERSION: string
  readonly VITE_APP_ENVIRONMENT: string
  readonly VITE_ENABLE_ANALYTICS: string
  readonly VITE_ENABLE_REPORTING: string
  readonly VITE_ENABLE_DOWNLOADS: string
  readonly VITE_ENABLE_SHARING: string
  readonly VITE_DEFAULT_REGION: string
  readonly VITE_DEFAULT_YEAR: string
  readonly VITE_DATA_YEAR_RANGE: string
  readonly VITE_MAX_EXPORT_SIZE: string
  readonly VITE_SUPPORTED_EXPORT_FORMATS: string
  readonly VITE_DEBUG_MODE: string
  readonly VITE_LOG_LEVEL: string
  readonly VITE_ENABLE_DEVTOOLS: string
  readonly VITE_CACHE_TTL: string
  readonly VITE_MAX_CONCURRENT_REQUESTS: string
  readonly VITE_REQUEST_RETRY_ATTEMPTS: string
  readonly VITE_MOCK_DATA_ENABLED: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
