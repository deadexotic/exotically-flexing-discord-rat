# Security Policy

## Token security

Your token is never actually safe but i try to improve the token security per update
so if you are worried either dont use or make sure you download the latest version when making a new client

## Stability Improvements

Version 2.5 includes significant stability enhancements to prevent data loss and system hangs:

- **Critical Bug Fix**: Resolved file truncation issue in builder.py that was causing rat_source.py to be truncated to 317 lines
- **File Integrity Protection**: Added multiple file size verification steps to prevent data loss
- **Fallback Mechanisms**: Implemented automatic fallback to main.py when rat_source.py is corrupted or truncated
- **Timeout Protection**: Added comprehensive timeouts to all network operations and file operations
- **Resource Management**: Implemented proper cleanup and termination of threads, processes, and file handles
- **Error Handling**: Enhanced error handling for all file operations with proper recovery mechanisms
- **Browser Data Extraction**: Optimized stealer function with timeout protection to prevent hanging

## Reporting a Vulnerability

Use the issues tab or contact me on telegram or discord
