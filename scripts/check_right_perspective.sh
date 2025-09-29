#!/bin/bash

# Right Perspective Special Check Script
# Verifies "The Right Perspective" channel is properly configured and safe

echo "🎭 Checking 'The Right Perspective' Special Configuration"
echo "======================================================="

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RIGHT_PERSPECTIVE_DIR="$PROJECT_ROOT/channels/_special_right_perspective"
MANIFEST_FILE="$RIGHT_PERSPECTIVE_DIR/branding/channel_manifest.yaml"

echo "📁 Project Root: $PROJECT_ROOT"
echo "📁 Right Perspective: $RIGHT_PERSPECTIVE_DIR"
echo ""

# Check if directory exists
if [ ! -d "$RIGHT_PERSPECTIVE_DIR" ]; then
    echo "❌ Right Perspective directory not found: $RIGHT_PERSPECTIVE_DIR"
    echo "   Creating directory structure..."
    mkdir -p "$RIGHT_PERSPECTIVE_DIR/branding"
    echo "✅ Directory structure created"
fi

# Check if manifest exists
if [ ! -f "$MANIFEST_FILE" ]; then
    echo "❌ Channel manifest not found: $MANIFEST_FILE"
    echo "   This should have been created by the integration process"
    exit 1
fi

echo "✅ Channel manifest found: $MANIFEST_FILE"

# Check critical safety settings
echo ""
echo "🔒 Checking Critical Safety Settings..."

# Check publish_opt_in
if grep -q "publish_opt_in: false" "$MANIFEST_FILE"; then
    echo "✅ publish_opt_in: false (SAFE - no auto-publish)"
else
    echo "❌ publish_opt_in: true (DANGER - auto-publish enabled)"
    echo "   This channel should NOT auto-publish due to sensitive content"
fi

# Check redact_personal_info
if grep -q "redact_personal_info: true" "$MANIFEST_FILE"; then
    echo "✅ redact_personal_info: true (SAFE - personal info protected)"
else
    echo "⚠️  redact_personal_info: false (WARNING - personal info not protected)"
fi

# Check sensitive_topics_flag
if grep -q "sensitive_topics_flag: true" "$MANIFEST_FILE"; then
    echo "✅ sensitive_topics_flag: true (SAFE - sensitive content flagged)"
else
    echo "⚠️  sensitive_topics_flag: false (WARNING - sensitive content not flagged)"
fi

# Check requires_manual_review
if grep -q "requires_manual_review: true" "$MANIFEST_FILE"; then
    echo "✅ requires_manual_review: true (SAFE - manual review required)"
else
    echo "❌ requires_manual_review: false (DANGER - no manual review)"
    echo "   This channel MUST require manual review due to content sensitivity"
fi

# Check avatar configuration
echo ""
echo "🎭 Checking Avatar Configuration..."

if grep -q "enable_duo_mode: true" "$MANIFEST_FILE"; then
    echo "✅ Duo mode enabled (male/female avatar interaction)"
else
    echo "⚠️  Duo mode not enabled"
fi

if grep -q "port: 9510" "$MANIFEST_FILE"; then
    echo "✅ Linlyx-Talker port 9510 configured"
else
    echo "⚠️  Linlyx-Talker port not properly configured"
fi

if grep -q "port: 9520" "$MANIFEST_FILE"; then
    echo "✅ Talking Heads port 9520 configured"
else
    echo "⚠️  Talking Heads port not properly configured"
fi

# Check YouTube compliance
echo ""
echo "📺 Checking YouTube Compliance..."

if grep -q "avatar_disclosure: true" "$MANIFEST_FILE"; then
    echo "✅ Avatar disclosure enabled (YouTube compliant)"
else
    echo "❌ Avatar disclosure not enabled (YouTube violation risk)"
fi

if grep -q "disclaimer_text:" "$MANIFEST_FILE"; then
    echo "✅ Disclaimer text configured"
else
    echo "⚠️  Disclaimer text not configured"
fi

# Check content safety
echo ""
echo "🛡️  Checking Content Safety..."

if grep -q "content_warnings: true" "$MANIFEST_FILE"; then
    echo "✅ Content warnings enabled"
else
    echo "⚠️  Content warnings not enabled"
fi

if grep -q "age_restriction: \"mature\"" "$MANIFEST_FILE"; then
    echo "✅ Age restriction set to mature"
