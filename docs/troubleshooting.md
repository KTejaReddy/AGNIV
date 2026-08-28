# AGNIV Troubleshooting Guide

## Common Issues

### 1. High Memory Usage Warning
If you see a `SYSTEM_WARNING` for high memory usage, AGNIV is consuming over 1GB of RAM.
**Solution:** Check the Extensions Dashboard for poorly optimized UI Panels or Integration loops. Try disabling extensions one by one.

### 2. AGNIV Keeps Booting into Safe Mode
AGNIV records consecutive crashes in `logs/crash_state.json`. If it crashes 3 times in a row, it enters Safe Mode.
**Solution:** 
- In Safe Mode, external extensions are skipped. 
- Check `task-*.log` in your `.gemini` logs for stack traces.
- To exit Safe Mode manually, delete the `logs/crash_state.json` file and restart.

### 3. Port 8000 Already in Use
**Error:** `[Errno 10048] error while attempting to bind on address ('0.0.0.0', 8000)`
**Solution:** Another instance of AGNIV or another server is running. Kill the process using port 8000.

### 4. Extensions Fail to Load
If an extension throws an error on boot:
- Ensure the `agniv-extension.json` is properly formatted (valid JSON).
- Verify that `entry_point` points to a real Python file.
- Check that the extension is not trying to directly import `app.*` outside the SDK. The `security_audit.py` script catches this.
