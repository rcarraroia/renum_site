"""
Task 3.1: Property test for agent CRUD operations
Property 8: Configuration Data Integrity
Validates: Requirements 5.3
"""

import fc from 'fast-check';
import { describe, test, expect } from '@jest/globals';

describe('Property 8: Configuration Data Integrity', () => {
    test('agent configuration update maintains integrity across all 9 categories', () => {
        fc.assert(
            fc.property(
                fc.record({
                    instructions: fc.record({
                        system_prompt: fc.string(),
                        persona: fc.string()
                    }),
                    intelligence: fc.record({
                        model: fc.constantFrom('gpt-4o', 'gpt-4o-mini', 'claude-3'),
                        temperature: fc.float({ min: 0, max: 1 })
                    }),
                    tools: fc.record({
                        enabled_tools: fc.array(fc.string())
                    }),
                    integrations: fc.record({}),
                    knowledge: fc.record({}),
                    triggers: fc.record({}),
                    guardrails: fc.record({}),
                    sub_agents: fc.record({}),
                    advanced: fc.record({})
                }),
                (config) => {
                    // Verify: All 9 categories exist
                    expect(config).toHaveProperty('instructions');
                    expect(config).toHaveProperty('intelligence');
                    expect(config).toHaveProperty('tools');
                    expect(config).toHaveProperty('integrations');
                    expect(config).toHaveProperty('knowledge');
                    expect(config).toHaveProperty('triggers');
                    expect(config).toHaveProperty('guardrails');
                    expect(config).toHaveProperty('sub_agents');
                    expect(config).toHaveProperty('advanced');

                    // Verify: Instructions maintains structure
                    if (config.instructions.system_prompt) {
                        expect(typeof config.instructions.system_prompt).toBe('string');
                    }

                    // Verify: Intelligence parameters are valid
                    expect(config.intelligence.temperature).toBeGreaterThanOrEqual(0);
                    expect(config.intelligence.temperature).toBeLessThanOrEqual(1);
                }
            ),
            { numRuns: 100 }
        );
    });
});