else
    echo "⚠️  Age restriction not properly set"
fi

# Check emergency controls
echo ""
echo "🚨 Checking Emergency Controls..."

if grep -q "auto_stop_on_controversy: true" "$MANIFEST_FILE"; then
    echo "✅ Auto-stop on controversy enabled"
else
    echo "⚠️  Auto-stop on controversy not enabled"
fi

if grep -q "manual_override_required: true" "$MANIFEST_FILE"; then
    echo "✅ Manual override required"
else
    echo "⚠️  Manual override not required"
fi

# Check humor configuration
echo ""
echo "😄 Checking Humor Configuration..."

if grep -q "humor_level: \"high\"" "$MANIFEST_FILE"; then
    echo "✅ High humor level configured"
else
    echo "⚠️  Humor level not properly configured"
fi

if grep -q "dry_humor" "$MANIFEST_FILE"; then
    echo "✅ Dry humor style configured"
else
    echo "⚠️  Dry humor style not configured"
fi

# Check research requirements
echo ""
echo "🔬 Checking Research Requirements..."

if grep -q "humor_ai_training: true" "$MANIFEST_FILE"; then
    echo "✅ Humor AI training enabled"
else
    echo "⚠️  Humor AI training not enabled"
fi

if grep -q "avatar_interaction_optimization" "$MANIFEST_FILE"; then
    echo "✅ Avatar interaction optimization configured"
else
    echo "⚠️  Avatar interaction optimization not configured"
fi

# Generate summary
echo ""
echo "📋 RIGHT PERSPECTIVE SAFETY SUMMARY"
echo "==================================="

# Count issues
SAFETY_ISSUES=0
WARNINGS=0

# Check for critical issues
if ! grep -q "publish_opt_in: false" "$MANIFEST_FILE"; then
    ((SAFETY_ISSUES++))
fi

if ! grep -q "requires_manual_review: true" "$MANIFEST_FILE"; then
    ((SAFETY_ISSUES++))
fi

if ! grep -q "avatar_disclosure: true" "$MANIFEST_FILE"; then
    ((SAFETY_ISSUES++))
fi

# Count warnings (non-critical but important)
if ! grep -q "redact_personal_info: true" "$MANIFEST_FILE"; then
    ((WARNINGS++))
fi

if ! grep -q "sensitive_topics_flag: true" "$MANIFEST_FILE"; then
    ((WARNINGS++))
fi

if ! grep -q "content_warnings: true" "$MANIFEST_FILE"; then
    ((WARNINGS++))
fi

# Display summary
if [ $SAFETY_ISSUES -eq 0 ]; then
    echo "✅ SAFETY STATUS: PASSED"
    echo "   No critical safety issues found"
else
    echo "❌ SAFETY STATUS: FAILED"
    echo "   $SAFETY_ISSUES critical safety issues found"
fi

if [ $WARNINGS -gt 0 ]; then
    echo "⚠️  WARNINGS: $WARNINGS non-critical issues found"
else
    echo "✅ No warnings"
fi

echo ""
echo "🎯 RECOMMENDATIONS:"
echo "==================="

if [ $SAFETY_ISSUES -gt 0 ]; then
    echo "🚨 CRITICAL: Fix safety issues before enabling this channel"
    echo "   - Ensure publish_opt_in: false"
    echo "   - Ensure requires_manual_review: true"
    echo "   - Ensure avatar_disclosure: true"
fi

if [ $WARNINGS -gt 0 ]; then
    echo "⚠️  Consider addressing warnings for better safety"
fi

echo ""
echo "📝 NEXT STEPS:"
echo "=============="
echo "1. Review and fix any safety issues"
echo "2. Test avatar interactions thoroughly"
echo "3. Verify humor AI training is working"
echo "4. Only enable publish_opt_in: true when ready"
echo "5. Monitor content for appropriateness"
echo ""
echo "🎭 'The Right Perspective' is a special case requiring extra care!"
echo "   This channel needs professional-level setup and monitoring."
echo ""

# Exit with appropriate code
if [ $SAFETY_ISSUES -eq 0 ]; then
    echo "✅ Right Perspective check: PASSED"
    exit 0
else
    echo "❌ Right Perspective check: FAILED"
    exit 1
fi
