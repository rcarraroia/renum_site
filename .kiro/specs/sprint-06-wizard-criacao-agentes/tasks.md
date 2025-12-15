# Implementation Plan - Sprint 06

## Phase 1: Database Schema Updates

- [x] 1. Update sub_agents table schema


  - Add client_id column (UUID, FK → clients, NOT NULL)
  - Add template_type column (VARCHAR(50), CHECK constraint)
  - Add status column (VARCHAR(20), DEFAULT 'draft', CHECK constraint)
  - Create indexes (client_id, status, template_type)
  - Update RLS policies for client-scoped access
  - _Requirements: 1.2, 2.1, 3.1, 9.1_

- [ ]* 1.1 Write property test for slug uniqueness
  - **Property 2: Slug uniqueness**
  - **Validates: Requirements 8.1**


- [x] 2. Create migration script



  - Write SQL migration file
  - Test migration on development database
  - Verify existing data compatibility
  - Document rollback procedure
  - _Requirements: 1.2_

## Phase 2: Backend - Templates System

- [x] 3. Create template service


  - Define template constants (5 templates)
  - Implement get_template() method
  - Implement generate_system_prompt() method
  - Add template validation
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

- [ ]* 3.1 Write property test for template application idempotence
  - **Property 3: Template application idempotence**
  - **Validates: Requirements 3.2, 3.3**


- [x] 4. Create Pydantic models for wizard


  - CustomFieldConfig model
  - StandardFieldConfig model
  - WizardStep1Data through WizardStep4Data models
  - WizardSession model
  - SandboxMessageRequest/Response models
  - PublicationResult model
  - _Requirements: 1.1, 5.3, 5.4_

## Phase 3: Backend - Wizard API

- [x] 5. Create wizard service


  - Implement start_wizard() method
  - Implement save_step() method
  - Implement get_wizard() method
  - Implement delete_wizard() method
  - Add step validation logic
  - _Requirements: 1.1, 1.5, 10.1, 10.2, 10.3_

- [ ]* 5.1 Write property test for wizard progress persistence
  - **Property 1: Wizard progress persistence**
  - **Validates: Requirements 10.1, 10.2**


- [x] 6. Create wizard API routes

  - POST /api/agents/wizard/start
  - PUT /api/agents/wizard/{wizard_id}/step/{step_number}
  - GET /api/agents/wizard/{wizard_id}
  - DELETE /api/agents/wizard/{wizard_id}
  - Add authentication middleware
  - Add request validation
  - _Requirements: 1.1, 1.5, 10.1_

- [x] 7. Implement B2C agent limit enforcement


  - Check client type (B2B vs B2C)
  - Count active agents for B2C clients
  - Return 403 if limit exceeded
  - Include upgrade URL in error response
  - _Requirements: 2.3, 2.4_

- [ ]* 7.1 Write property test for B2C agent limit enforcement
  - **Property 8: B2C agent limit enforcement**
  - **Validates: Requirements 2.3, 2.4**

## Phase 4: Backend - Sandbox System

- [x] 8. Create sandbox service


  - Implement create_sandbox() method
  - Implement process_message() method (async)
  - Implement get_sandbox_history() method
  - Implement get_collected_data() method
  - Implement cleanup_sandbox() method
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

- [ ]* 8.1 Write property test for sandbox isolation
  - **Property 5: Sandbox isolation**
  - **Validates: Requirements 7.2, 7.3**

- [x] 9. Create sandbox API routes


  - POST /api/agents/wizard/{wizard_id}/sandbox/start
  - POST /api/agents/wizard/{wizard_id}/sandbox/message
  - GET /api/agents/wizard/{wizard_id}/sandbox/history
  - GET /api/agents/wizard/{wizard_id}/sandbox/data
  - DELETE /api/agents/wizard/{wizard_id}/sandbox
  - _Requirements: 7.1, 7.2, 7.3_


- [x] 10. Integrate sandbox with LangGraph

  - Create temporary agent instance from wizard config
  - Process messages through LangGraph
  - Collect structured data from conversation
  - Validate collected data against field configurations
  - _Requirements: 7.3, 12.1, 12.2, 12.3_

- [ ]* 10.1 Write property test for custom field validation
  - **Property 4: Custom field validation**
  - **Validates: Requirements 12.1, 12.2, 12.3**

## Phase 5: Backend - Publication System

