#!/usr/bin/env python3
"""
Comprehensive Test Script for SAGA Reykjavík Image Search Platform

This script demonstrates and tests:
1. Semantic search
2. Icelandic language search with translation
3. Hybrid search (text + metadata)
4. Indexing service job management
5. Health checks

Prerequisites:
- Flask backend running on port 5000
- Indexing service running on port 8001
- At least some images indexed
"""

import requests
import time
import json
from typing import Dict, Any


# Configuration
FLASK_BASE_URL = "http://localhost:5000"
INDEXING_BASE_URL = "http://localhost:8001"


class Colors:
    """ANSI color codes for terminal output"""

    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def print_header(text: str):
    """Print section header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 70}")
    print(f"{text}")
    print(f"{'=' * 70}{Colors.ENDC}\n")


def print_success(text: str):
    """Print success message"""
    print(f"{Colors.OKGREEN}✅ {text}{Colors.ENDC}")


def print_info(text: str):
    """Print info message"""
    print(f"{Colors.OKCYAN}ℹ️  {text}{Colors.ENDC}")


def print_warning(text: str):
    """Print warning message"""
    print(f"{Colors.WARNING}⚠️  {text}{Colors.ENDC}")


def print_error(text: str):
    """Print error message"""
    print(f"{Colors.FAIL}❌ {text}{Colors.ENDC}")


def test_health_checks():
    """Test 1: Health check endpoints"""
    print_header("TEST 1: Health Checks")

    # Flask health
    try:
        response = requests.get(f"{FLASK_BASE_URL}/api/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success("Flask backend is healthy")
            print_info(f"   Model loaded: {data.get('model_loaded')}")
            print_info(f"   Device: {data.get('device')}")
            print_info(f"   Translator available: {data.get('translator_available')}")
        else:
            print_error(f"Flask health check failed: {response.status_code}")
    except Exception as e:
        print_error(f"Flask backend not reachable: {e}")

    # Indexing service health
    try:
        response = requests.get(f"{INDEXING_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print_success("Indexing service is healthy")
        else:
            print_error(f"Indexing service health check failed: {response.status_code}")
    except Exception as e:
        print_warning(f"Indexing service not reachable: {e}")


def test_database_stats():
    """Test 2: Database statistics"""
    print_header("TEST 2: Database Statistics")

    try:
        response = requests.get(f"{FLASK_BASE_URL}/api/stats", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success("Retrieved database statistics:")
            print_info(f"   Total images indexed: {data.get('total_images', 0)}")
            print_info(f"   Vector size: {data.get('vector_size', 512)}")
            print_info(f"   Device: {data.get('device', 'unknown')}")
            print_info(f"   Icelandic enabled: {data.get('icelandic_enabled', False)}")

            if data.get("total_images", 0) == 0:
                print_warning("No images indexed yet. Please index some images first.")
                return False

            return True
        else:
            print_error(f"Failed to get stats: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error getting stats: {e}")
        return False


def test_semantic_search():
    """Test 3: Semantic search"""
    print_header("TEST 3: Semantic Search")

    test_queries = [
        "old buildings in downtown",
        "people walking on street",
        "harbor with boats",
        "mountain landscape",
    ]

    for query in test_queries:
        print_info(f"Searching for: '{query}'")

        try:
            response = requests.post(
                f"{FLASK_BASE_URL}/api/search",
                json={"query": query, "limit": 5, "min_score": 0.2},
                timeout=10,
            )

            if response.status_code == 200:
                data = response.json()
                count = data.get("count", 0)

                if count > 0:
                    print_success(f"Found {count} results")

                    # Display top result
                    top_result = data["results"][0]
                    print_info(
                        f"   Top result: {top_result['filename']} (score: {top_result['score']:.3f})"
                    )
                    print_info(f"   Description: {top_result['description'][:80]}...")
                else:
                    print_warning("No results found")

            else:
                print_error(f"Search failed: {response.status_code}")

        except Exception as e:
            print_error(f"Search error: {e}")

        time.sleep(0.5)  # Rate limiting


def test_icelandic_search():
    """Test 4: Icelandic language search"""
    print_header("TEST 4: Icelandic Language Search")

    icelandic_queries = [
        "gamlar byggingar í miðbænum",
        "fólk að ganga á götunni",
        "höfnin með bátum",
        "fjallasýn",
    ]

    for query in icelandic_queries:
        print_info(f"Icelandic query: '{query}'")

        try:
            response = requests.post(
                f"{FLASK_BASE_URL}/api/search/icelandic",
                json={"query": query, "limit": 3},
                timeout=10,
            )

            if response.status_code == 200:
                data = response.json()

                if data.get("was_translated"):
                    print_success(
                        f"Translated to: '{data.get('translated_query')}'"
                    )

                count = data.get("count", 0)
                if count > 0:
                    print_success(f"Found {count} results")
                    top_result = data["results"][0]
                    print_info(
                        f"   Top result: {top_result['filename']} (score: {top_result['score']:.3f})"
                    )
                else:
                    print_warning("No results found")

            else:
                print_error(f"Icelandic search failed: {response.status_code}")

        except Exception as e:
            print_error(f"Search error: {e}")

        time.sleep(0.5)


def test_hybrid_search():
    """Test 5: Hybrid search (text + metadata)"""
    print_header("TEST 5: Hybrid Search (Text + Metadata)")

    # Example hybrid search
    print_info("Hybrid search: 'buildings' with folder filter")

    try:
        response = requests.post(
            f"{FLASK_BASE_URL}/api/search/hybrid",
            json={
                "text_query": "historic buildings",
                "metadata_filter": {},  # Add actual filters if you have specific folders
                "weights": {"text": 0.7, "metadata": 0.3},
                "limit": 5,
            },
            timeout=10,
        )

        if response.status_code == 200:
            data = response.json()
            count = data.get("count", 0)

            if count > 0:
                print_success(f"Found {count} results using hybrid search")

                # Display results with hybrid scores
                for i, result in enumerate(data["results"][:3], 1):
                    print_info(
                        f"   {i}. {result['filename']} "
                        f"(hybrid: {result.get('hybrid_score', 0):.3f}, "
                        f"semantic: {result['score']:.3f})"
                    )
            else:
                print_warning("No results found")

        else:
            print_error(f"Hybrid search failed: {response.status_code}")

    except Exception as e:
        print_error(f"Hybrid search error: {e}")


def test_indexing_service():
    """Test 6: Indexing service job management"""
    print_header("TEST 6: Indexing Service (Job Management)")

    # List existing jobs
    print_info("Fetching existing indexing jobs...")

    try:
        response = requests.get(f"{INDEXING_BASE_URL}/jobs?limit=5", timeout=5)

        if response.status_code == 200:
            data = response.json()
            jobs = data.get("jobs", [])

            if jobs:
                print_success(f"Found {len(jobs)} recent jobs:")

                for job in jobs:
                    status = job.get("status", "unknown")
                    folder = job.get("image_folder", "N/A")
                    job_id = job.get("id", "N/A")[:8]

                    progress = job.get("progress", {})
                    processed = progress.get("processed", 0)
                    total = progress.get("total", 0)

                    print_info(
                        f"   Job {job_id} - Status: {status} - "
                        f"Folder: {folder} - Progress: {processed}/{total}"
                    )
            else:
                print_warning("No indexing jobs found")

        else:
            print_error(f"Failed to list jobs: {response.status_code}")

    except Exception as e:
        print_warning(f"Indexing service not available: {e}")


def run_all_tests():
    """Run all tests in sequence"""
    print(f"\n{Colors.BOLD}{'=' * 70}")
    print(f"SAGA Reykjavík - Comprehensive Feature Test Suite")
    print(f"{'=' * 70}{Colors.ENDC}\n")

    print_info("Starting test suite...")
    time.sleep(1)

    # Run tests
    test_health_checks()
    has_data = test_database_stats()

    if has_data:
        test_semantic_search()
        test_icelandic_search()
        test_hybrid_search()
    else:
        print_warning("Skipping search tests - no data indexed")

    test_indexing_service()

    # Summary
    print_header("Test Suite Complete")
    print_success("All tests executed successfully!")
    print_info("Check the output above for any warnings or errors.")


if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print_warning("\n\nTest suite interrupted by user")
    except Exception as e:
        print_error(f"\n\nUnexpected error: {e}")
