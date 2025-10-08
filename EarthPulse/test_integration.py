#!/usr/bin/env python3
"""
Integration Test Script for Earth Observation Visualizer
Tests the complete backend-frontend integration
"""

import asyncio
import httpx
import json
import sys
from datetime import datetime

class IntegrationTester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)
        
    async def test_backend_health(self):
        """Test backend health check"""
        print("🔍 Testing Backend Health...")
        
        try:
            response = await self.client.get(f"{self.base_url}/health")
            if response.status_code == 200:
                print("✅ Backend is healthy")
                return True
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Backend connection failed: {e}")
            return False
    
    async def test_api_info(self):
        """Test API information endpoint"""
        print("🔍 Testing API Information...")
        
        try:
            response = await self.client.get(f"{self.base_url}/api/v1/info")
            if response.status_code == 200:
                data = response.json()
                print("✅ API info retrieved successfully")
                print(f"   • API Version: {data.get('api_version')}")
                print(f"   • Integration Ready: {data.get('integration_ready')}")
                print(f"   • Supported Indicators: {len(data.get('data_indicators', {}))}")
                return True
            else:
                print(f"❌ API info failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ API info error: {e}")
            return False
    
    async def test_environmental_endpoints(self):
        """Test environmental data endpoints"""
        print("🔍 Testing Environmental Data Endpoints...")
        
        endpoints = [
            "/environmental/ndvi/2020?region=nepal_himalayas",
            "/environmental/glacier/2020?region=nepal_himalayas", 
            "/environmental/urban/2020?region=nepal_himalayas",
            "/environmental/temperature/2020?region=nepal_himalayas"
        ]
        
        success_count = 0
        
        for endpoint in endpoints:
            try:
                response = await self.client.get(f"{self.base_url}/api/v1{endpoint}")
                if response.status_code == 200:
                    data = response.json()
                    indicator = endpoint.split('/')[1]
                    print(f"✅ {indicator.upper()} data retrieved")
                    success_count += 1
                else:
                    print(f"❌ {endpoint} failed: {response.status_code}")
            except Exception as e:
                print(f"❌ {endpoint} error: {e}")
        
        print(f"Environmental endpoints: {success_count}/4 successful")
        return success_count == 4
    
    async def test_map_services(self):
        """Test map services endpoints"""
        print("🔍 Testing Map Services...")
        
        try:
            response = await self.client.get(f"{self.base_url}/api/v1/maps/regions")
            if response.status_code == 200:
                data = response.json()
                regions = data.get('regions', [])
                print(f"✅ Map regions retrieved: {len(regions)} regions")
                print(f"   • Default region: {data.get('default_region')}")
                return True
            else:
                print(f"❌ Map regions failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Map regions error: {e}")
            return False
    
    async def test_reports_generation(self):
        """Test report generation"""
        print("🔍 Testing Report Generation...")
        
        report_request = {
            "report_type": "summary",
            "year": 2020,
            "region": "nepal_himalayas",
            "indicators": ["ndvi", "glacier"],
            "include_charts": True,
            "include_maps": True
        }
        
        try:
            response = await self.client.post(
                f"{self.base_url}/api/v1/reports/generate",
                json=report_request
            )
            if response.status_code == 200:
                data = response.json()
                print("✅ Report generation successful")
                print(f"   • Report ID: {data.get('report_id')}")
                print(f"   • Pages: {data.get('preview', {}).get('pages')}")
                return True
            else:
                print(f'❌ Report generation failed: {response.status_code}')
                return False
        except Exception as e:
            print(f"❌ Report generation error: {e}")
            return False

    async def test_performance(self):
        """Test API performance"""
        print("🔍 Testing API Performance...")
        
        start_time = datetime.now()
        
        # Concurrent requests
        tasks = []
        for year in range(2020, 2025):
            tasks.append(self.client.get(f"{self.base_url}/api/v1/environmental/summary?year={year}&region=nepal_himalayas"))
        
        try:
            responses = await asyncio.gather(*tasks)
            end_time = datetime.now()
            
            successful = sum(1 for r in responses if r.status_code == 200)
            duration = (end_time - start_time).total_seconds()
            
            print(f"✅ Performance test completed")
            print(f"   • Successful requests: {successful}/5")
            print(f"   • Duration: {duration:.2f}s")
            print(f"   • Average response time: {duration/5:.2f}s")
            
            return successful >= 4
        except Exception as e:
            print(f"❌ Performance test error: {e}")
            return False
    
    async def run_all_tests(self):
        """Run all integration tests"""
        print("🌍 Earth Observation Visualizer - Integration Test")
        print("=" * 60)
        
        tests = [
            ("Backend Health", self.test_backend_health),
            ("API Information", self.test_api_info),
            ("Environmental Data", self.test_environmental_endpoints),
            ("Map Services", self.test_map_services),
            ("Report Generation", self.test_reports_generation),
            ("Performance", self.test_performance)
        ]
        
        results = []
        
        for test_name, test_func in tests:
            print(f"\n{test_name}:")
            try:
                result = await test_func()
                results.append((test_name, result))
            except Exception as e:
                print(f"❌ {test_name} failed with exception: {e}")
                results.append((test_name, False))
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 INTEGRATION TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for _, result in results if result)
        total = len(results)
        
        for test_name, result in results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} - {test_name}")
        
        print(f"\nOverall: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! Integration is working correctly.")
            print("🚀 Your Earth Observation Visualizer is ready!")
        elif passed >= total * 0.7:
            print("⚠️  Most tests passed. Minor issues detected.")
            print("🔧 Check failed tests for details.")
        else:
            print("❌ Multiple test failures detected.")
            print("🛠️  Please check your setup and configuration.")
        
        return passed >= total * 0.7

    async def close(self):
        """Close client connections"""
        await self.client.aclose()

async def main():
    """Main test runner"""
    backend_url = "http://localhost:8000"
    
    if len(sys.argv) > 1:
        backend_url = sys.argv[1]
    
    tester = IntegrationTester(backend_url)
    
    try:
        success = await tester.run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n👋 Tests interrupted by user")
        sys.exit(1)
    finally:
        await tester.close()

if __name__ == "__main__":
    asyncio.run(main())