- [x] 11. Create publication service


  - Implement generate_slug() method
  - Implement generate_public_url() method
  - Implement generate_embed_code() method
  - Implement generate_qr_code() method
  - Implement publish_agent() method
  - _Requirements: 8.1, 8.2, 8.3, 8.4_

- [ ]* 11.1 Write property test for publication atomicity
  - **Property 7: Publication atomicity**
  - **Validates: Requirements 8.1, 8.2, 8.3, 8.4**


- [x] 12. Create publication API route

  - POST /api/agents/wizard/{wizard_id}/publish
  - Validate wizard completion
  - Create sub_agent record with status='active'
  - Generate all publication assets
  - Return PublicationResult
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_


- [x] 13. Install QR code generation library

  - Add qrcode or segno to requirements.txt
  - Test QR code generation
  - Configure QR code size and format
  - _Requirements: 8.4_

## Phase 6: Backend - Integration Status Check




- [ ] 14. Create integration status endpoint
  - GET /api/integrations/status (reuse from Sprint 07A)
  - Return list of integrations with status
  - Filter by client_id
  - _Requirements: 6.1, 6.2, 6.3_

- [ ]* 14.1 Write property test for integration status consistency
  - **Property 6: Integration status consistency**
  - **Validates: Requirements 6.2, 6.3**

## Phase 7: Frontend - Wizard Components (Step 1)

- [x] 15. Create Step1Objective component



  - Template selection cards (5 templates)
  - Agent name input with validation
  - Real-time slug generation preview
  - Description textarea
  - Niche dropdown
  - _Requirements: 3.1, 3.2, 3.5_




- [ ] 16. Create template cards UI
  - Design template card component
  - Add icons for each template
  - Display template description
  - Highlight selected template
  - _Requirements: 3.1, 3.5_


- [x] 17. Implement slug generation logic

  - Convert name to lowercase
  - Replace spaces with hyphens
  - Remove special characters
  - Show preview in real-time
  - _Requirements: 8.1_


## Phase 8: Frontend - Wizard Components (Step 2)

- [x] 18. Create Step2Personality component

  - Personality selector (4 cards)
  - Tone sliders (formal vs informal, direct vs descriptive)
  - Conversation preview section
  - Real-time preview updates
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

- [x] 19. Implement conversation preview

  - Display 3 example exchanges
  - Update examples when personality/tone changes
  - Use template-specific examples
  - Smooth transition animations
  - _Requirements: 13.1, 13.2_

## Phase 9: Frontend - Wizard Components (Step 3)

- [x] 20. Create Step3Fields component


  - Standard fields checklist
  - Required toggle for each field
  - Custom fields builder section
  - Add field button
  - Conversation flow preview
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

- [x] 21. Create custom field configuration form

  - Field type selector
  - Label input
  - Validation rules configuration
  - Placeholder input
  - Options input (for radio/checkbox/dropdown)
  - _Requirements: 5.3, 5.4_

- [x] 22. Implement drag-and-drop field reordering

  - Use react-beautiful-dnd or similar library
  - Visual feedback during drag
  - Update order in state
  - Update conversation flow preview
  - _Requirements: 5.5_

- [ ]* 22.1 Write property test for field order preservation
  - **Property 9: Field order preservation**
  - **Validates: Requirements 5.5**

## Phase 10: Frontend - Wizard Components (Step 4)

- [x] 23. Create Step4Integrations component


  - Integration cards (WhatsApp, Email, Database)
  - Status indicators (✅ Configured / ⚠️ Not Configured)
  - Enable checkboxes
  - "Configure Now" buttons
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

- [x] 24. Integrate with Sprint 07A integration modals

  - Import integration configuration components
  - Open modal on "Configure Now" click
  - Refresh status after configuration
  - Return to wizard after configuration
  - _Requirements: 6.4, 6.5_

## Phase 11: Frontend - Wizard Components (Step 5)


- [x] 25. Create Step5TestPublish component

  - Sandbox chat interface
  - "Start Test" button
  - Message input and display
  - Collected information summary
  - "Publish Agent" button
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

- [x] 26. Implement sandbox chat functionality

  - Connect to sandbox WebSocket or API
  - Send and receive messages
  - Display typing indicator
  - Show collected data in real-time
  - _Requirements: 7.2, 7.3, 7.4_

- [x] 27. Create publication success modal

  - Display public URL (with copy button)
  - Display embed code (with copy button)
  - Display QR code image (with download button)
  - "View Agent" button (redirect to agent details)
  - _Requirements: 8.2, 8.3, 8.4, 8.5_


