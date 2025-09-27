# Alerting & Notification Setup Guide

This guide explains how to configure production alerting and notification systems for your TRAE AI application.

## Overview

The application includes a comprehensive alerting system with multiple notification channels:
- **Slack** - Real-time notifications for all alert types
- **Email** - Critical and high-priority alerts
- **PagerDuty** - Critical alerts requiring immediate response
- **SMS/Twilio** - Optional SMS notifications for critical alerts

## 🚨 Critical Setup Steps

### 1. Slack Integration

#### Create Slack Webhook
1. Go to https://api.slack.com/apps
2. Create a new app or select existing app
3. Navigate to "Incoming Webhooks"
4. Create webhooks for these channels:
   - `#alerts` (general alerts)
   - `#critical-alerts` (critical issues)
   - `#high-priority-alerts` (high priority issues)
   - `#scaling-events` (scaling notifications)
   - `#performance-alerts` (performance issues)
   - `#infrastructure-alerts` (infrastructure issues)

#### Configure Environment Variable
```bash
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

### 2. Email Alerts (SMTP)

#### Gmail Setup (Recommended)
1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"

#### Configure SMTP Variables
```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Alert email addresses
ALERT_EMAIL_FROM=alerts@your-domain.com
ALERT_EMAIL_TO=admin@your-domain.com,ops@your-domain.com
CRITICAL_ALERT_EMAIL=critical@your-domain.com
HIGH_PRIORITY_EMAIL=high-priority@your-domain.com
```

#### Alternative SMTP Providers
- **SendGrid**: `smtp.sendgrid.net:587`
- **Mailgun**: `smtp.mailgun.org:587`
- **AWS SES**: `email-smtp.region.amazonaws.com:587`

### 3. PagerDuty Integration (Critical Alerts)

#### Setup PagerDuty
1. Create PagerDuty account at https://www.pagerduty.com
2. Create a new service
3. Get integration key from service settings
4. Create separate service for security alerts

#### Configure PagerDuty Variables
```bash
PAGERDUTY_INTEGRATION_KEY=your-pagerduty-integration-key
PAGERDUTY_SECURITY_KEY=your-pagerduty-security-key
```

### 4. SMS Notifications (Optional)

#### Twilio Setup
1. Create Twilio account at https://www.twilio.com
2. Get Account SID and Auth Token
3. Purchase phone number for sending SMS

#### Configure Twilio Variables
```bash
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_FROM_NUMBER=+1234567890
ALERT_SMS_NUMBERS=+1234567890,+0987654321
```

## 📋 Production Deployment Checklist

### Pre-Deployment
- [ ] Create Slack webhooks for all required channels
- [ ] Set up SMTP credentials (Gmail App Password recommended)
- [ ] Configure PagerDuty services and get integration keys
- [ ] Set up Twilio account (if SMS alerts needed)
- [ ] Test all notification channels in staging environment

### Environment Configuration
- [ ] Copy `.env.production.template` to `.env.production`
- [ ] Fill in all `REPLACE_WITH_*` placeholders
- [ ] Verify database URL points to PostgreSQL (not SQLite)
- [ ] Ensure all secrets are externalized (no hardcoded values)
- [ ] Set strong passwords and API keys

### Security Verification
- [ ] Rotate default admin password
- [ ] Generate new SECRET_KEY, JWT_SECRET, TRAE_MASTER_KEY
- [ ] Verify `.env.production` is in `.gitignore`
- [ ] Use environment-specific secrets in CI/CD pipeline
- [ ] Enable HTTPS and secure cookies

### Alert Testing
- [ ] Test Slack notifications
- [ ] Test email alerts (critical and high-priority)
- [ ] Test PagerDuty integration
- [ ] Test SMS notifications (if configured)
- [ ] Verify alert routing rules work correctly

## 🔧 Alert Configuration

### Alert Severity Levels

| Severity | Channels | Response Time | Examples |
|----------|----------|---------------|----------|
| **Critical** | Slack + Email + PagerDuty + SMS | Immediate | Service down, security breach |
| **High** | Slack + Email | 15 minutes | High error rate, performance degradation |
| **Medium** | Slack | 1 hour | Scaling events, resource warnings |
| **Low** | Slack | 4 hours | Info notifications, maintenance |

### Alert Categories

- **Infrastructure**: Server health, resource usage, connectivity
- **Performance**: Response times, throughput, resource consumption
- **Security**: Authentication failures, suspicious activity, breaches
- **Scaling**: Auto-scaling events, capacity changes
- **Application**: Business logic errors, feature failures

## 🚀 Testing Your Setup

### Manual Testing
```bash
# Test Slack webhook
curl -X POST -H 'Content-type: application/json' \
  --data '{"text":"Test alert from TRAE AI"}' \
  $SLACK_WEBHOOK_URL

# Test email (using Python)
python -c "
import smtplib
from email.mime.text import MIMEText

smtp = smtplib.SMTP('smtp.gmail.com', 587)
smtp.starttls()
smtp.login('your-email@gmail.com', 'your-app-password')

msg = MIMEText('Test alert from TRAE AI')
msg['Subject'] = 'Test Alert'
msg['From'] = 'alerts@your-domain.com'
msg['To'] = 'admin@your-domain.com'

smtp.send_message(msg)
smtp.quit()
print('Email sent successfully')
"
```

### Automated Testing
The monitoring system includes built-in health checks that will trigger test alerts when started.

## 📚 Troubleshooting

### Common Issues

1. **Slack webhooks not working**
   - Verify webhook URL is correct
   - Check Slack app permissions
   - Ensure channels exist

2. **Email alerts failing**
   - Verify SMTP credentials
   - Check Gmail App Password (not regular password)
   - Ensure 2FA is enabled for Gmail

3. **PagerDuty not receiving alerts**
   - Verify integration key
   - Check service configuration
   - Ensure escalation policies are set

4. **SMS not sending**
   - Verify Twilio credentials
   - Check phone number format (+1234567890)
   - Ensure Twilio account has sufficient balance

### Log Locations
- AlertManager logs: `/var/log/alertmanager/`
- Application logs: `/var/log/trae-ai/`
- Monitoring system logs: Check running processes

## 🔒 Security Best Practices

1. **Never commit secrets to version control**
2. **Use environment-specific credentials**
3. **Rotate API keys regularly**
4. **Limit webhook permissions**
5. **Monitor alert system health**
6. **Use secure SMTP connections (TLS)**
7. **Implement rate limiting for alerts**

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review application and AlertManager logs
3. Test individual notification channels
4. Verify environment variable configuration

For production deployments, ensure all notification channels are tested and working before going live.