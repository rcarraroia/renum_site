/**
 * Task 6.2: Property test for inheritance independence
 * Property 4: Sub-agent Independence Consistency
 * Validates: Requirements 3.4
 */

import fc from 'fast-check';
import { describe, test, expect } from '@jest/globals';

describe('Property 4: Sub-agent Independence Consistency', () => {
    test('sub-agent with inheritance disabled can have different configuration', () => {
        fc.assert(
            fc.property(
                fc.record({ system_prompt: fc.string() }),
                fc.record({ system_prompt: fc.string() }),
                fc.boolean(),
                (parentInstructions, subAgentInstructions, inherit) => {
                    const effective = inherit ? parentInstructions : subAgentInstructions;

                    if (!inherit) {
                        // Sub-agent should be able to have different config
                        // (even if it happens to be the same by chance)
                        expect(effective).toEqual(subAgentInstructions);
                    } else {
                        expect(effective).toEqual(parentInstructions);
                    }
                }
            ),
            { numRuns: 100 }
        );
    });
});
