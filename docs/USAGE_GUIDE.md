# 📘 Usage Guide - API Log Viewer

Detailed guide for using the API Log Viewer with Java/Spring application logs.

## 🎯 Understanding the Log Format

### Java/Spring Log Structure

```
08:27:33.453 [http-nio-28080-exec-10] INFO  k.g.t.g.c.BackendInvoiceCntr :: ===========/CINV00101L005 START GET DATA============
```

**Parsed Components:**
- **Time**: `08:27:33.453` (HH:MM:SS.mmm)
- **Thread**: `http-nio-28080-exec-10`
- **Level**: `INFO`
- **Logger**: `k.g.t.g.c.BackendInvoiceCntr`
- **Service**: `BackendInvoiceCntr`
- **Endpoint**: `/CINV00101L005`
- **Method**: `POST` (default when not specified)
- **Operation**: `START`

### Error Log Structure

```
08:27:34.001 [http-nio-28080-exec-10] ERROR kh.gov.tax.gdtict.util.ApiLogCls :: ===========BackendInvoiceCntr: CINV00101L005 START RROR LOG============
08:27:34.001 [http-nio-28080-exec-10] ERROR kh.gov.tax.gdtict.util.ApiLogCls :: RSLT_CD[719]
08:27:34.001 [http-nio-28080-exec-10] ERROR kh.gov.tax.gdtict.util.ApiLogCls :: RSLT_MSG[DATA NOT FOUND.]
```

**Parsed Components:**
- **Controller**: `BackendInvoiceCntr`
- **Endpoint**: `/CINV00101L005`
- **Status Code**: `404` (mapped from RSLT_CD[719])
- **Message**: `DATA NOT FOUND.`

## 🚀 Quick Start

### 1. Load the Log File

```bash
python main.py examples/sample_api_format.log
```

### 2. View Summary

```
› summary
```

**Output:**
```
┌─────────────────────────┬───────────────────────────────────────────────┐
│ Metric                  │ Value                                         │
├─────────────────────────┼───────────────────────────────────────────────┤
│ Total Entries           │ 120                                           │
│ File Size               │ 45.23 KB                                      │
│ Log Levels              │ ERROR: 45, INFO: 75                           │
│ HTTP Methods            │ POST: 120                                     │
│ Status Codes            │ 404: 30, 200: 45                              │
│ Top Threads             │ http-nio-28080: 80, SimpleAsyncTaskExecutor: 40│
│ Top Services            │ BackendInvoiceCntr: 50, InvoiceDataEntryCntr: 30│
└─────────────────────────┴───────────────────────────────────────────────┘
```

### 3. List Entries

```
› list 20
```

**Output shows:**
- Line number
- Timestamp (millisecond precision)
- Log level (color-coded)
- Thread name
- Service/Controller name
- HTTP method
- API endpoint
- Status code (color-coded)
- Formatted message

## 🔍 Filtering Examples

### Filter by Log Level

```
› filter level ERROR
› list
```

Shows only ERROR level logs.

### Filter by Thread

```
› filter thread http-nio-28080
› list
```

Shows all logs from HTTP request handling threads.

### Filter by Service

```
› filter service BackendInvoiceCntr
› list
```

Shows all logs from the BackendInvoiceCntr service.

### Filter by Status Code

```
› filter status 404
› list
```

Shows all 404 errors (including RSLT_CD[719] which maps to 404).

### Search for Text

```
› filter search DATA NOT FOUND
› list
```

**Unicode search:**
```
› filter search ážœáž·ážšáŸˆ
› list
```

### Combined Filtering

```
› filter level ERROR
› filter service BackendInvoiceCntr
› list
```

## 📊 Detailed View

### View Single Entry

```
› view 12
```

