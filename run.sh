#!/bin/bash

case "$1" in
    "app")
        echo "Starting Task Manager application..."
        docker-compose up app
        ;;
    "test")
        echo "Running tests..."
        docker-compose up --build tests
        ;;
    "stop")
        echo "Stopping all services..."
        docker-compose down
        ;;
    "clean")
        echo "Cleaning up..."
        docker-compose down -v
        docker system prune -f
        ;;
    *)
        echo "Usage: ./run.sh [app|test|stop|clean]"
        echo ""
        echo "Commands:"
        echo "  app   - Start the application"
        echo "  test  - Run tests"
        echo "  stop  - Stop all services"
        echo "  clean - Stop and clean up everything"
        echo ""
        echo "Examples:"
        echo "  ./run.sh app"
        echo "  ./run.sh test"
        ;;
esac
