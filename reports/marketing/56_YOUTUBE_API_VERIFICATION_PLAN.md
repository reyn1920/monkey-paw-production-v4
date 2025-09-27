# YouTube API Integration Verification Plan

This document outlines the comprehensive testing and verification steps for the YouTube API integration routes implemented in the TRAE.AI Dashboard.

## Prerequisites

### Environment Setup
1. Copy `.env.example` to `.env` and configure the following YouTube variables:
   ```bash
   # Core YouTube API Configuration
   YOUTUBE_API_KEY=your_youtube_api_key_here
   YOUTUBE_CHANNEL_ID=your_youtube_channel_id_here
   YOUTUBE_CLIENT_ID=your_youtube_client_id_here
   YOUTUBE_CLIENT_SECRET=your_youtube_client_secret_here
   YOUTUBE_REFRESH_TOKEN=your_youtube_refresh_token_here

   # OAuth Configuration
   YT_CLIENT_ID=your_youtube_client_id_here
   YT_CLIENT_SECRET=your_youtube_client_secret_here
   YT_REDIRECT_URI=http://127.0.0.1:8000/oauth2/callback/youtube
   YT_SCOPES="https://www.googleapis.com/auth/youtube.upload https://www.googleapis.com/auth/youtube.readonly https://www.googleapis.com/auth/yt-analytics.readonly"

   # Feature Flags
   FEATURE_YT_UPLOADS=true
   FEATURE_YT_ANALYTICS=true
   FEATURE_AUTO_COMMENTS=false
   FEATURE_AUTO_COMMUNITY_POSTS=false

   # Provider Configuration
   YOUTUBE_PROVIDER_ENABLED=true
   YOUTUBE_PROVIDER_PRIORITY=1
   ```

2. Ensure the dashboard server is running:
   ```bash
   python app/dashboard.py
   ```

## 1. OAuth Authentication Flow Testing

### 1.1 OAuth Initiation Route
**Endpoint:** `GET /youtube/oauth/start`

**Test Steps:**
1. Open browser and navigate to: `http://127.0.0.1:8083/youtube/oauth/start`
2. Verify redirect to Google OAuth consent screen
3. Check that the consent screen requests the correct scopes:
   - YouTube upload permissions
   - YouTube read permissions
   - YouTube Analytics read permissions

**Expected Results:**
- ✅ Successful redirect to Google OAuth
- ✅ Correct scopes displayed
- ✅ No server errors in logs

### 1.2 OAuth Callback Route
**Endpoint:** `GET /oauth2/callback/youtube`

**Test Steps:**
1. Complete the OAuth flow from step 1.1
2. Grant permissions in Google consent screen
3. Verify successful callback handling
4. Check that refresh token is stored securely

**Expected Results:**
- ✅ Successful callback processing
- ✅ Refresh token stored in configuration
- ✅ Success message displayed
- ✅ No sensitive data exposed in response

## 2. Video Upload Route Testing

### 2.1 Upload Route Validation
**Endpoint:** `POST /youtube/upload`

**Test Cases:**

#### Test Case 2.1.1: Valid Upload Request
```bash
curl -X POST http://127.0.0.1:8083/youtube/upload \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Video Upload",
    "description": "This is a test video upload via API",
    "tags": ["test", "api", "youtube"],
    "category_id": "22",
    "privacy_status": "private",
    "video_file_path": "/path/to/test/video.mp4"
  }'
```

**Expected Results:**
- ✅ Returns 200 status code
- ✅ Returns video_id in response
- ✅ Logs upload simulation details

#### Test Case 2.1.2: Missing Required Fields
```bash
curl -X POST http://127.0.0.1:8083/youtube/upload \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Missing title field"
  }'
```

**Expected Results:**
- ✅ Returns 400 status code
- ✅ Error message indicates missing required fields

#### Test Case 2.1.3: Invalid Privacy Status
```bash
curl -X POST http://127.0.0.1:8083/youtube/upload \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Video",
    "description": "Test description",
    "privacy_status": "invalid_status",
    "video_file_path": "/path/to/video.mp4"
  }'
```

**Expected Results:**
- ✅ Returns 400 status code
- ✅ Error message indicates invalid privacy status

## 3. Analytics Route Testing

### 3.1 Analytics Summary Route
**Endpoint:** `GET /youtube/analytics/summary`

**Test Cases:**

#### Test Case 3.1.1: Valid Analytics Request
```bash
curl -X GET "http://127.0.0.1:8083/youtube/analytics/summary?start_date=2024-01-01&end_date=2024-01-31"
```

**Expected Results:**
- ✅ Returns 200 status code
- ✅ Returns analytics data structure with:
  - Channel metrics (views, subscribers, etc.)
  - Video performance data
  - Engagement metrics
  - Revenue data (if monetized)

#### Test Case 3.1.2: Missing Date Parameters
```bash
curl -X GET "http://127.0.0.1:8083/youtube/analytics/summary"
```

**Expected Results:**
- ✅ Returns 200 status code (uses default date range)
- ✅ Returns analytics data for default period

#### Test Case 3.1.3: Invalid Date Format
```bash
curl -X GET "http://127.0.0.1:8083/youtube/analytics/summary?start_date=invalid-date&end_date=2024-01-31"
```

**Expected Results:**
- ✅ Returns 400 status code
- ✅ Error message indicates invalid date format

## 4. Webhook Integration Testing

