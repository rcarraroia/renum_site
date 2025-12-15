"""
Test RENUS Dynamic Routing - Sprint 09 Task E.6
Tests end-to-end dynamic agent loading and topic-based routing
"""

import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from src.agents.renus import RenusAgent
from src.agents.agent_loader import get_agent_registry
from src.agents.topic_analyzer import get_topic_analyzer
from langchain_core.messages import HumanMessage


async def test_agent_loading():
    """Test 1: Agent loading from database"""
    print("\n" + "="*60)
    print("TEST 1: Agent Loading from Database")
    print("="*60)
    
    registry = get_agent_registry()
    
    # Load agents
    count = registry.load_agents_from_db()
    print(f"✅ Loaded {count} agents from database")
    
    # Get stats
    stats = registry.get_stats()
    print(f"📊 Registry Stats:")
    print(f"   - Total agents: {stats['total_agents']}")
    print(f"   - Total sub-agents: {stats['total_subagents']}")
    print(f"   - Agents with sub-agents: {stats['agents_with_subagents']}")
    print(f"   - Last sync: {stats['last_sync']}")
    
    # List all agents
    agents = registry.list_all_agents()
    print(f"\n📋 Agents in registry:")
    for agent in agents:
        print(f"   - {agent['name']} (ID: {agent['id'][:8]}...)")
        sub_agents = registry.get_subagents(agent['id'])
        if sub_agents:
            print(f"     Sub-agents: {len(sub_agents)}")
            for sub in sub_agents:
                topics = sub.get('topics', [])
                print(f"       • {sub['name']} - Topics: {topics}")
    
    return count > 0


async def test_sync():
    """Test 2: Registry sync"""
    print("\n" + "="*60)
    print("TEST 2: Registry Sync")
    print("="*60)
    
    registry = get_agent_registry()
    
    # Sync
    stats = registry.sync()
    print(f"✅ Sync completed:")
    print(f"   - Total: {stats['total']}")
    print(f"   - Added: {stats['added']}")
    print(f"   - Removed: {stats['removed']}")
    print(f"   - Kept: {stats['kept']}")
    
    return True


async def test_topic_analysis():
    """Test 3: Topic analysis"""
    print("\n" + "="*60)
    print("TEST 3: Topic Analysis")
    print("="*60)
    
    analyzer = get_topic_analyzer()
    
    # Test messages
    test_cases = [
        ("Quero fazer uma pesquisa", ["pesquisa", "vendas", "suporte"]),
        ("Preciso de ajuda com vendas", ["pesquisa", "vendas", "suporte"]),
        ("Como funciona o suporte?", ["pesquisa", "vendas", "suporte"]),
        ("Olá, tudo bem?", ["pesquisa", "vendas", "suporte"]),
    ]
    
    for message, topics in test_cases:
        matched = await analyzer.analyze_topic(message, topics)
        print(f"📝 Message: '{message}'")
        print(f"   Topics: {topics}")
        print(f"   Matched: {matched if matched else 'None'}")
        print()
    
    return True


async def test_routing():
    """Test 4: End-to-end routing"""
    print("\n" + "="*60)
    print("TEST 4: End-to-End Routing")
    print("="*60)
    
    registry = get_agent_registry()
    
    # Get first agent with sub-agents
    agents = registry.list_all_agents()
    
    if not agents:
        print("⚠️  No agents in registry - skipping routing test")
        return False
    
    # Find agent with sub-agents
    agent_with_subs = None
    for agent in agents:
        sub_agents = registry.get_subagents(agent['id'])
        if sub_agents:
            agent_with_subs = agent
            break
    
    if not agent_with_subs:
        print("⚠️  No agents with sub-agents - skipping routing test")
        return False
    
    print(f"🎯 Testing routing for agent: {agent_with_subs['name']}")
    
    # Initialize RENUS
    renus = RenusAgent(enable_periodic_sync=False)
    
    # Test routing
    test_messages = [
        "Quero fazer uma pesquisa",
        "Preciso de ajuda",
        "Como funciona?",
    ]
    
    for message in test_messages:
        try:
            routing = await renus.route_message_dynamic(
                message=message,
                agent_id=agent_with_subs['id']
            )
            
            print(f"\n📝 Message: '{message}'")
            print(f"   Type: {routing['type']}")
            
            if routing['type'] == 'sub_agent':
                print(f"   ✅ Routed to sub-agent: {routing['sub_agent_name']}")
                print(f"   Topic: {routing['topic']}")
            else:
                print(f"   ✅ Routed to main agent: {routing['agent_name']}")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return True


async def test_renus_initialization():
    """Test 5: RENUS initialization with dynamic loading"""
    print("\n" + "="*60)
    print("TEST 5: RENUS Initialization")
    print("="*60)
    
    # Initialize RENUS (should load agents automatically)
    renus = RenusAgent(enable_periodic_sync=False)
    
    # Check registry
    stats = renus.get_registry_stats()
    print(f"✅ RENUS initialized")
    print(f"📊 Registry Stats:")
    print(f"   - Total agents: {stats['total_agents']}")
    print(f"   - Total sub-agents: {stats['total_subagents']}")
    
    return stats['total_agents'] > 0


async def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🧪 RENUS DYNAMIC ROUTING - END-TO-END TESTS")
    print("="*60)
    
    tests = [
        ("Agent Loading", test_agent_loading),
        ("Registry Sync", test_sync),
        ("Topic Analysis", test_topic_analysis),
        ("End-to-End Routing", test_routing),
        ("RENUS Initialization", test_renus_initialization),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = await test_func()
            results.append((test_name, result, None))
        except Exception as e:
            results.append((test_name, False, str(e)))
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    passed = 0
    failed = 0
    
    for test_name, result, error in results:
        if result:
            print(f"✅ {test_name}: PASSED")
            passed += 1
        else:
            print(f"❌ {test_name}: FAILED")
            if error:
                print(f"   Error: {error}")
            failed += 1
    
    print(f"\n📈 Results: {passed}/{len(tests)} passed")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED!")
        return 0
    else:
        print(f"\n⚠️  {failed} test(s) failed")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
