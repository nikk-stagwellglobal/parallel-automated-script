#!/bin/bash


API_URL="http://localhost:8000/api/v1"

echo "Testing Lucene Query Parser API - Clean Architecture Version"
echo "============================================================="
echo ""

echo "Test 1: Health check"
curl -s -X GET "http://localhost:8000/healthz" | jq '.'
echo ""
echo ""

echo "Test 2: Simple word query (JSON endpoint)"
curl -s -X POST "$API_URL/parse" \
  -H "Content-Type: application/json" \
  -d '{"query": "test"}' | jq '.'
echo ""
echo ""

echo "Test 3: OR operation with phrases (JSON endpoint)"
curl -s -X POST "$API_URL/parse" \
  -H "Content-Type: application/json" \
  -d '{"query": "(\"H.B. Fuller\" OR \"Arkema\")"}' | jq '.'
echo ""
echo ""

echo "Test 4: Complex query with NOT (JSON endpoint)"
curl -s -X POST "$API_URL/parse" \
  -H "Content-Type: application/json" \
  -d '{"query": "(\"H.B. Fuller\" OR \"Arkema\") NOT \"Albemarle County\""}' | jq '.'
echo ""
echo ""

echo "Test 5: Field-specific search (JSON endpoint)"
curl -s -X POST "$API_URL/parse" \
  -H "Content-Type: application/json" \
  -d '{"query": "headline:(\"Gallery\" OR \"Research and markets\")"}' | jq '.'
echo ""
echo ""

echo "Test 6: File upload - simple query"
curl -s -X POST "$API_URL/parse-file" \
  -F "file=@queries/simple_query.txt" | jq '.'
echo ""
echo ""

echo "Test 7: File upload - complex query"
curl -s -X POST "$API_URL/parse-file" \
  -F "file=@queries/complex_query.txt" | jq '.'
echo ""
echo ""

echo "Test 8: File upload - field search"
curl -s -X POST "$API_URL/parse-file" \
  -F "file=@queries/field_search.txt" | jq '.'
echo ""
echo ""

echo "Test 9: Pydantic validation - empty query (should fail)"
curl -s -X POST "$API_URL/parse" \
  -H "Content-Type: application/json" \
  -d '{"query": ""}' | jq '.'
echo ""
echo ""

echo "Test 10: Invalid Lucene syntax (should fail)"
curl -s -X POST "$API_URL/parse" \
  -H "Content-Type: application/json" \
  -d '{"query": "((unclosed"}' | jq '.'
echo ""
echo ""

echo "All tests completed!"
echo ""
echo "Check logs/app.log for detailed logging output"