### 4.1 Webhook Challenge Verification
**Endpoint:** `GET /youtube/webhook`

**Test Steps:**
1. Simulate PubSubHubbub challenge verification:
```bash
curl -X GET "http://127.0.0.1:8083/youtube/webhook?hub.challenge=test_challenge_string&hub.mode=subscribe&hub.topic=https://www.youtube.com/xml/feeds/videos.xml?channel_id=YOUR_CHANNEL_ID"
```

**Expected Results:**
- ✅ Returns the challenge string as response
- ✅ Logs challenge verification
- ✅ Returns 200 status code

### 4.2 Webhook Notification Handling
**Endpoint:** `POST /youtube/webhook`

**Test Steps:**
1. Simulate webhook notification:
```bash
curl -X POST http://127.0.0.1:8083/youtube/webhook \
  -H "Content-Type: application/atom+xml" \
  -d '<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns:yt="http://www.youtube.com/xml/schemas/2015" xmlns="http://www.w3.org/2005/Atom">
  <link rel="hub" href="https://pubsubhubbub.appspot.com"/>
  <link rel="self" href="https://www.youtube.com/xml/feeds/videos.xml?channel_id=CHANNEL_ID"/>
  <title>YouTube video feed</title>
  <updated>2024-01-15T12:00:00+00:00</updated>
  <entry>
    <id>yt:video:VIDEO_ID</id>
    <yt:videoId>VIDEO_ID</yt:videoId>
    <yt:channelId>CHANNEL_ID</yt:channelId>
    <title>New Video Title</title>
    <link rel="alternate" href="http://www.youtube.com/watch?v=VIDEO_ID"/>
    <author>
      <name>Channel Name</name>
      <uri>http://www.youtube.com/channel/CHANNEL_ID</uri>
    </author>
    <published>2024-01-15T12:00:00+00:00</published>
    <updated>2024-01-15T12:00:00+00:00</updated>
  </entry>
</feed>'
```

**Expected Results:**
- ✅ Returns 200 status code
- ✅ Logs notification receipt
- ✅ Processes XML notification data

### 4.3 Webhook Subscription Route
**Endpoint:** `POST /youtube/webhook/subscribe`

**Test Steps:**
1. Test webhook subscription:
```bash
curl -X POST http://127.0.0.1:8083/youtube/webhook/subscribe \
  -H "Content-Type: application/json" \
  -d '{
    "channel_id": "YOUR_CHANNEL_ID",
    "callback_url": "http://127.0.0.1:8083/youtube/webhook"
  }'
```

**Expected Results:**
- ✅ Returns 200 status code
- ✅ Simulates PubSubHubbub subscription
- ✅ Logs subscription attempt

## 5. Error Handling and Edge Cases

### 5.1 Authentication Errors
- Test with invalid/expired OAuth tokens
- Test with missing authentication
- Verify proper error messages and status codes

### 5.2 Rate Limiting
- Test API rate limit handling
- Verify graceful degradation
- Check retry mechanisms

### 5.3 Network Failures
- Test with simulated network timeouts
- Verify error handling for API unavailability
- Check fallback mechanisms

## 6. Security Verification

### 6.1 Secrets Management
- ✅ Verify no API keys in source code
- ✅ Confirm environment variables are used
- ✅ Check that sensitive data is not logged
- ✅ Verify OAuth tokens are stored securely

### 6.2 Input Validation
- ✅ Test SQL injection prevention
- ✅ Test XSS prevention in responses
- ✅ Verify file upload security
- ✅ Check parameter validation

## 7. Performance Testing

### 7.1 Load Testing
- Test concurrent requests to each endpoint
- Monitor response times under load
- Check memory usage during operations

### 7.2 Resource Management
- Verify proper cleanup of temporary files
- Check database connection handling
- Monitor for memory leaks

## 8. Integration Testing

### 8.1 End-to-End Workflow
1. Complete OAuth flow
2. Upload a test video
3. Fetch analytics for the channel
4. Verify webhook notifications
5. Check all data consistency

### 8.2 Dashboard Integration
- Verify routes are accessible from dashboard UI
- Test form submissions and responses
- Check error message display
- Verify success notifications

## 9. Monitoring and Logging

### 9.1 Log Verification
- Check that all operations are logged appropriately
- Verify log levels are correct
- Ensure sensitive data is not logged
- Confirm error logs contain useful debugging information

### 9.2 Metrics Collection
- Verify API usage metrics are collected
- Check performance metrics logging
- Confirm error rate tracking

## 10. Documentation and Maintenance

### 10.1 API Documentation
- Verify all endpoints are documented
- Check parameter descriptions
- Confirm example requests/responses
- Update any outdated information

### 10.2 Configuration Management
- Verify all environment variables are documented
- Check default values are appropriate
- Confirm configuration validation

---

## Verification Checklist Summary

- [ ] OAuth flow works end-to-end
- [ ] Video upload simulation functions correctly
- [ ] Analytics data retrieval works
- [ ] Webhook challenge verification passes
- [ ] Webhook notifications are processed
- [ ] All error cases return appropriate responses
- [ ] Security measures are in place
- [ ] Performance is acceptable
- [ ] Logging is comprehensive
- [ ] Documentation is complete

## Notes

- This verification plan assumes a development/testing environment
- For production deployment, additional security and performance testing is required
- All API keys and tokens should be properly secured before going live
- Consider implementing additional monitoring and alerting for production use