**Output:**
```
╭─────────────────────── Entry #12 ───────────────────────╮
│ Line Number: 12                                          │
│ Timestamp: 2026-01-21 08:27:34.001000                   │
│ Level: ERROR                                             │
│ Thread: http-nio-28080-exec-10                          │
│ Logger: kh.gov.tax.gdtict.util.ApiLogCls                │
│ Service: BackendInvoiceCntr                              │
│ Method: POST                                             │
│ Endpoint: /CINV00101L005                                │
│ Status Code: 404                                         │
│ Response Time: N/A ms                                    │
│                                                          │
│ Message:                                                 │
│ START - /CINV00101L005                                  │
│                                                          │
│ Raw Log:                                                 │
╰──────────────────────────────────────────────────────────╯
╭────────────────────── Raw Line ──────────────────────────╮
│ 08:27:34.001 [http-nio-28080-exec-10] ERROR            │
│ kh.gov.tax.gdtict.util.ApiLogCls ::                     │
│ ===========BackendInvoiceCntr: CINV00101L005            │
│ START RROR LOG============                               │
╰──────────────────────────────────────────────────────────╯
```

## 💾 Export Filtered Results

### Export Errors Only

```
› filter level ERROR
› export errors_only.log
```

**Result:** Creates `errors_only.log` with all ERROR entries.

### Export by Time Range

```
› filter search 08:27
› export morning_logs.log
```

### Export Specific Service Errors

```
› filter service BackendInvoiceCntr
› filter level ERROR
› export backend_errors.log
```

## 🔧 Advanced Usage

### Analyze Request Flow

To trace a request through multiple log entries:

```
› filter thread http-nio-28080-exec-10
› list 50
```

This shows all logs for a specific request thread.

### Find All Failed Requests

```
› filter status 404
› summary
```

Shows statistics of all 404 errors.

### Monitor Specific Endpoint

```
› filter search CINV00101L005
› list
```

Shows all logs related to the CINV00101L005 endpoint.

### Check Unicode Data Processing

```
› filter search ážœáž·ážšáŸˆ áž"áŸŠáž»áž"ážáž¶áŸ†
› view 17
```

View entries containing Khmer text to verify proper Unicode handling.

## 🎨 Understanding Color Coding

### Log Levels
- 🔵 **DEBUG** - Cyan
- 🟢 **INFO** - Green
- 🟡 **WARN** - Yellow
- 🔴 **ERROR** - Red
- 🔴 **CRITICAL** - Bright Red

### Status Codes
- 🟢 **2xx** (Success) - Green
- 🔵 **3xx** (Redirect) - Blue
- 🟡 **4xx** (Client Error) - Yellow
- 🔴 **5xx** (Server Error) - Red

## 📝 Editing Logs

### Edit an Entry

```
› view 25
› edit 25
Enter new content: 08:27:34.001 [http-nio-28080-exec-10] INFO  k.g.t.g.c.BackendInvoiceCntr :: Fixed entry
› save
```

## 💡 Pro Tips

### 1. Quick Error Analysis

```
› filter level ERROR
› summary
```

Gives you immediate overview of all errors.

### 2. Thread Tracking

```
› filter thread exec-10
› list 100
```

Follow a single request through the entire log.

### 3. Service Performance

```
› filter service BackendInvoiceCntr
› filter search STOP
› list
```

See all completed operations for a service.

### 4. Finding Patterns

```
› filter search DATA NOT FOUND
› export not_found_errors.log
```

Collect all instances of a specific error.

### 5. Time-Based Analysis

```
› filter search 08:27
› list 50
```

Focus on logs from a specific time period.

## 🐛 Troubleshooting

### Issue: No Method Shown

**Solution:** The tool defaults to POST when no method is explicitly mentioned. This is by design for Java/Spring logs.

### Issue: Unicode Characters Not Displaying

**Solution:** Ensure your terminal supports UTF-8 encoding:
```bash
export LANG=en_US.UTF-8
```

### Issue: Large Files Loading Slowly

**Solution:** Use filtering immediately after load:
```bash
python main.py large.log
› filter level ERROR  # Reduces dataset
› list
```

## 📚 Common Workflows

### Daily Error Review
```
› filter level ERROR
› summary
› list 50
› export daily_errors_$(date +%Y%m%d).log
```

### Performance Investigation
```
› filter service BackendInvoiceCntr
› filter search START
› list
```

### Client Request Tracking
```
› filter thread http-nio-28080-exec-4
› list 100
› export request_trace.log
```

---

**For more help, type `help` inside the application!**