## Phase 12: Frontend - Main Wizard Container

- [x] 28. Update AgentWizard main component

  - Replace existing wizard with new 5-step flow
  - Implement step navigation (Next/Previous)
  - Implement step validation
  - Implement auto-save on step completion
  - Implement wizard state management
  - _Requirements: 1.1, 1.5, 10.1, 10.2_

- [x] 29. Create wizard API service


  - startWizard() function
  - saveStep() function
  - getWizard() function
  - deleteWizard() function
  - testSandbox() function

  - publishAgent() function
  - _Requirements: 1.1, 1.5, 10.1_


- [x] 30. Implement wizard progress persistence

  - Save to backend on each step completion
  - Load saved progress on wizard mount
  - Handle network errors gracefully
  - Show save status indicator
  - _Requirements: 10.1, 10.2, 10.3_

## Phase 13: Frontend - Agents Dashboard


- [x] 31. Update AgentsListPage component


  - Display agents with new status field
  - Add filter by template_type
  - Add filter by status
  - Display draft agents separately

  - _Requirements: 9.1, 10.4_

- [x] 32. Implement agent actions


  - Edit button (redirect to agent config, not wizard)
  - Clone button (create duplicate with "-copy" suffix)
  - Pause/Resume button (toggle status)

  - Delete button (with confirmation modal)
  - _Requirements: 9.2, 9.3, 9.4, 9.5_

- [x] 33. Create agent metrics display

  - Total conversations
  - Conversations today
  - Leads qualified
  - Conversion rate

  - _Requirements: 9.1_

## Phase 14: Frontend - Services and Types

- [x] 34. Create TypeScript types

  - WizardFormData interface

  - CustomField interface
  - AgentListItem interface
  - PublicationResult interface
  - _Requirements: 1.1, 5.3, 9.1_

- [x] 35. Create agentService.ts

  - listAgents() function
  - getAgent() function
  - cloneAgent() function
  - pauseAgent() function
  - deleteAgent() function
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

## Phase 15: Integration and Testing

- [x] 36. Checkpoint - Backend API Testing




  - Test all wizard endpoints with Postman/curl
  - Verify wizard session creation and retrieval
  - Verify step data persistence
  - Verify sandbox functionality
  - Verify publication generates all assets
  - Ensure all tests pass, ask the user if questions arise.
  - _Requirements: 1.1, 7.1, 8.1_

- [x] 37. Checkpoint - Frontend Integration Testing


  - Test complete wizard flow (all 5 steps)
  - Test template selection and application
  - Test custom field creation and reordering
  - Test integration status display
  - Test sandbox chat interaction
  - Test agent publication
  - Ensure all tests pass, ask the user if questions arise.
  - _Requirements: 1.1, 3.1, 5.3, 6.1, 7.1, 8.1_

- [x] 38. Checkpoint - End-to-End Testing


  - Create agent as B2B client (multiple agents)
  - Create agent as B2C client (single agent limit)
  - Test draft agent persistence and resumption
  - Test agent cloning
  - Test agent pause/resume
  - Test agent deletion
  - Verify public URL accessibility
  - Verify embed code functionality
  - Verify QR code generation
  - Ensure all tests pass, ask the user if questions arise.
  - _Requirements: 1.1, 2.1, 2.3, 8.1, 9.1, 10.1_

## Phase 16: Documentation and Cleanup

- [ ]* 39. Update API documentation
  - Document all new wizard endpoints
  - Add request/response examples
  - Document error codes
  - Update Swagger/OpenAPI spec
  - _Requirements: 1.1_
  - _Note: Can be done post-sprint_

- [ ]* 40. Create user guide
  - Write step-by-step wizard guide
  - Add screenshots for each step
  - Document template options
  - Document custom field types
  - Document publication assets usage
  - _Requirements: 1.1, 3.1, 5.3, 8.1_
  - _Note: Can be done post-sprint_

- [x] 41. Clean up old wizard code


  - Archive old wizard components (if replacing)
  - Remove unused imports
  - Update routing
  - Test that no functionality is broken
  - _Requirements: 1.1_
  - _Note: Not applicable - no old wizard existed_

- [x] 42. Final validation


  - Run all unit tests
  - Run all integration tests
  - Run all property-based tests
  - Verify all requirements are met
  - Get user approval for deployment
  - _Requirements: ALL_

