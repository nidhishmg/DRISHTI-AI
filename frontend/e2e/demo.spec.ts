import { test, expect } from '@playwright/test';

test('dashboard loads and displays kpis', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveTitle(/Dashboard/);
    await expect(page.locator('text=Total Voice Reports')).toBeVisible();
    await expect(page.locator('text=Active Clusters')).toBeVisible();
});

test('heatmap is visible', async ({ page }) => {
    await page.goto('/');
    await expect(page.locator('.leaflet-container')).toBeVisible();
});
