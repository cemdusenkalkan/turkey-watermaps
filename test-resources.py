#!/usr/bin/env python3
"""
Resource verification test for Turkey Water Risk Atlas
Tests that all required files are accessible and properly formatted.
"""

import os
import json
from pathlib import Path
import sys

# Optional: requests for web server testing
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

def test_local_files():
    """Test that all required files exist locally in docs/"""
    print("🔍 Testing local files in docs/ directory...")

    required_files = [
        'docs/index.html',
        'docs/tiles_catchments/metadata.json',
        'docs/data_web/turkey_provinces_web.geojson',
        'docs/data_web/hydrorivers_tr_web_final.geojson',
        'docs/data_web/hydrolakes_tr_web.geojson'
    ]

    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)

    if missing_files:
        print("❌ Missing files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    else:
        print("✅ All required files exist")
        return True

def test_metadata_structure():
    """Test that metadata.json has correct structure"""
    print("\n📊 Testing metadata structure...")

    try:
        with open('docs/tiles_catchments/metadata.json', 'r') as f:
            metadata = json.load(f)

        # Check basic metadata fields
        basic_checks = [
            ('name' in metadata, "Has name field"),
            (metadata.get('format') == 'pbf', "Format is 'pbf'"),
            (int(metadata.get('minzoom', 0)) == 4, f"Min zoom is 4 (got {metadata.get('minzoom')})"),
            (int(metadata.get('maxzoom', 0)) == 10, f"Max zoom is 10 (got {metadata.get('maxzoom')})")
        ]

        # Check vector layers from the embedded JSON string
        vector_layers = None
        if 'json' in metadata:
            try:
                json_data = json.loads(metadata['json'])
                vector_layers = json_data.get('vector_layers', [])
            except:
                pass

        layer_checks = [
            (vector_layers is not None and len(vector_layers) > 0, "Has vector layers in JSON"),
            (vector_layers and vector_layers[0].get('id') == 'aqueduct_baseline_annual_tr_web',
             f"Correct layer ID (got {vector_layers[0].get('id') if vector_layers else 'None'})")
        ]

        all_checks = basic_checks + layer_checks
        passed = 0
        for check, description in all_checks:
            if check:
                print(f"   ✅ {description}")
                passed += 1
            else:
                print(f"   ❌ {description}")

        return passed == len(all_checks)

    except Exception as e:
        print(f"❌ Error reading metadata: {e}")
        return False

def test_geojson_files():
    """Test that GeoJSON files are valid JSON and have expected structure"""
    print("\n🗺️ Testing GeoJSON files...")

    geojson_files = [
        'docs/data_web/turkey_provinces_web.geojson',
        'docs/data_web/hydrorivers_tr_web_final.geojson',
        'docs/data_web/hydrolakes_tr_web.geojson'
    ]

    all_valid = True
    for file_path in geojson_files:
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)

            # Basic structure checks
            if 'type' in data and data['type'] in ['FeatureCollection', 'Feature']:
                print(f"   ✅ {os.path.basename(file_path)} - Valid GeoJSON")
            else:
                print(f"   ❌ {os.path.basename(file_path)} - Invalid GeoJSON structure")
                all_valid = False

        except Exception as e:
            print(f"   ❌ {os.path.basename(file_path)} - Error: {e}")
            all_valid = False

    return all_valid

def test_sample_tiles():
    """Test that sample tile files exist"""
    print("\n🧩 Testing sample tile files...")

    sample_tiles = [
        'docs/tiles_catchments/4/10/6.pbf',
        'docs/tiles_catchments/6/36/23.pbf',
        'docs/tiles_catchments/8/146/95.pbf',
        'docs/tiles_catchments/10/604/401.pbf'
    ]

    existing_tiles = 0
    for tile_path in sample_tiles:
        if os.path.exists(tile_path):
            file_size = os.path.getsize(tile_path)
            print(f"   ✅ {tile_path} - {file_size} bytes")
            existing_tiles += 1
        else:
            print(f"   ❌ {tile_path} - Missing")

    return existing_tiles == len(sample_tiles)

def count_tiles():
    """Count total number of tile files"""
    print("\n📈 Counting tile files...")

    tiles_dir = Path('docs/tiles_catchments')
    if not tiles_dir.exists():
        print("❌ tiles_catchments directory not found")
        return False

    pbf_files = list(tiles_dir.rglob('*.pbf'))
    print(f"   📊 Total tile files: {len(pbf_files)}")

    # Count by zoom level
    zoom_counts = {}
    for pbf_file in pbf_files:
        parts = pbf_file.parts
        try:
            zoom_idx = parts.index('tiles_catchments') + 1
            zoom = parts[zoom_idx]
            zoom_counts[zoom] = zoom_counts.get(zoom, 0) + 1
        except:
            continue

    print("   📊 Tiles by zoom level:")
    for zoom in sorted(zoom_counts.keys()):
        print(f"      Zoom {zoom}: {zoom_counts[zoom]} tiles")

    return len(pbf_files) > 0

def test_web_server(base_url="http://localhost:8000"):
    """Test that web server is responding (optional)"""
    if not HAS_REQUESTS:
        print("\n🌐 Web server test skipped (install requests: pip install requests)")
        return None

    print(f"\n🌐 Testing web server at {base_url}...")

    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            print(f"   ✅ Web server responding (status {response.status_code})")
            return True
        else:
            print(f"   ❌ Web server error (status {response.status_code})")
            return False
    except Exception as e:
        print(f"   ⚠️ Web server not accessible: {e}")
        print("   💡 Start server with: cd docs && python -m http.server 8000")
        return None

def main():
    """Run all tests"""
    print("🧪 Turkey Water Risk Atlas - Resource Verification Tests")
    print("=" * 60)

    tests = [
        ("Local Files", test_local_files),
        ("Metadata Structure", test_metadata_structure),
        ("GeoJSON Files", test_geojson_files),
        ("Sample Tiles", test_sample_tiles),
        ("Tile Count", count_tiles),
        ("Web Server", lambda: test_web_server())
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with error: {e}")
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY:")

    passed = 0
    total = 0
    for test_name, result in results:
        total += 1
        if result is True:
            print(f"   ✅ {test_name}")
            passed += 1
        elif result is None:
            print(f"   ⚠️ {test_name} - Skipped")
        else:
            print(f"   ❌ {test_name}")

    success_rate = (passed / total) * 100
    print(f"\n🎯 Overall: {passed}/{total} tests passed ({success_rate:.1f}%)")

    if success_rate == 100:
        print("🎉 All tests passed! Your water risk atlas is ready to deploy.")
        return 0
    elif success_rate >= 80:
        print("⚠️ Most tests passed. Check the failed tests before deploying.")
        return 1
    else:
        print("❌ Many tests failed. Fix the issues before deploying.")
        return 2

if __name__ == "__main__":
    sys.exit(main())
