"""
Simple WebSocket Test - Sprint 09
Tests WebSocket connection and basic functionality
"""

import asyncio
import json
import websockets
from datetime import datetime


# Configuration
WS_URL = "ws://localhost:8000/ws"
JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0LXVzZXItMDAxIiwicm9sZSI6ImF1dGhlbnRpY2F0ZWQiLCJpYXQiOjE3NjUxMTY0NTgsImV4cCI6MTc2NTEyMDA1OH0.1_42xDSOZX-1D4RQ79LI1IfL3l8xl-dUGgkeZrPXTDY"  # Valid token generated


async def test_websocket_connection():
    """Test WebSocket connection with JWT token"""
    print("=" * 60)
    print("TEST 1: WebSocket Connection")
    print("=" * 60)
    
    url = f"{WS_URL}?token={JWT_TOKEN}"
    print(f"\nConnecting to: {url}")
    
    try:
        async with websockets.connect(url) as websocket:
            print("✅ Connected successfully!")
            
            # Wait for connected message
            response = await websocket.recv()
            data = json.loads(response)
            print(f"\nReceived: {json.dumps(data, indent=2)}")
            
            if data.get("type") == "connected":
                print("✅ Received connected confirmation")
                return True
            else:
                print("❌ Expected 'connected' message")
                return False
                
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False


async def test_ping_pong():
    """Test ping/pong keep-alive"""
    print("\n" + "=" * 60)
    print("TEST 2: Ping/Pong")
    print("=" * 60)
    
    url = f"{WS_URL}?token={JWT_TOKEN}"
    
    try:
        async with websockets.connect(url) as websocket:
            # Wait for connected
            await websocket.recv()
            
            # Send ping
            ping_message = {"type": "ping"}
            await websocket.send(json.dumps(ping_message))
            print(f"\nSent: {json.dumps(ping_message, indent=2)}")
            
            # Wait for pong
            response = await websocket.recv()
            data = json.loads(response)
            print(f"\nReceived: {json.dumps(data, indent=2)}")
            
            if data.get("type") == "pong":
                print("✅ Received pong response")
                return True
            else:
                print("❌ Expected 'pong' message")
                return False
                
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


async def test_join_conversation():
    """Test joining a conversation"""
    print("\n" + "=" * 60)
    print("TEST 3: Join Conversation")
    print("=" * 60)
    
    url = f"{WS_URL}?token={JWT_TOKEN}"
    conversation_id = "test-conversation-123"
    
    try:
        async with websockets.connect(url) as websocket:
            # Wait for connected
            await websocket.recv()
            
            # Join conversation
            join_message = {
                "type": "join",
                "conversation_id": conversation_id
            }
            await websocket.send(json.dumps(join_message))
            print(f"\nSent: {json.dumps(join_message, indent=2)}")
            
            # Wait for response
            response = await websocket.recv()
            data = json.loads(response)
            print(f"\nReceived: {json.dumps(data, indent=2)}")
            
            if data.get("type") == "joined" and data.get("success"):
                print("✅ Joined conversation successfully")
                return True
            else:
                print("❌ Failed to join conversation")
                return False
                
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


async def test_typing_indicator():
    """Test typing indicator"""
    print("\n" + "=" * 60)
    print("TEST 4: Typing Indicator")
    print("=" * 60)
    
    url = f"{WS_URL}?token={JWT_TOKEN}"
    conversation_id = "test-conversation-123"
    
    try:
        async with websockets.connect(url) as websocket:
            # Wait for connected
            await websocket.recv()
            
            # Send typing indicator
            typing_message = {
                "type": "typing",
                "conversation_id": conversation_id,
                "is_typing": True
            }
            await websocket.send(json.dumps(typing_message))
            print(f"\nSent: {json.dumps(typing_message, indent=2)}")
            
            # Wait for response
            response = await websocket.recv()
            data = json.loads(response)
            print(f"\nReceived: {json.dumps(data, indent=2)}")
            
            if data.get("type") == "typing_sent" and data.get("success"):
                print("✅ Typing indicator sent successfully")
                return True
            else:
                print("❌ Failed to send typing indicator")
                return False
                
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


async def test_invalid_token():
    """Test connection with invalid token"""
    print("\n" + "=" * 60)
    print("TEST 5: Invalid Token (Should Fail)")
    print("=" * 60)
    
    url = f"{WS_URL}?token=invalid-token"
    print(f"\nConnecting with invalid token...")
    
    try:
        async with websockets.connect(url) as websocket:
            # Should not reach here
            print("❌ Connection accepted with invalid token!")
            return False
            
    except websockets.exceptions.InvalidStatusCode as e:
        if e.status_code in [401, 403, 1008]:
            print(f"✅ Connection rejected as expected (code: {e.status_code})")
            return True
        else:
            print(f"❌ Unexpected status code: {e.status_code}")
            return False
    except Exception as e:
        print(f"✅ Connection rejected: {e}")
        return True


async def run_all_tests():
    """Run all WebSocket tests"""
    print("\n" + "=" * 60)
    print("WEBSOCKET VALIDATION - SPRINT 09")
    print("=" * 60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"URL: {WS_URL}")
    
    results = []
    
    # Test 1: Connection
    results.append(("Connection", await test_websocket_connection()))
    
    # Test 2: Ping/Pong
    results.append(("Ping/Pong", await test_ping_pong()))
    
    # Test 3: Join Conversation
    results.append(("Join Conversation", await test_join_conversation()))
    
    # Test 4: Typing Indicator
    results.append(("Typing Indicator", await test_typing_indicator()))
    
    # Test 5: Invalid Token
    results.append(("Invalid Token", await test_invalid_token()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return False


if __name__ == "__main__":
    # Run tests
    success = asyncio.run(run_all_tests())
    
    # Exit with appropriate code
    exit(0 if success else 1)
