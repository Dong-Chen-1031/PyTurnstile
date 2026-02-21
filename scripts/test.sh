#!/usr/bin/env bash
# Test helper script

set -e

function help() {
    echo "PyTurnstile Test Script"
    echo ""
    echo "Usage: ./scripts/test.sh [command]"
    echo ""
    echo "Available commands:"
    echo "  all          - Run all tests"
    echo "  cov          - Run tests with coverage report"
    echo "  html         - Generate HTML coverage report"
    echo "  quick        - Quick test (stops on first failure)"
    echo "  watch        - Watch mode (requires pytest-watch)"
    echo "  lint         - Run linter"
    echo "  format       - Format code"
    echo "  format-check - Check code formatting"
    echo "  help         - Show this help message"
}

function run_all() {
    echo "Running all tests..."
    uv run pytest
}

function run_cov() {
    echo "Running tests with coverage..."
    uv run pytest --cov=src/pyturnstile --cov-report=term-missing
}

function run_html() {
    echo "Generating HTML coverage report..."
    uv run pytest --cov=src/pyturnstile --cov-report=html
    echo "HTML report generated at htmlcov/index.html"
}

function run_quick() {
    echo "Running quick tests..."
    uv run pytest -x
}

function run_lint() {
    echo "Running linter..."
    uv run ruff check src/
}

function run_format() {
    echo "Formatting code..."
    uv run ruff format src/
}

function run_format_check() {
    echo "Checking code format..."
    uv run ruff format --check src/
}

# Main logic
case "${1:-all}" in
    all)
        run_all
        ;;
    cov)
        run_cov
        ;;
    html)
        run_html
        ;;
    quick)
        run_quick
        ;;
    lint)
        run_lint
        ;;
    format)
        run_format
        ;;
    format-check)
        run_format_check
        ;;
    help|--help|-h)
        help
        ;;
    *)
        echo "❌ Unknown command: $1"
        echo ""
        help
        exit 1
        ;;
esac
