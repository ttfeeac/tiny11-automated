#!/usr/bin/env python3
"""
UUP Dump API Test & Debug Script
Author: kelexine (https://github.com/kelexine)

Quick test script to debug API responses and data structure
"""

import json
import requests
from pprint import pprint

def test_uupdump_api():
    """Test UUP Dump API and show response structure"""
    
    print("🔍 Testing UUP Dump API...")
    print("=" * 60)
    
    try:
        # Make API request
        response = requests.get(
            "https://api.uupdump.net/listid.php",
            params={
                'search': 'Windows 11',
                'sortByDate': '1'
            },
            timeout=30
        )
        
        print(f"✅ HTTP Status: {response.status_code}")
        print(f"✅ Content-Type: {response.headers.get('Content-Type')}")
        print()
        
        # Parse JSON
        data = response.json()
        
        # Show top-level structure
        print("📦 Response Structure:")
        print(f"   Type: {type(data)}")
        print(f"   Keys: {list(data.keys()) if isinstance(data, dict) else 'N/A'}")
        print()
        
        # Dive into response
        if 'response' in data:
            resp = data['response']
            print("📦 Response.response Structure:")
            print(f"   Type: {type(resp)}")
            print(f"   Keys: {list(resp.keys()) if isinstance(resp, dict) else 'N/A'}")
            print()
            
            # Check builds
            if 'builds' in resp:
                builds = resp['builds']
                print("📦 Builds Structure:")
                print(f"   Type: {type(builds)}")
                
                if isinstance(builds, dict):
                    print(f"   Keys (sample): {list(builds.keys())[:10]}")
                    print(f"   Total builds: {len(builds)}")
                elif isinstance(builds, list):
                    print(f"   Length: {len(builds)}")
                print()
                
                # Show first build
                if isinstance(builds, dict):
                    first_key = list(builds.keys())[0] if builds else None
                    if first_key:
                        print(f"📦 First Build (key='{first_key}'):")
                        pprint(builds[first_key], indent=2)
                        print()
                elif isinstance(builds, list) and len(builds) > 0:
                    print("📦 First Build Example:")
                    pprint(builds[0], indent=2)
                    print()
                    
                # Count Windows 11 builds
                win11_count = 0
                win11_amd64_count = 0
                
                # Handle both dict and list formats
                builds_iter = builds.values() if isinstance(builds, dict) else builds
                
                for idx, build in enumerate(builds_iter):
                    if idx >= 30:
                        break
                        
                    title = build.get('title', '')
                    arch = build.get('arch', '')
                    
                    if 'Windows 11' in title:
                        win11_count += 1
                        if arch == 'amd64':
                            win11_amd64_count += 1
                
                print(f"📊 Statistics (first 30):")
                print(f"   Windows 11 builds: {win11_count}")
                print(f"   Windows 11 x64 builds: {win11_amd64_count}")
                print()
                
                # Show some Windows 11 x64 builds
                print("📋 Windows 11 x64 Builds:")
                count = 0
                
                builds_iter = builds.values() if isinstance(builds, dict) else builds
                
                for idx, build in enumerate(builds_iter):
                    if idx >= 30:
                        break
                        
                    title = build.get('title', '')
                    arch = build.get('arch', '')
                    build_num = build.get('build', 'Unknown')
                    uuid = build.get('uuid', 'Unknown')
                    
                    if 'Windows 11' in title and arch == 'amd64':
                        count += 1
                        print(f"   {count}. {title}")
                        print(f"      Build: {build_num}, UUID: {uuid}, Arch: {arch}")
                        if count >= 5:
                            break
        
        print()
        print("=" * 60)
        print("✅ Test completed successfully!")
        
        # Save full response for debugging
        with open('uupdump_response_debug.json', 'w') as f:
            json.dump(data, f, indent=2)
        print("💾 Full response saved to: uupdump_response_debug.json")
        
    except requests.RequestException as e:
        print(f"❌ Network error: {e}")
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}")
        print(f"   Response text: {response.text[:500]}")
    except Exception as e:
        print(f"❌ Unexpected error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()


def test_specific_build(build_id):
    """Test fetching details for a specific build"""
    
    print(f"🔍 Fetching details for build: {build_id}")
    print("=" * 60)
    
    try:
        response = requests.get(
            "https://api.uupdump.net/get.php",
            params={
                'id': build_id,
                'pack': 'en-us',
                'edition': 'professional'
            },
            timeout=30
        )
        
        data = response.json()
        
        print("📦 Build Details:")
        pprint(data, indent=2)
        
        # Save to file
        filename = f'build_{build_id}_details.json'
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"\n💾 Details saved to: {filename}")
        
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        # Test specific build ID
        test_specific_build(sys.argv[1])
    else:
        # Test main API
        test_uupdump_api()