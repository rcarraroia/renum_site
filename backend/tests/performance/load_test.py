"""
Task 34: Performance Testing
Testes de carga e performance usando locust
"""

from locust import HttpUser, task, between
import json
import random

class AgentLoadTestUser(HttpUser):
    """Load testing for agent management APIs"""
    
    wait_time = between(1, 3)
    
    def on_start(self):
        """Login and get token"""
        response = self.client.post("/api/auth/login", json={
            "email": "loadtest@renum.com",
            "password": "loadtest123"
        })
        if response.status_code == 200:
            self.token = response.json().get("access_token")
            self.headers = {"Authorization": f"Bearer {self.token}"}
        else:
            self.headers = {}
    
    @task(3)
    def list_agents(self):
        """List agents - most common operation"""
        self.client.get("/api/agents", headers=self.headers)
    
    @task(2)
    def get_agent_details(self):
        """Get single agent details"""
        # Use a known agent ID or randomize
        agent_id = "test-agent-id"
        self.client.get(f"/api/agents/{agent_id}", headers=self.headers)
    
    @task(1)
    def get_agent_config(self):
        """Get agent configuration"""
        agent_id = "test-agent-id"
        self.client.get(f"/api/agents/{agent_id}/config", headers=self.headers)
    
    @task(1)
    def update_agent_config(self):
        """Update agent configuration"""
        agent_id = "test-agent-id"
        config = {
            "instructions": {
                "system_prompt": f"Test prompt {random.randint(1, 1000)}"
            }
        }
        self.client.put(
            f"/api/agents/{agent_id}/config/instructions",
            json=config,
            headers=self.headers
        )
    
    @task(1)
    def list_sub_agents(self):
        """List sub-agents"""
        agent_id = "test-agent-id"
        self.client.get(f"/api/agents/{agent_id}/sub-agents", headers=self.headers)
    
    @task(1)
    def get_templates(self):
        """Get marketplace templates"""
        self.client.get("/api/agents/wizard/templates", headers=self.headers)


class WizardLoadTestUser(HttpUser):
    """Load testing for wizard flow"""
    
    wait_time = between(2, 5)
    
    def on_start(self):
        """Login"""
        response = self.client.post("/api/auth/login", json={
            "email": "loadtest@renum.com",
            "password": "loadtest123"
        })
        if response.status_code == 200:
            self.token = response.json().get("access_token")
            self.headers = {"Authorization": f"Bearer {self.token}"}
        else:
            self.headers = {}
    
    @task(1)
    def complete_wizard_flow(self):
        """Complete full wizard flow"""
        # Step 1: Start wizard
        response = self.client.post(
            "/api/agents/wizard/start",
            json={"agent_type": "client", "client_id": "test-client"},
            headers=self.headers
        )
        
        if response.status_code != 200:
            return
        
        session_id = response.json().get("session_id")
        
        # Step 2: Basic info
        self.client.post(
            f"/api/agents/wizard/step/1",
            json={
                "session_id": session_id,
                "data": {"name": f"Load Test Agent {random.randint(1, 10000)}"}
            },
            headers=self.headers
        )
        
        # Step 3: Complete
        self.client.post(
            f"/api/agents/wizard/complete",
            json={"session_id": session_id},
            headers=self.headers
        )


class IntegrationLoadTestUser(HttpUser):
    """Load testing for integrations"""
    
    wait_time = between(5, 10)
    
    def on_start(self):
        """Login"""
        response = self.client.post("/api/auth/login", json={
            "email": "loadtest@renum.com",
            "password": "loadtest123"
        })
        if response.status_code == 200:
            self.token = response.json().get("access_token")
            self.headers = {"Authorization": f"Bearer {self.token}"}
        else:
            self.headers = {}
    
    @task(2)
    def list_integrations(self):
        """List all integrations"""
        self.client.get("/api/integrations/status", headers=self.headers)
    
    @task(1)
    def test_integration(self):
        """Test an integration"""
        integration_type = random.choice(["whatsapp", "email", "sms"])
        self.client.post(
            f"/api/integrations/{integration_type}/test",
            headers=self.headers
        )


# Performance thresholds
PERFORMANCE_THRESHOLDS = {
    "list_agents": {"p95": 500, "p99": 1000},  # ms
    "get_agent": {"p95": 200, "p99": 500},
    "update_config": {"p95": 300, "p99": 700},
    "wizard_complete": {"p95": 2000, "p99": 5000},
    "integration_test": {"p95": 5000, "p99": 10000}
}
