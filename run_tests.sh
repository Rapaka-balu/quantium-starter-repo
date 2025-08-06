#!/bin/bash

# Step 1: Activate virtual environment
source .venv/Scripts/activate

# Step 2: Run the tests
pytest test_app.py --html=report.html --self-contained-html

# Step 3: Return success or failure code
if [ $? -eq 0 ]; then
    echo "✅ All tests passed."
    exit 0
else
    echo "❌ Tests failed."
    exit 1
fi
./run_tests.sh
