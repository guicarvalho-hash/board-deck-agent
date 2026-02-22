"""
Test script to verify Board Deck Agent setup.
"""
import os
import sys
from dotenv import load_dotenv


def test_environment():
    """Test environment variables."""
    print("Testing environment variables...")
    
    load_dotenv()
    
    required_vars = ['OPENAI_API_KEY', 'USER_EMAIL']
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
            print(f"  ✗ {var}: NOT SET")
        else:
            # Mask sensitive values
            if 'KEY' in var or 'TOKEN' in var:
                masked = value[:10] + '...' if len(value) > 10 else '***'
                print(f"  ✓ {var}: {masked}")
            else:
                print(f"  ✓ {var}: {value}")
    
    if missing_vars:
        print(f"\n❌ Missing required variables: {', '.join(missing_vars)}")
        print("Please set these in your .env file")
        return False
    
    print("✓ All required environment variables are set\n")
    return True


def test_credentials():
    """Test Google OAuth credentials."""
    print("Testing Google OAuth credentials...")
    
    if not os.path.exists('credentials.json'):
        print("  ✗ credentials.json: NOT FOUND")
        print("\n❌ Please download OAuth credentials from Google Cloud Console")
        print("   See SETUP.md for instructions")
        return False
    
    print("  ✓ credentials.json: Found")
    
    if os.path.exists('token.json'):
        print("  ✓ token.json: Found (already authenticated)")
    else:
        print("  ℹ token.json: Not found (will authenticate on first run)")
    
    print("✓ Google OAuth credentials configured\n")
    return True


def test_dependencies():
    """Test Python dependencies."""
    print("Testing Python dependencies...")
    
    try:
        import google.auth
        print("  ✓ google-auth")
    except ImportError:
        print("  ✗ google-auth: NOT INSTALLED")
        return False
    
    try:
        from googleapiclient.discovery import build
        print("  ✓ google-api-python-client")
    except ImportError:
        print("  ✗ google-api-python-client: NOT INSTALLED")
        return False
    
    try:
        import openai
        print("  ✓ openai")
    except ImportError:
        print("  ✗ openai: NOT INSTALLED")
        return False
    
    try:
        from dotenv import load_dotenv
        print("  ✓ python-dotenv")
    except ImportError:
        print("  ✗ python-dotenv: NOT INSTALLED")
        return False
    
    try:
        from bs4 import BeautifulSoup
        print("  ✓ beautifulsoup4")
    except ImportError:
        print("  ✗ beautifulsoup4: NOT INSTALLED")
        return False
    
    print("✓ All dependencies installed\n")
    return True


def test_openai_connection():
    """Test OpenAI API connection."""
    print("Testing OpenAI API connection...")
    
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("  ✗ OPENAI_API_KEY not set")
        return False
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        
        # Test with a minimal request
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'test' if you can read this"}],
            max_tokens=5
        )
        
        print("  ✓ OpenAI API connection successful")
        print("✓ OpenAI API is working\n")
        return True
        
    except Exception as e:
        print(f"  ✗ OpenAI API error: {str(e)}")
        print("\n❌ Check your OPENAI_API_KEY")
        return False


def test_data_file():
    """Test data file creation."""
    print("Testing data file...")
    
    load_dotenv()
    data_file = os.getenv('DATA_FILE', 'board_insights.json')
    
    if os.path.exists(data_file):
        print(f"  ✓ {data_file}: Found")
    else:
        print(f"  ℹ {data_file}: Will be created on first run")
    
    # Test write permissions
    try:
        test_file = 'test_write.tmp'
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        print("  ✓ Write permissions: OK")
    except Exception as e:
        print(f"  ✗ Write permissions: FAILED - {e}")
        return False
    
    print("✓ Data file configuration OK\n")
    return True


def main():
    """Run all tests."""
    print("="*70)
    print("BOARD DECK AGENT - SETUP VERIFICATION")
    print("="*70)
    print()
    
    results = []
    
    # Run all tests
    results.append(("Dependencies", test_dependencies()))
    results.append(("Environment Variables", test_environment()))
    results.append(("Google Credentials", test_credentials()))
    results.append(("Data File", test_data_file()))
    results.append(("OpenAI Connection", test_openai_connection()))
    
    # Summary
    print("="*70)
    print("SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print()
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 All tests passed! Your setup is complete.")
        print("\nNext steps:")
        print("  1. Run: python main.py --mode once")
        print("  2. Authenticate with Google (first time only)")
        print("  3. The agent will check for meeting minutes")
        print("\nFor continuous monitoring:")
        print("  python main.py --mode continuous")
    else:
        print("\n❌ Some tests failed. Please fix the issues above.")
        print("\nRefer to SETUP.md for detailed instructions.")
        sys.exit(1)


if __name__ == '__main__':
    main()
