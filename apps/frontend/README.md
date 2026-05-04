# Frontend Service

## Overview

**Purpose:** Web UI for managing redirect links with server-side rendering and React Query for data fetching.

**Technology:** Next.js 16, React 19, TypeScript, Tailwind CSS, shadcn/ui, TanStack Query

**Port:** 3000

---

## Responsibilities

- Display list of redirect links
- Create new short links
- Edit and delete existing links
- Auto-generate TypeScript types from OpenAPI spec
- Server-side data prefetching for optimal performance

---

## Project Structure

**Architecture:** Next.js App Router with server/client components:
- `src/app/` - Next.js App Router pages
- `src/components/` - React components
- `src/lib/` - Utilities and API client

**Key Files:**
- `src/app/page.tsx` - Main page
- `src/app/layout.tsx` - Root layout with providers
- `src/lib/api/client.ts` - OpenAPI Fetch client configuration
- `src/lib/api/v1.d.ts` - Auto-generated TypeScript types from OpenAPI
- `src/lib/api/query-client.ts` - React Query client setup

**Explore the codebase:**
```bash
# List all TypeScript/React files
find apps/frontend/src -name "*.tsx" -o -name "*.ts" | head -20

# View app directory structure
ls apps/frontend/src/app/

# View components
ls apps/frontend/src/components/
```

---

## Dependencies

- **Next.js 16** - React framework with App Router
- **React 19** - UI library
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **shadcn/ui** - UI component library
- **TanStack Query** - Data fetching and caching
- **openapi-fetch** - Type-safe API client
- **openapi-react-query** - React Query integration for OpenAPI

---

## Running the Service

### Prerequisites

- Node.js 20+
- npm
- API Backend running on http://localhost:8000

### Setup

```bash
cd apps/frontend
npm install
```

### Start Development Server

```bash
npm run dev
```

The application will be available at http://localhost:3000

---

## API Integration

The frontend uses auto-generated TypeScript types from the OpenAPI specification.

### Update API Types

When the backend API changes:

```bash
# Fetch latest OpenAPI spec and regenerate types
npm run openapi:update
```

This runs:
1. `openapi:fetch` - Downloads OpenAPI JSON from backend
2. `openapi:generate-types` - Generates TypeScript types

### Manual Update

```bash
# Fetch OpenAPI spec only
npm run openapi:fetch

# Generate types only
npm run openapi:generate-types
```

### API Client Usage

```typescript
import { fetchClient } from "@/lib/api/client";

// Type-safe API call
const { data, error } = await fetchClient.GET("/redirect_links/");
```

### React Query Integration

```typescript
// Prefetch in server component
import { dehydrate, HydrationBoundary } from "@tanstack/react-query";

import { client } from "@/lib/api/client";
import { getQueryClient } from "@/lib/api/query-client";

const queryClient = getQueryClient();
await queryClient.prefetchQuery(
  client.queryOptions("get", "/redirect_links/", {
    params: {
      query: {
        limit: 3,
        offset: 0,
      },
    },
  }),
);

// ...

return (
  <HydrationBoundary state={dehydrate(queryClient)}>
    {/* child components with client.useQuery(...) */}
  </HydrationBoundary>
);
```

```typescript
// Get perfetched data in a client component
"use client";

import { client } from "@/lib/api/client";

const { data, error } = client.useQuery("get", "/redirect_links/", {
  params: {
    query: {
      limit: 10,
      offset: 0,
    },
  },
});
```

---

## Development

### Available Scripts

```bash
npm run dev              # Start development server
npm run build            # Build for production
npm run start            # Start production server
npm run lint             # Run ESLint
npm run lint:fix         # Fix ESLint issues
npm run openapi:fetch    # Fetch OpenAPI spec from backend
npm run openapi:generate-types  # Generate TypeScript types
npm run openapi:update   # Fetch and generate (combined)
```

### Adding shadcn/ui Components

```bash
npx shadcn add button
```

### Project Conventions

- Server components in `app/` directory
- Client components marked with `"use client"`
- API types auto-generated from OpenAPI
- React Query for client-side data fetching
- Server prefetching for initial data

---

## Architecture

### Data Flow

1. **Server-side prefetching** (`page.tsx`):
   - Uses React Query to prefetch data on server
   - Dehydrates state for client hydration

2. **Client-side hydration** (`list.tsx`):
   - Hydrates server-fetched data
   - Handles user interactions (create, edit, delete)
   - Uses React Query for mutations

### API Type Safety

All API calls are type-safe through:
- OpenAPI specification from backend
- Auto-generated TypeScript types
- openapi-fetch client with compile-time type checking

---

## Troubleshooting

### Type errors after API changes
- Regenerate types: `npm run openapi:update`
- Ensure backend is running on port 8000

### API connection errors
- Verify API Backend is running: http://localhost:8000/docs
- Check browser console for CORS errors

### Build errors
- Clear `.next/` directory: `rm -rf .next`
- Reinstall dependencies: `rm -rf node_modules && npm install`

### Hot reload not working
- Check `next.config.ts` for proper configuration
- Restart dev server

---

## Updating This Documentation

When modifying this service, update this README if you change:
- Service responsibilities or architecture
- Key files or project structure
- Configuration variables
- Dependencies

**Don't manually document:**
- API endpoints (auto-generated in OpenAPI)
- TypeScript types (auto-generated from OpenAPI)

Always verify root AGENTS.md remains accurate after changes.
