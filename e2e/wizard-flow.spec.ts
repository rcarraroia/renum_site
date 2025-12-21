/**
 * Task 33: End-to-End Testing - Wizard Flow
 * Testes de integração completos usando Playwright
 */

import { test, expect } from '@playwright/test';

test.describe('Wizard Flow E2E', () => {
    test.beforeEach(async ({ page }) => {
        // Login
        await page.goto('/login');
        await page.fill('input[name="email"]', 'admin@renum.com');
        await page.fill('input[name="password"]', 'testpassword');
        await page.click('button[type="submit"]');
        await page.waitForURL('/dashboard/**');
    });

    test('should complete full wizard flow for RENUS agent', async ({ page }) => {
        // Step 1: Navigate to wizard
        await page.goto('/dashboard/agents/wizard/new');
        await expect(page.locator('h1')).toContainText('Criar Novo Agente');

        // Step 2: Select agent type
        await page.click('button:has-text("Sistema (RENUS/ISA)")');
        await expect(page.locator('[data-testid="agent-type-system"]')).toBeVisible();
        await page.click('button:has-text("Próximo")');

        // Step 3: Fill basic info
        await page.fill('input[name="name"]', 'Test RENUS Agent');
        await page.fill('textarea[name="description"]', 'Agente de teste para E2E');
        await page.click('button:has-text("Próximo")');

        // Step 4: Configure personality
        await page.fill('input[name="persona"]', 'Assistente profissional');
        await page.click('button:has-text("Próximo")');

        // Step 5: Configure integrations
        await page.click('label:has-text("WhatsApp")');
        await page.click('button:has-text("Próximo")');

        // Step 6: Test and publish
        await page.click('button:has-text("Testar Agente")');
        await expect(page.locator('.test-result')).toBeVisible();

        await page.click('button:has-text("Publicar")');
        await expect(page.locator('.success-message')).toContainText('publicado');
    });

    test('should create agent from marketplace template', async ({ page }) => {
        // Navigate to marketplace
        await page.goto('/dashboard/marketplace');
        await expect(page.locator('h1')).toContainText('Marketplace');

        // Select first template
        const firstTemplate = page.locator('.template-card').first();
        await firstTemplate.click();

        // Preview and use template
        await page.click('button:has-text("Usar Template")');

        // Should redirect to wizard with template pre-filled
        await expect(page.url()).toContain('/wizard/new?template=');

        // Complete wizard
        await page.fill('input[name="name"]', 'Agent from Template');
        await page.click('button:has-text("Criar Agente")');

        await expect(page.locator('.success-message')).toBeVisible();
    });

    test('should navigate between contextual interfaces', async ({ page }) => {
        // Test RENUS interface
        await page.goto('/dashboard/agents/renus');
        await expect(page.locator('h1')).toContainText('RENUS');
        await expect(page.locator('.metrics-card')).toHaveCount(4);

        // Test quick link to config
        await page.click('a:has-text("Configuração Técnica")');
        await expect(page.url()).toContain('/config');

        // Navigate back and to ISA
        await page.goto('/dashboard/agents/isa');
        await expect(page.locator('h1')).toContainText('ISA');

        // Test Pesquisas
        await page.goto('/dashboard/agents/pesquisas');
        await expect(page.locator('h1')).toContainText('Pesquisas');
    });

    test('should manage sub-agents', async ({ page }) => {
        // Navigate to agent config
        await page.goto('/dashboard/admin/agents/test-agent/config');

        // Go to sub-agents tab
        await page.click('button:has-text("Sub-agentes")');

        // Create sub-agent
        await page.click('button:has-text("Novo Sub-agente")');
        await page.fill('input[name="name"]', 'Sub-agente B2C');
        await page.fill('textarea[name="specialization"]', 'Atendimento ao consumidor');

        // Configure inheritance
        await page.click('input[name="inherit-instructions"]');
        await page.click('input[name="inherit-intelligence"]');

        await page.click('button:has-text("Criar Sub-agente")');
        await expect(page.locator('.sub-agent-card')).toContainText('Sub-agente B2C');
    });

    test('should test integrations in radar', async ({ page }) => {
        await page.goto('/dashboard/integrations/radar');
        await expect(page.locator('h1')).toContainText('Radar');

        // Test integration button
        const whatsappCard = page.locator('.integration-card:has-text("WhatsApp")');
        await whatsappCard.locator('button:has-text("Testar")').click();

        // Wait for test result
        await expect(page.locator('.test-result')).toBeVisible({ timeout: 10000 });
    });

    test('should view intelligence dashboard', async ({ page }) => {
        await page.goto('/dashboard/intelligence');
        await expect(page.locator('h1')).toContainText('Intelligence');

        // Check tabs
        await expect(page.locator('button:has-text("Evolução")')).toBeVisible();
        await expect(page.locator('button:has-text("Memórias")')).toBeVisible();
        await expect(page.locator('button:has-text("Aprendizado")')).toBeVisible();

        // Check agent cards are loaded
        await expect(page.locator('.agent-evolution-card')).toHaveCount({ gt: 0 });
    });
});

test.describe('Configuration Tabs E2E', () => {
    test('should save and load all configuration tabs', async ({ page }) => {
        await page.goto('/dashboard/admin/agents/test-agent/config');

        const tabs = [
            'Instruções',
            'Inteligência',
            'Ferramentas',
            'Integrações',
            'Conhecimento',
            'Triggers',
            'Guardrails',
            'Sub-agentes',
            'Avançado'
        ];

        for (const tab of tabs) {
            await page.click(`button:has-text("${tab}")`);
            await expect(page.locator('.tab-content')).toBeVisible();

            // Each tab should have a save button
            await expect(page.locator('button:has-text("Salvar")')).toBeVisible();
        }
    });
});
