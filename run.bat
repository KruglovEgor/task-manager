@echo off
setlocal

if "%1"=="app" (
    echo Starting Task Manager application...
    docker-compose up app
) else if "%1"=="test" (
    echo Running tests...
    docker-compose up --build tests
) else if "%1"=="stop" (
    echo Stopping all services...
    docker-compose down
) else if "%1"=="clean" (
    echo Cleaning up...
    docker-compose down -v
    docker system prune -f
) else (
    echo Usage: run.bat [app^|test^|stop^|clean]
    echo.
    echo Commands:
    echo   app   - Start the application
    echo   test  - Run tests
    echo   stop  - Stop all services
    echo   clean - Stop and clean up everything
    echo.
    echo Examples:
    echo   run.bat app
    echo   run.bat test
)
