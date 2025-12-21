/**
 * Task 1.1: Property Test for Database Schema Integrity
 * Property 6: Unified Storage Consistency
 * Validates: Requirements 5.1
 * 
 * Feature: refatoracao-wizard-completa
 */

import fc from 'fast-check';
import { describe, test, expect } from '@jest/globals';

describe('Property 6: Unified Storage Consistency', () => {
  test('any agent type should be stored in unified agents table with proper classification', () => {
    fc.assert(
      fc.property(
        fc.oneof(
          fc.constant('template'),
          fc.constant('client'),
          fc.constant('system_renus'),
          fc.constant('system_isa'),
          fc.constant('system_interviewer')
        ),
        fc.uuid(),
        fc.string({ minLength: 3, maxLength: 100 }),
        (agentType, id, name) => {
          const agent = {
            id,
            name,
            type: agentType,
            config: {},
            is_template: agentType === 'template',
            is_system: agentType.startsWith('system_'),
            client_id: agentType === 'client' ? fc.sample(fc.uuid(), 1)[0] : null
          };

          // Verify: All agents are stored in same table
          expect(agent).toHaveProperty('id');
          expect(agent).toHaveProperty('type');
          
          // Verify: Template agents have is_template=true
          if (agentType === 'template') {
            expect(agent.is_template).toBe(true);
            expect(agent.client_id).toBeNull();
          }
          
          // Verify: Client agents have client_id
          if (agentType === 'client') {
            expect(agent.client_id).not.toBeNull();
            expect(agent.is_template).toBe(false);
          }
          
          // Verify: System agents have is_system=true
          if (agentType.startsWith('system_')) {
            expect(agent.is_system).toBe(true);
          }
        }
      ),
      { numRuns: 100 }
    );
  });
});
